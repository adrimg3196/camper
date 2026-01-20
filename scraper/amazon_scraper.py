#!/usr/bin/env python3
"""
Camping Deals - Amazon Scraper 100% Gratuito
Extrae ofertas de Amazon usando web scraping con anti-detección
Sin necesidad de API oficial de Amazon
"""

import requests
import random
import time
import json
import os
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from fake_useragent import UserAgent
    HAS_FAKE_UA = True
except ImportError:
    HAS_FAKE_UA = False
    print("⚠️ fake_useragent no instalado. Usando User-Agent estático.")


class FreeAmazonScraper:
    """Scraper de Amazon gratuito con sistema anti-detección"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent() if HAS_FAKE_UA else None
        self.base_url = 'https://www.amazon.es'
        self.partner_tag = os.environ.get('AMAZON_PARTNER_TAG', 'camperdeals-21')
        
        # User agents de respaldo
        self.backup_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        ]
        
        # Categorías de camping con keywords
        self.categories = {
            'tiendas-campana': ['tienda campaña', 'tienda camping', 'carpa camping'],
            'sacos-dormir': ['saco dormir', 'sleeping bag', 'saco momia'],
            'mochilas': ['mochila trekking', 'mochila senderismo', 'mochila montaña'],
            'cocina-camping': ['hornillo camping', 'cocina portátil', 'utensilios camping'],
            'iluminacion': ['linterna frontal', 'farolillo camping', 'linterna led'],
            'mobiliario': ['silla camping', 'mesa camping', 'hamaca outdoor'],
            'herramientas': ['navaja suiza', 'multiherramienta', 'kit supervivencia'],
            'accesorios': ['brújula', 'cantimplora', 'botiquín camping'],
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """Genera headers aleatorios para evitar detección"""
        user_agent = self.ua.random if self.ua else random.choice(self.backup_agents)
        
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
    
    def _random_delay(self, min_sec: float = 2, max_sec: float = 8):
        """Delay aleatorio para simular comportamiento humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def _build_search_url(self, keyword: str, page: int = 1) -> str:
        """Construye URL de búsqueda con filtro de descuento"""
        keyword_encoded = keyword.replace(' ', '+')
        # Filtrar por descuento >= 30%
        return f"{self.base_url}/s?k={keyword_encoded}&rh=p_n_pct-off-with-tax%3A30-&page={page}"
    
    def _extract_price(self, price_str: str) -> Optional[float]:
        """Extrae precio numérico de string"""
        if not price_str:
            return None
        try:
            # Limpiar y convertir: "29,99 €" -> 29.99
            clean = re.sub(r'[^\d,.]', '', price_str)
            clean = clean.replace(',', '.')
            # Si hay múltiples puntos, quedarse solo con el último como decimal
            parts = clean.rsplit('.', 1)
            if len(parts) == 2:
                clean = parts[0].replace('.', '') + '.' + parts[1]
            return float(clean)
        except (ValueError, AttributeError):
            return None
    
    def _extract_asin(self, product_element) -> Optional[str]:
        """Extrae ASIN del producto"""
        asin = product_element.get('data-asin')
        if asin and len(asin) == 10:
            return asin
        return None
    
    def _extract_deal_data(self, product_element, category: str) -> Optional[Dict]:
        """Extrae todos los datos de un producto"""
        try:
            asin = self._extract_asin(product_element)
            if not asin:
                return None
            
            # Título
            title_elem = product_element.find('h2')
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # Imagen
            img_elem = product_element.find('img', {'class': 's-image'})
            image_url = img_elem.get('src') if img_elem else None
            
            # Precio actual
            price_elem = product_element.find('span', {'class': 'a-price-whole'})
            price_fraction = product_element.find('span', {'class': 'a-price-fraction'})
            
            if not price_elem:
                return None
                
            current_price_str = price_elem.get_text(strip=True)
            if price_fraction:
                current_price_str += '.' + price_fraction.get_text(strip=True)
            current_price = self._extract_price(current_price_str)
            
            if not current_price:
                return None
            
            # Precio original (tachado)
            original_elem = product_element.find('span', {'class': 'a-price', 'data-a-strike': 'true'})
            if original_elem:
                original_offscreen = original_elem.find('span', {'class': 'a-offscreen'})
                original_price = self._extract_price(original_offscreen.get_text()) if original_offscreen else current_price
            else:
                # Buscar precio de lista alternativo
                list_price_elem = product_element.find('span', {'class': 'a-text-price'})
                if list_price_elem:
                    original_price = self._extract_price(list_price_elem.get_text())
                else:
                    original_price = current_price
            
            if not original_price or original_price <= current_price:
                return None
            
            # Calcular descuento
            discount = round(((original_price - current_price) / original_price) * 100)
            
            if discount < 30:
                return None
            
            # Rating
            rating_elem = product_element.find('span', {'class': 'a-icon-alt'})
            rating = None
            if rating_elem:
                rating_text = rating_elem.get_text()
                rating_match = re.search(r'(\d[,.]?\d?)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1).replace(',', '.'))
            
            # Número de reseñas
            reviews_elem = product_element.find('span', {'class': 'a-size-base', 'dir': 'auto'})
            review_count = None
            if reviews_elem:
                reviews_text = reviews_elem.get_text().replace('.', '').replace(',', '')
                reviews_match = re.search(r'(\d+)', reviews_text)
                if reviews_match:
                    review_count = int(reviews_match.group(1))
            
            # Prime
            is_prime = bool(product_element.find('i', {'class': 'a-icon-prime'}))
            
            # URL de afiliado
            affiliate_url = f"{self.base_url}/dp/{asin}?tag={self.partner_tag}"
            
            return {
                'asin': asin,
                'title': title[:200],  # Limitar longitud
                'image_url': image_url,
                'category': category,
                'current_price': current_price,
                'original_price': original_price,
                'discount': discount,
                'affiliate_url': affiliate_url,
                'rating': rating,
                'review_count': review_count,
                'is_prime': is_prime,
                'scraped_at': datetime.now().isoformat(),
            }
            
        except Exception as e:
            print(f"⚠️ Error extrayendo datos: {e}")
            return None
    
    def scrape_category(self, category: str, max_pages: int = 2) -> List[Dict]:
        """Scrapea una categoría completa"""
        deals = []
        keywords = self.categories.get(category, [category])
        
        print(f"\n📂 Scrapeando categoría: {category}")
        
        for keyword in keywords:
            for page in range(1, max_pages + 1):
                url = self._build_search_url(keyword, page)
                print(f"  🔍 Buscando: '{keyword}' (página {page})")
                
                self._random_delay(3, 8)
                
                try:
                    response = self.session.get(url, headers=self._get_headers(), timeout=15)
                    
                    if response.status_code != 200:
                        print(f"  ⚠️ HTTP {response.status_code}")
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar productos
                    products = soup.find_all('div', {'data-component-type': 's-search-result'})
                    
                    for product in products:
                        deal = self._extract_deal_data(product, category)
                        if deal:
                            # Evitar duplicados por ASIN
                            if not any(d['asin'] == deal['asin'] for d in deals):
                                deals.append(deal)
                                print(f"    ✅ {deal['title'][:50]}... (-{deal['discount']}%)")
                    
                except requests.RequestException as e:
                    print(f"  ❌ Error de red: {e}")
                    continue
        
        return deals
    
    def scrape_all_categories(self) -> List[Dict]:
        """Scrapea todas las categorías de camping"""
        all_deals = []
        
        print("🏕️ Iniciando scraping de ofertas camping...")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        for category in self.categories.keys():
            category_deals = self.scrape_category(category)
            all_deals.extend(category_deals)
            
            # Pausa entre categorías para evitar bloqueos
            if category != list(self.categories.keys())[-1]:
                print(f"  ⏳ Pausa entre categorías...")
                self._random_delay(10, 20)
        
        # Ordenar por descuento
        all_deals.sort(key=lambda x: x['discount'], reverse=True)
        
        print(f"\n📊 Total ofertas encontradas: {len(all_deals)}")
        print(f"🏆 Mayor descuento: {all_deals[0]['discount']}%" if all_deals else "")
        
        return all_deals
    
    def save_deals_json(self, deals: List[Dict], filepath: str = 'data/deals.json'):
        """Guarda las ofertas en JSON para GitHub Pages"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Ofertas guardadas en {filepath}")


def main():
    """Función principal del scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Camping Deals Amazon Scraper')
    parser.add_argument('--category', type=str, help='Categoría específica a scrapear')
    parser.add_argument('--output', type=str, default='data/deals.json', help='Archivo de salida')
    parser.add_argument('--test', action='store_true', help='Modo test (menos requests)')
    
    args = parser.parse_args()
    
    scraper = FreeAmazonScraper()
    
    if args.category:
        deals = scraper.scrape_category(args.category, max_pages=1 if args.test else 2)
    else:
        deals = scraper.scrape_all_categories()
    
    if deals:
        scraper.save_deals_json(deals, args.output)
    
    return deals


if __name__ == '__main__':
    main()
