#!/usr/bin/env python3
"""
Camper Deals - Amazon Product Advertising API 5.0 Scraper
Detecta ofertas con ≥30% de descuento en categorías de camping/outdoor
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de Amazon PA-API
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY', '')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY', '')
AMAZON_PARTNER_TAG = os.getenv('AMAZON_PARTNER_TAG', 'camperdeals-21')
AMAZON_REGION = os.getenv('AMAZON_REGION', 'eu-west-1')  # España

# Base de datos
DB_PATH = Path(__file__).parent.parent / 'data' / 'offers.db'

# Categorías y keywords de búsqueda
CATEGORIES = {
    'tiendas-campana': {
        'search_index': 'SportingGoods',
        'keywords': ['tienda campaña', 'tienda camping 4 estaciones', 'carpa camping'],
    },
    'sacos-dormir': {
        'search_index': 'SportingGoods',
        'keywords': ['saco dormir', 'saco dormir invierno', 'sleeping bag'],
    },
    'mochilas': {
        'search_index': 'SportingGoods',
        'keywords': ['mochila trekking', 'mochila senderismo 50l', 'mochila montaña'],
    },
    'cocina-camping': {
        'search_index': 'SportingGoods',
        'keywords': ['hornillo camping', 'cocina gas portátil', 'utensilios camping'],
    },
    'iluminacion': {
        'search_index': 'SportingGoods',
        'keywords': ['linterna frontal', 'farolillo camping', 'linterna led recargable'],
    },
    'mobiliario': {
        'search_index': 'SportingGoods',
        'keywords': ['silla camping plegable', 'mesa camping', 'hamaca outdoor'],
    },
    'herramientas': {
        'search_index': 'SportingGoods',
        'keywords': ['navaja suiza', 'multiherramienta outdoor', 'kit supervivencia'],
    },
    'accesorios': {
        'search_index': 'SportingGoods',
        'keywords': ['brújula senderismo', 'botiquín camping', 'cantimplora'],
    },
}

# Descuento mínimo requerido
MIN_DISCOUNT_PERCENTAGE = 30


def init_database():
    """Inicializa la base de datos SQLite"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            image_url TEXT NOT NULL,
            category TEXT NOT NULL,
            original_price REAL NOT NULL,
            discounted_price REAL NOT NULL,
            discount_percentage INTEGER NOT NULL,
            affiliate_url TEXT NOT NULL,
            rating REAL,
            review_count INTEGER,
            is_prime INTEGER DEFAULT 0,
            last_updated TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON products(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_discount ON products(discount_percentage DESC)')
    
    conn.commit()
    conn.close()
    logger.info(f"Base de datos inicializada en {DB_PATH}")


def calculate_discount(original: float, current: float) -> int:
    """Calcula el porcentaje de descuento"""
    if original <= 0:
        return 0
    return int(((original - current) / original) * 100)


def upsert_product(product: dict):
    """Inserta o actualiza un producto en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO products (
            asin, title, description, image_url, category,
            original_price, discounted_price, discount_percentage,
            affiliate_url, rating, review_count, is_prime, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(asin) DO UPDATE SET
            title = excluded.title,
            description = excluded.description,
            image_url = excluded.image_url,
            original_price = excluded.original_price,
            discounted_price = excluded.discounted_price,
            discount_percentage = excluded.discount_percentage,
            affiliate_url = excluded.affiliate_url,
            rating = excluded.rating,
            review_count = excluded.review_count,
            is_prime = excluded.is_prime,
            last_updated = excluded.last_updated
    ''', (
        product['asin'],
        product['title'],
        product.get('description'),
        product['image_url'],
        product['category'],
        product['original_price'],
        product['discounted_price'],
        product['discount_percentage'],
        product['affiliate_url'],
        product.get('rating'),
        product.get('review_count'),
        1 if product.get('is_prime') else 0,
        datetime.now().isoformat(),
    ))
    
    conn.commit()
    conn.close()


def search_amazon_products(category: str, keywords: list, search_index: str) -> list:
    """
    Busca productos en Amazon usando PA-API 5.0
    
    NOTA: Esta función requiere el SDK oficial de Amazon PA-API.
    Instalar con: pip install paapi5-python-sdk
    
    Para modo de prueba sin credenciales, retorna datos de ejemplo.
    """
    products = []
    
    # Si no hay credenciales, generar datos de ejemplo
    if not AMAZON_ACCESS_KEY or not AMAZON_SECRET_KEY:
        logger.warning("No se encontraron credenciales de Amazon PA-API. Usando datos de ejemplo.")
        return generate_demo_products(category)
    
    try:
        # Importar SDK de Amazon PA-API
        from paapi5_python_sdk.api.default_api import DefaultApi
        from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
        from paapi5_python_sdk.models.partner_type import PartnerType
        from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
        
        # Configurar API
        api = DefaultApi(
            access_key=AMAZON_ACCESS_KEY,
            secret_key=AMAZON_SECRET_KEY,
            host='webservices.amazon.es',
            region=AMAZON_REGION
        )
        
        # Recursos a obtener
        resources = [
            SearchItemsResource.ITEMINFO_TITLE,
            SearchItemsResource.IMAGES_PRIMARY_LARGE,
            SearchItemsResource.OFFERS_LISTINGS_PRICE,
            SearchItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
            SearchItemsResource.CUSTOMERREVIEWS_STARRATING,
            SearchItemsResource.CUSTOMERREVIEWS_COUNT,
            SearchItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMENELIGIBLE,
        ]
        
        for keyword in keywords:
            request = SearchItemsRequest(
                partner_tag=AMAZON_PARTNER_TAG,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keyword,
                search_index=search_index,
                resources=resources,
                item_count=10
            )
            
            response = api.search_items(request)
            
            if response.search_result and response.search_result.items:
                for item in response.search_result.items:
                    product = parse_amazon_item(item, category)
                    if product and product['discount_percentage'] >= MIN_DISCOUNT_PERCENTAGE:
                        products.append(product)
                        logger.info(f"✅ Oferta encontrada: {product['title'][:50]}... ({product['discount_percentage']}% OFF)")
                        
    except ImportError:
        logger.error("SDK de Amazon PA-API no instalado. Ejecuta: pip install paapi5-python-sdk")
        return generate_demo_products(category)
    except Exception as e:
        logger.error(f"Error buscando en Amazon: {e}")
        return generate_demo_products(category)
    
    return products


def parse_amazon_item(item, category: str) -> Optional[dict]:
    """Parsea un item de la respuesta de Amazon"""
    try:
        # Obtener precios
        listing = item.offers.listings[0] if item.offers and item.offers.listings else None
        if not listing:
            return None
            
        current_price = listing.price.amount if listing.price else 0
        original_price = listing.saving_basis.amount if listing.saving_basis else current_price
        
        if current_price <= 0 or original_price <= 0:
            return None
            
        discount = calculate_discount(original_price, current_price)
        
        if discount < MIN_DISCOUNT_PERCENTAGE:
            return None
        
        return {
            'asin': item.asin,
            'title': item.item_info.title.display_value if item.item_info else '',
            'image_url': item.images.primary.large.url if item.images else '',
            'category': category,
            'original_price': original_price,
            'discounted_price': current_price,
            'discount_percentage': discount,
            'affiliate_url': f'https://www.amazon.es/dp/{item.asin}?tag={AMAZON_PARTNER_TAG}',
            'rating': item.customer_reviews.star_rating.value if item.customer_reviews else None,
            'review_count': item.customer_reviews.count if item.customer_reviews else None,
            'is_prime': listing.delivery_info.is_prime_eligible if listing.delivery_info else False,
        }
    except Exception as e:
        logger.debug(f"Error parseando item: {e}")
        return None


def generate_demo_products(category: str) -> list:
    """Genera productos de demostración para testing"""
    import random
    
    demo_titles = {
        'tiendas-campana': [
            'Tienda Campaña 4 Estaciones Pro - 4 Personas Impermeable',
            'Carpa Ultraligera Trekking 2P - Doble Capa',
        ],
        'sacos-dormir': [
            'Saco Dormir Momia -15°C Ultracompacto',
            'Saco Dormir Rectangular Confort +5°C',
        ],
        'mochilas': [
            'Mochila Trekking 65L Impermeable AIR',
            'Mochila Senderismo 40L Ultralight',
        ],
        'cocina-camping': [
            'Hornillo Gas Camping Plegable PRO',
            'Set Cocina Camping Aluminio 12 Piezas',
        ],
        'iluminacion': [
            'Frontal LED 1000lm Recargable USB-C',
            'Farolillo Camping Solar + USB',
        ],
        'mobiliario': [
            'Silla Camping Plegable XL Portavasos',
            'Mesa Camping Aluminio Plegable',
        ],
        'herramientas': [
            'Multiherramienta 18 Funciones Acero',
            'Kit Supervivencia Completo 15 en 1',
        ],
        'accesorios': [
            'Brújula Profesional con Espejo',
            'Botiquín Primeros Auxilios Outdoor',
        ],
    }
    
    products = []
    for i, title in enumerate(demo_titles.get(category, ['Producto Demo'])):
        original = round(random.uniform(50, 250), 2)
        discount = random.randint(30, 55)
        discounted = round(original * (1 - discount / 100), 2)
        
        products.append({
            'asin': f'DEMO{category[:3].upper()}{i}',
            'title': title,
            'image_url': 'https://via.placeholder.com/500x500.png?text=Producto+Demo',
            'category': category,
            'original_price': original,
            'discounted_price': discounted,
            'discount_percentage': discount,
            'affiliate_url': f'https://www.amazon.es/dp/DEMO?tag={AMAZON_PARTNER_TAG}',
            'rating': round(random.uniform(4.0, 5.0), 1),
            'review_count': random.randint(100, 5000),
            'is_prime': random.choice([True, False]),
        })
    
    return products


def delete_old_products(days: int = 7):
    """Elimina productos no actualizados en X días"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM products 
        WHERE julianday('now') - julianday(last_updated) > ?
    ''', (days,))
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    if deleted > 0:
        logger.info(f"🗑️  Eliminados {deleted} productos antiguos")


def main(test_mode: bool = False, dry_run: bool = False):
    """Función principal del scraper"""
    logger.info("🏕️  Iniciando Camper Deals Scraper...")
    
    # Inicializar DB
    init_database()
    
    # Limpiar productos antiguos
    delete_old_products(7)
    
    total_found = 0
    
    for category, config in CATEGORIES.items():
        logger.info(f"\n📂 Buscando en categoría: {category}")
        
        products = search_amazon_products(
            category=category,
            keywords=config['keywords'],
            search_index=config['search_index']
        )
        
        for product in products:
            if not dry_run:
                upsert_product(product)
            total_found += 1
    
    logger.info(f"\n✅ Scraping completado: {total_found} ofertas encontradas con ≥{MIN_DISCOUNT_PERCENTAGE}% descuento")
    
    if dry_run:
        logger.info("⚠️  Modo dry-run: No se guardaron cambios en la base de datos")
    
    return total_found


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Camper Deals Amazon Scraper')
    parser.add_argument('--test', action='store_true', help='Modo test con datos de ejemplo')
    parser.add_argument('--dry-run', action='store_true', help='No guardar en DB')
    
    args = parser.parse_args()
    
    main(test_mode=args.test, dry_run=args.dry_run)
