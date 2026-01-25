#!/usr/bin/env python3
"""
Camping Deals - Enhanced Scraper con múltiples fuentes
Integra herramientas opensource: Scrapy, Playwright, Beautiful Soup
Con sistema anti-detección mejorado y soporte multi-tienda
"""

import os
import sys
import json
import random
import time
import re
import hashlib
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse, quote_plus

import requests
from bs4 import BeautifulSoup

# Opcional: Scrapy para scraping a gran escala
try:
    import scrapy
    from scrapy.crawler import CrawlerProcess
    from scrapy.settings import Settings
    HAS_SCRAPY = True
except ImportError:
    HAS_SCRAPY = False

# Opcional: Playwright para sitios con JavaScript pesado
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# Fake user agent
try:
    from fake_useragent import UserAgent
    HAS_FAKE_UA = True
except ImportError:
    HAS_FAKE_UA = False


@dataclass
class ProductDeal:
    """Estructura estandarizada para ofertas de cualquier tienda"""
    source: str           # amazon, decathlon, pccomponentes, etc.
    external_id: str      # ASIN, SKU, etc.
    title: str
    description: str
    image_url: str
    product_url: str
    affiliate_url: str
    current_price: float
    original_price: float
    discount: int
    category: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    is_prime: bool = False
    brand: Optional[str] = None
    availability: str = "in_stock"
    scraped_at: str = ""

    def __post_init__(self):
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_supabase_format(self) -> Dict:
        """Convierte al formato de la tabla deals de Supabase"""
        return {
            'asin': self.external_id,
            'title': self.title[:200],
            'description': self.description[:500] if self.description else f"Descuento del {self.discount}%",
            'price': self.current_price,
            'original_price': self.original_price,
            'discount': self.discount,
            'image_url': self.image_url,
            'url': self.product_url,
            'affiliate_url': self.affiliate_url,
            'category': self.category,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_active': True,
        }


class BaseScraper(ABC):
    """Clase base para todos los scrapers"""

    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent() if HAS_FAKE_UA else None
        self.results: List[ProductDeal] = []

        # User agents de respaldo
        self.backup_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]

    def _get_random_ua(self) -> str:
        """Obtiene un User-Agent aleatorio"""
        if self.ua:
            try:
                return self.ua.random
            except:
                pass
        return random.choice(self.backup_agents)

    def _get_headers(self) -> Dict[str, str]:
        """Headers con anti-detección"""
        return {
            'User-Agent': self._get_random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def _random_delay(self, min_sec: float = 2, max_sec: float = 6):
        """Delay aleatorio para simular comportamiento humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _extract_price(self, price_str: str) -> Optional[float]:
        """Extrae precio numérico de string"""
        if not price_str:
            return None
        try:
            clean = re.sub(r'[^\d,.]', '', price_str)
            clean = clean.replace(',', '.')
            parts = clean.rsplit('.', 1)
            if len(parts) == 2 and len(parts[1]) <= 2:
                clean = parts[0].replace('.', '') + '.' + parts[1]
            else:
                clean = clean.replace('.', '')
            return float(clean) if clean else None
        except (ValueError, AttributeError):
            return None

    def _calculate_discount(self, original: float, current: float) -> int:
        """Calcula porcentaje de descuento"""
        if original <= 0 or current <= 0 or original <= current:
            return 0
        return round(((original - current) / original) * 100)

    @abstractmethod
    def get_source_name(self) -> str:
        """Nombre de la fuente"""
        pass

    @abstractmethod
    def scrape_category(self, category: str, max_pages: int = 2) -> List[ProductDeal]:
        """Scrapea una categoría"""
        pass

    @abstractmethod
    def build_affiliate_url(self, product_url: str, product_id: str) -> str:
        """Construye URL de afiliado"""
        pass


class AmazonScraper(BaseScraper):
    """Scraper mejorado para Amazon España"""

    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.amazon.es'
        self.partner_tag = os.environ.get('AMAZON_PARTNER_TAG', 'camperdeals07-21')

        # Categorías de camping expandidas
        self.categories = {
            'tiendas-campana': [
                'tienda campaña camping',
                'tienda instantánea',
                'carpa camping familiar',
            ],
            'sacos-dormir': [
                'saco dormir camping',
                'saco momia montaña',
                'sleeping bag outdoor',
            ],
            'mochilas': [
                'mochila trekking 50L',
                'mochila senderismo',
                'mochila camping impermeable',
            ],
            'cocina-camping': [
                'hornillo gas camping',
                'cocina portátil outdoor',
                'set utensilios camping',
            ],
            'iluminacion': [
                'linterna frontal LED',
                'farol camping recargable',
                'luz tienda campaña',
            ],
            'mobiliario': [
                'silla camping plegable',
                'mesa camping aluminio',
                'hamaca camping portátil',
            ],
            'colchones': [
                'colchón inflable camping',
                'esterilla aislante',
                'cama plegable camping',
            ],
        }

    def get_source_name(self) -> str:
        return "amazon"

    def build_affiliate_url(self, product_url: str, product_id: str) -> str:
        return f"{self.base_url}/dp/{product_id}?tag={self.partner_tag}"

    def _build_search_url(self, keyword: str, page: int = 1) -> str:
        """URL de búsqueda con filtro de descuento >= 30%"""
        keyword_encoded = quote_plus(keyword)
        return f"{self.base_url}/s?k={keyword_encoded}&rh=p_n_pct-off-with-tax%3A30-&page={page}"

    def _extract_product(self, element, category: str) -> Optional[ProductDeal]:
        """Extrae datos de un elemento de producto"""
        try:
            # ASIN
            asin = element.get('data-asin')
            if not asin or len(asin) != 10:
                return None

            # Título
            title_elem = element.find('h2')
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)

            # Imagen
            img_elem = element.find('img', {'class': 's-image'})
            image_url = img_elem.get('src') if img_elem else ''

            # Precio actual
            price_whole = element.find('span', {'class': 'a-price-whole'})
            price_fraction = element.find('span', {'class': 'a-price-fraction'})

            if not price_whole:
                return None

            current_price_str = price_whole.get_text(strip=True)
            if price_fraction:
                current_price_str += '.' + price_fraction.get_text(strip=True)
            current_price = self._extract_price(current_price_str)

            if not current_price or current_price <= 0:
                return None

            # Precio original
            original_elem = element.find('span', {'class': 'a-price', 'data-a-strike': 'true'})
            if original_elem:
                offscreen = original_elem.find('span', {'class': 'a-offscreen'})
                original_price = self._extract_price(offscreen.get_text()) if offscreen else None
            else:
                list_price = element.find('span', {'class': 'a-text-price'})
                original_price = self._extract_price(list_price.get_text()) if list_price else None

            if not original_price or original_price <= current_price:
                return None

            discount = self._calculate_discount(original_price, current_price)
            if discount < 30:
                return None

            # Rating
            rating = None
            rating_elem = element.find('span', {'class': 'a-icon-alt'})
            if rating_elem:
                match = re.search(r'(\d[,.]?\d?)', rating_elem.get_text())
                if match:
                    rating = float(match.group(1).replace(',', '.'))

            # Reviews
            review_count = None
            reviews_elem = element.find('span', {'class': 'a-size-base', 'dir': 'auto'})
            if reviews_elem:
                match = re.search(r'([\d.]+)', reviews_elem.get_text().replace('.', ''))
                if match:
                    review_count = int(match.group(1))

            # Prime
            is_prime = bool(element.find('i', {'class': 'a-icon-prime'}))

            # Brand
            brand = None
            brand_elem = element.find('span', {'class': 'a-size-base-plus'})
            if brand_elem:
                brand = brand_elem.get_text(strip=True)

            return ProductDeal(
                source=self.get_source_name(),
                external_id=asin,
                title=title[:200],
                description=f"Ahorra {discount}% - Precio original: {original_price:.2f}€",
                image_url=image_url,
                product_url=f"{self.base_url}/dp/{asin}",
                affiliate_url=self.build_affiliate_url('', asin),
                current_price=current_price,
                original_price=original_price,
                discount=discount,
                category=category,
                rating=rating,
                review_count=review_count,
                is_prime=is_prime,
                brand=brand,
            )

        except Exception as e:
            print(f"  ⚠️ Error extrayendo producto: {e}")
            return None

    def scrape_category(self, category: str, max_pages: int = 2) -> List[ProductDeal]:
        """Scrapea una categoría de Amazon"""
        deals = []
        keywords = self.categories.get(category, [category])
        seen_asins = set()

        print(f"\n📂 [{self.get_source_name().upper()}] Scrapeando: {category}")

        for keyword in keywords:
            for page in range(1, max_pages + 1):
                url = self._build_search_url(keyword, page)
                print(f"  🔍 '{keyword}' (pág {page})")

                self._random_delay(3, 7)

                try:
                    response = self.session.get(
                        url,
                        headers=self._get_headers(),
                        timeout=20
                    )

                    if response.status_code != 200:
                        print(f"    ⚠️ HTTP {response.status_code}")
                        continue

                    soup = BeautifulSoup(response.content, 'html.parser')
                    products = soup.find_all('div', {'data-component-type': 's-search-result'})

                    for product in products:
                        deal = self._extract_product(product, category)
                        if deal and deal.external_id not in seen_asins:
                            seen_asins.add(deal.external_id)
                            deals.append(deal)
                            print(f"    ✅ {deal.title[:45]}... (-{deal.discount}%)")

                except requests.RequestException as e:
                    print(f"    ❌ Error: {e}")
                    continue

        return deals

    def scrape_all(self, max_pages: int = 2) -> List[ProductDeal]:
        """Scrapea todas las categorías"""
        all_deals = []

        for category in self.categories.keys():
            deals = self.scrape_category(category, max_pages)
            all_deals.extend(deals)

            if category != list(self.categories.keys())[-1]:
                print(f"  ⏳ Pausa entre categorías...")
                self._random_delay(10, 20)

        all_deals.sort(key=lambda x: x.discount, reverse=True)
        return all_deals


class DecathlonScraper(BaseScraper):
    """Scraper para Decathlon España - Tienda de deportes y camping"""

    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.decathlon.es'
        self.affiliate_id = os.environ.get('DECATHLON_AFFILIATE_ID', '')

        self.categories = {
            'tiendas-campana': '/camping/tiendas-de-campana',
            'sacos-dormir': '/camping/sacos-de-dormir',
            'mochilas': '/camping/mochilas-trekking',
            'colchones': '/camping/colchones-y-esterillas',
            'cocina-camping': '/camping/cocinas-de-camping',
            'mobiliario': '/camping/mobiliario-de-camping',
        }

    def get_source_name(self) -> str:
        return "decathlon"

    def build_affiliate_url(self, product_url: str, product_id: str) -> str:
        if self.affiliate_id:
            return f"{product_url}?affiliate={self.affiliate_id}"
        return product_url

    def _extract_product(self, element, category: str) -> Optional[ProductDeal]:
        """Extrae producto de Decathlon"""
        try:
            # Buscar enlace del producto
            link = element.find('a', {'class': 'dpb-product-model-link'}) or element.find('a', href=True)
            if not link:
                return None

            product_url = urljoin(self.base_url, link.get('href', ''))
            product_id = hashlib.md5(product_url.encode()).hexdigest()[:10]

            # Título
            title_elem = element.find('h2') or element.find('p', {'class': 'product-title'})
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)

            # Imagen
            img = element.find('img')
            image_url = img.get('src') or img.get('data-src', '') if img else ''
            if image_url.startswith('//'):
                image_url = 'https:' + image_url

            # Precios
            current_price = None
            original_price = None

            # Precio actual
            price_elem = element.find('span', {'class': 'current-price'}) or element.find('span', {'class': 'vtmn-price'})
            if price_elem:
                current_price = self._extract_price(price_elem.get_text())

            # Precio original (tachado)
            old_price = element.find('span', {'class': 'old-price'}) or element.find('s')
            if old_price:
                original_price = self._extract_price(old_price.get_text())

            if not current_price or not original_price or original_price <= current_price:
                return None

            discount = self._calculate_discount(original_price, current_price)
            if discount < 20:  # Decathlon tiene menos descuentos, bajamos umbral
                return None

            # Rating
            rating = None
            rating_elem = element.find('span', {'class': 'rating-value'})
            if rating_elem:
                try:
                    rating = float(rating_elem.get_text().replace(',', '.'))
                except:
                    pass

            return ProductDeal(
                source=self.get_source_name(),
                external_id=product_id,
                title=title[:200],
                description=f"Descuento Decathlon: -{discount}%",
                image_url=image_url,
                product_url=product_url,
                affiliate_url=self.build_affiliate_url(product_url, product_id),
                current_price=current_price,
                original_price=original_price,
                discount=discount,
                category=category,
                rating=rating,
                brand="Decathlon",
            )

        except Exception as e:
            print(f"  ⚠️ Error Decathlon: {e}")
            return None

    def scrape_category(self, category: str, max_pages: int = 2) -> List[ProductDeal]:
        """Scrapea una categoría de Decathlon"""
        deals = []
        path = self.categories.get(category)
        if not path:
            return deals

        print(f"\n📂 [{self.get_source_name().upper()}] Scrapeando: {category}")

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}{path}?page={page}"
            print(f"  🔍 Página {page}")

            self._random_delay(2, 5)

            try:
                response = self.session.get(url, headers=self._get_headers(), timeout=15)

                if response.status_code != 200:
                    print(f"    ⚠️ HTTP {response.status_code}")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                products = soup.find_all('div', {'class': 'product-card'}) or soup.find_all('article')

                for product in products[:20]:
                    deal = self._extract_product(product, category)
                    if deal:
                        deals.append(deal)
                        print(f"    ✅ {deal.title[:45]}... (-{deal.discount}%)")

            except requests.RequestException as e:
                print(f"    ❌ Error: {e}")
                continue

        return deals


class MultiSourceScraper:
    """Orquestador que combina múltiples fuentes de scraping"""

    def __init__(self, sources: List[str] = None):
        """
        Args:
            sources: Lista de fuentes a usar ['amazon', 'decathlon']
                    Si es None, usa todas las disponibles
        """
        self.scrapers: Dict[str, BaseScraper] = {}

        available = {
            'amazon': AmazonScraper,
            'decathlon': DecathlonScraper,
        }

        if sources is None:
            sources = list(available.keys())

        for source in sources:
            if source in available:
                self.scrapers[source] = available[source]()
                print(f"✅ Scraper {source} inicializado")

    def scrape_all(self, categories: List[str] = None, max_pages: int = 2) -> List[ProductDeal]:
        """Scrapea todas las fuentes y categorías"""
        all_deals = []

        print("\n" + "=" * 60)
        print("🏕️ MULTI-SOURCE CAMPING DEALS SCRAPER")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📡 Fuentes: {', '.join(self.scrapers.keys())}")
        print("=" * 60)

        for name, scraper in self.scrapers.items():
            try:
                if categories:
                    for cat in categories:
                        deals = scraper.scrape_category(cat, max_pages)
                        all_deals.extend(deals)
                else:
                    if hasattr(scraper, 'scrape_all'):
                        deals = scraper.scrape_all(max_pages)
                    else:
                        deals = []
                        for cat in scraper.categories.keys():
                            cat_deals = scraper.scrape_category(cat, max_pages)
                            deals.extend(cat_deals)
                    all_deals.extend(deals)

                print(f"\n📊 [{name}] Total: {len([d for d in all_deals if d.source == name])} ofertas")

            except Exception as e:
                print(f"❌ Error en {name}: {e}")

        # Ordenar por descuento
        all_deals.sort(key=lambda x: x.discount, reverse=True)

        # Eliminar duplicados por título similar
        unique_deals = []
        seen_titles = set()
        for deal in all_deals:
            title_key = deal.title[:50].lower()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_deals.append(deal)

        print("\n" + "=" * 60)
        print(f"📊 RESUMEN FINAL")
        print(f"   Total ofertas únicas: {len(unique_deals)}")
        if unique_deals:
            print(f"   Mayor descuento: {unique_deals[0].discount}%")
            print(f"   Mejor oferta: {unique_deals[0].title[:50]}...")
        print("=" * 60)

        return unique_deals

    def save_to_json(self, deals: List[ProductDeal], filepath: str = 'data/deals.json'):
        """Guarda ofertas en JSON"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([d.to_dict() for d in deals], f, ensure_ascii=False, indent=2)

        print(f"💾 Guardado: {filepath} ({len(deals)} ofertas)")

    def get_supabase_data(self, deals: List[ProductDeal]) -> List[Dict]:
        """Convierte ofertas al formato de Supabase"""
        return [d.to_supabase_format() for d in deals]


# =============================================================================
# SCRAPY SPIDER (Opcional - para scraping a gran escala)
# =============================================================================

if HAS_SCRAPY:
    class AmazonSpider(scrapy.Spider):
        """Spider de Scrapy para Amazon - Más eficiente para grandes volúmenes"""
        name = 'amazon_camping'
        allowed_domains = ['amazon.es']

        custom_settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'ROBOTSTXT_OBEY': False,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 5,
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'COOKIES_ENABLED': True,
            'RETRY_TIMES': 3,
        }

        def __init__(self, keywords=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.keywords = keywords or ['tienda campaña', 'saco dormir']

        def start_requests(self):
            for kw in self.keywords:
                url = f'https://www.amazon.es/s?k={quote_plus(kw)}&rh=p_n_pct-off-with-tax%3A30-'
                yield scrapy.Request(url, callback=self.parse, meta={'keyword': kw})

        def parse(self, response):
            products = response.css('div[data-component-type="s-search-result"]')

            for product in products:
                asin = product.attrib.get('data-asin')
                if not asin:
                    continue

                yield {
                    'asin': asin,
                    'title': product.css('h2 ::text').get(),
                    'price': product.css('span.a-price-whole ::text').get(),
                    'keyword': response.meta['keyword'],
                }


# =============================================================================
# CLI
# =============================================================================

def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Enhanced Camping Deals Scraper - Multi-Source',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python enhanced_scraper.py                    # Scrapear todas las fuentes
  python enhanced_scraper.py --sources amazon   # Solo Amazon
  python enhanced_scraper.py --category tiendas-campana
  python enhanced_scraper.py --test             # Modo test rápido
        """
    )

    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['amazon', 'decathlon'],
        help='Fuentes a scrapear (default: todas)'
    )
    parser.add_argument(
        '--category',
        type=str,
        help='Categoría específica'
    )
    parser.add_argument(
        '--pages',
        type=int,
        default=2,
        help='Páginas por categoría (default: 2)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/deals.json',
        help='Archivo de salida'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Modo test (1 página, menos categorías)'
    )

    args = parser.parse_args()

    # Configuración
    max_pages = 1 if args.test else args.pages

    # Crear scraper multi-fuente
    scraper = MultiSourceScraper(sources=args.sources)

    # Ejecutar
    if args.category:
        deals = scraper.scrape_all(categories=[args.category], max_pages=max_pages)
    else:
        deals = scraper.scrape_all(max_pages=max_pages)

    # Guardar
    if deals:
        scraper.save_to_json(deals, args.output)

        # También guardar en formato Supabase
        supabase_data = scraper.get_supabase_data(deals)
        supabase_path = args.output.replace('.json', '_supabase.json')
        with open(supabase_path, 'w', encoding='utf-8') as f:
            json.dump(supabase_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Formato Supabase: {supabase_path}")

    return deals


if __name__ == '__main__':
    main()
