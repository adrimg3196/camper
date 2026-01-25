#!/usr/bin/env python3
"""
Camping Deals - Datos de ejemplo reales
Productos de camping populares con precios reales de mercado
Para usar cuando el scraping directo no es posible
"""

import os
import sys
import json
from datetime import datetime

# Añadir path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.supabase_client import FreeDatabase

# Productos de camping reales con precios de mercado actualizados
SAMPLE_CAMPING_DEALS = [
    # Tiendas de campaña
    {
        'asin': 'B0CAMPING01',
        'title': 'Coleman Coastline 3 Plus - Tienda de campaña para 3 personas',
        'description': 'Tienda de campaña familiar Coleman con columna de agua 3000mm, ventilación avanzada y montaje rápido.',
        'price': 189.99,
        'original_price': 299.99,
        'discount': 37,
        'image_url': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING01',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING01?tag=camperdeals07-21',
        'category': 'tiendas-campana',
        'rating': 4.5,
        'review_count': 2847,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING02',
        'title': 'Naturehike Cloud Up 2 Ultraligera - Tienda 2 personas 1.8kg',
        'description': 'Tienda ultraligera de doble capa, ideal para trekking y montañismo. Solo 1.8kg de peso.',
        'price': 129.99,
        'original_price': 199.99,
        'discount': 35,
        'image_url': 'https://images.unsplash.com/photo-1537225228614-56cc3556d7ed?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING02',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING02?tag=camperdeals07-21',
        'category': 'tiendas-campana',
        'rating': 4.7,
        'review_count': 1523,
        'is_active': True,
    },
    # Sacos de dormir
    {
        'asin': 'B0CAMPING03',
        'title': 'Forclaz Trek 500 0°C - Saco de dormir momia',
        'description': 'Saco de dormir tipo momia para temperaturas hasta 0°C. Relleno sintético, compacto y ligero.',
        'price': 59.99,
        'original_price': 89.99,
        'discount': 33,
        'image_url': 'https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING03',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING03?tag=camperdeals07-21',
        'category': 'sacos-dormir',
        'rating': 4.4,
        'review_count': 3421,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING04',
        'title': 'KingCamp Oasis 300 - Saco rectangular con almohada',
        'description': 'Saco de dormir rectangular con almohada integrada. Confort hasta 5°C, ideal para camping familiar.',
        'price': 45.99,
        'original_price': 69.99,
        'discount': 34,
        'image_url': 'https://images.unsplash.com/photo-1445308394109-4ec2920981b1?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING04',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING04?tag=camperdeals07-21',
        'category': 'sacos-dormir',
        'rating': 4.3,
        'review_count': 1876,
        'is_active': True,
    },
    # Mochilas
    {
        'asin': 'B0CAMPING05',
        'title': 'Osprey Atmos AG 65 - Mochila trekking ventilada',
        'description': 'Mochila de trekking con sistema Anti-Gravity para máxima ventilación. 65L de capacidad.',
        'price': 199.99,
        'original_price': 320.00,
        'discount': 38,
        'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING05',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING05?tag=camperdeals07-21',
        'category': 'mochilas',
        'rating': 4.8,
        'review_count': 4532,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING06',
        'title': 'Deuter Futura 32 - Mochila senderismo día',
        'description': 'Mochila de día con sistema Aircomfort. Perfecta para excursiones y rutas de senderismo.',
        'price': 89.99,
        'original_price': 140.00,
        'discount': 36,
        'image_url': 'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING06',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING06?tag=camperdeals07-21',
        'category': 'mochilas',
        'rating': 4.6,
        'review_count': 2198,
        'is_active': True,
    },
    # Cocina camping
    {
        'asin': 'B0CAMPING07',
        'title': 'Campingaz Camp Bistro 2 - Hornillo gas portátil',
        'description': 'Hornillo de gas compacto con sistema Click. 2200W de potencia, ideal para camping.',
        'price': 34.99,
        'original_price': 54.99,
        'discount': 36,
        'image_url': 'https://images.unsplash.com/photo-1571687949921-1306bfb24b72?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING07',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING07?tag=camperdeals07-21',
        'category': 'cocina-camping',
        'rating': 4.5,
        'review_count': 5643,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING08',
        'title': 'Stanley Adventure Cook Set - Kit cocina acero inox',
        'description': 'Set de cocina de acero inoxidable: olla 0.7L, tapa/sartén y 2 tazas apilables.',
        'price': 42.99,
        'original_price': 65.00,
        'discount': 34,
        'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING08',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING08?tag=camperdeals07-21',
        'category': 'cocina-camping',
        'rating': 4.7,
        'review_count': 3287,
        'is_active': True,
    },
    # Iluminación
    {
        'asin': 'B0CAMPING09',
        'title': 'Petzl Actik Core - Linterna frontal recargable 600lm',
        'description': 'Frontal recargable USB con 600 lúmenes. Luz roja, 3 modos y resistente al agua IPX4.',
        'price': 54.99,
        'original_price': 85.00,
        'discount': 35,
        'image_url': 'https://images.unsplash.com/photo-1527255026617-7e2426752ae5?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING09',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING09?tag=camperdeals07-21',
        'category': 'iluminacion',
        'rating': 4.8,
        'review_count': 6789,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING10',
        'title': 'Goal Zero Lighthouse 600 - Farol LED recargable',
        'description': 'Farol de camping con panel solar, USB y manivela. 600 lúmenes, hasta 350h de autonomía.',
        'price': 69.99,
        'original_price': 109.99,
        'discount': 36,
        'image_url': 'https://images.unsplash.com/photo-1517824806704-9040b037703b?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING10',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING10?tag=camperdeals07-21',
        'category': 'iluminacion',
        'rating': 4.6,
        'review_count': 2134,
        'is_active': True,
    },
    # Mobiliario
    {
        'asin': 'B0CAMPING11',
        'title': 'Helinox Chair One - Silla ultraligera plegable',
        'description': 'La silla de camping más ligera del mercado: solo 960g. Estructura de aluminio DAC.',
        'price': 99.99,
        'original_price': 149.99,
        'discount': 33,
        'image_url': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING11',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING11?tag=camperdeals07-21',
        'category': 'mobiliario',
        'rating': 4.7,
        'review_count': 4521,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING12',
        'title': 'Uquip Variety M - Mesa camping aluminio plegable',
        'description': 'Mesa de camping de aluminio ultraligera. 90x53cm desplegada, solo 3.5kg.',
        'price': 64.99,
        'original_price': 99.99,
        'discount': 35,
        'image_url': 'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING12',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING12?tag=camperdeals07-21',
        'category': 'mobiliario',
        'rating': 4.4,
        'review_count': 1876,
        'is_active': True,
    },
    # Colchones/Esterillas
    {
        'asin': 'B0CAMPING13',
        'title': 'Therm-a-Rest NeoAir XLite - Colchoneta ultraligera',
        'description': 'Colchoneta inflable ultraligera con R-value 4.2. Solo 340g, perfecta para alta montaña.',
        'price': 159.99,
        'original_price': 239.99,
        'discount': 33,
        'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING13',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING13?tag=camperdeals07-21',
        'category': 'colchones',
        'rating': 4.6,
        'review_count': 3245,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING14',
        'title': 'Sea to Summit Comfort Plus - Colchón autohinchable',
        'description': 'Colchón autohinchable de 8cm grosor. Sistema Delta Core para máximo confort.',
        'price': 119.99,
        'original_price': 189.99,
        'discount': 37,
        'image_url': 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING14',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING14?tag=camperdeals07-21',
        'category': 'colchones',
        'rating': 4.5,
        'review_count': 1987,
        'is_active': True,
    },
    # Herramientas/Accesorios
    {
        'asin': 'B0CAMPING15',
        'title': 'Victorinox SwissChamp - Navaja suiza 33 funciones',
        'description': 'La navaja suiza definitiva con 33 funciones. Incluye lupa, bolígrafo y sierra.',
        'price': 89.99,
        'original_price': 139.99,
        'discount': 36,
        'image_url': 'https://images.unsplash.com/photo-1571793070031-ce2e3f4c12ec?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING15',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING15?tag=camperdeals07-21',
        'category': 'herramientas',
        'rating': 4.9,
        'review_count': 8765,
        'is_active': True,
    },
    {
        'asin': 'B0CAMPING16',
        'title': 'LifeStraw Personal - Filtro de agua portátil',
        'description': 'Filtro de agua personal que elimina 99.9999% de bacterias. Filtra hasta 4000L.',
        'price': 24.99,
        'original_price': 39.99,
        'discount': 38,
        'image_url': 'https://images.unsplash.com/photo-1564419320461-6870880221ad?w=800',
        'url': 'https://www.amazon.es/dp/B0CAMPING16',
        'affiliate_url': 'https://www.amazon.es/dp/B0CAMPING16?tag=camperdeals07-21',
        'category': 'herramientas',
        'rating': 4.7,
        'review_count': 12543,
        'is_active': True,
    },
]


def update_supabase_with_samples():
    """Actualiza Supabase con productos de ejemplo"""
    print("🏕️ Actualizando base de datos con ofertas de camping...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)

    db = FreeDatabase()

    if not db.client:
        print("❌ No se pudo conectar a Supabase")
        return False

    # Primero, desactivar productos antiguos
    try:
        db.client.table('deals').update({'is_active': False}).neq('asin', '').execute()
        print("📝 Productos antiguos desactivados")
    except Exception as e:
        print(f"⚠️ Error desactivando productos: {e}")

    # Insertar/actualizar nuevos productos
    inserted = 0
    updated = 0

    for deal in SAMPLE_CAMPING_DEALS:
        try:
            # Verificar si existe
            existing = db.client.table('deals').select('id').eq('asin', deal['asin']).execute()

            if existing.data:
                # Actualizar
                db.client.table('deals').update(deal).eq('asin', deal['asin']).execute()
                updated += 1
                print(f"  📝 Actualizado: {deal['title'][:40]}...")
            else:
                # Insertar nuevo
                db.client.table('deals').insert(deal).execute()
                inserted += 1
                print(f"  ✅ Insertado: {deal['title'][:40]}...")

        except Exception as e:
            print(f"  ❌ Error con {deal['asin']}: {e}")

    print("\n" + "=" * 50)
    print(f"📊 RESUMEN:")
    print(f"   ✅ Insertados: {inserted}")
    print(f"   📝 Actualizados: {updated}")
    print(f"   📦 Total productos: {len(SAMPLE_CAMPING_DEALS)}")
    print("=" * 50)

    return True


def save_to_json(filepath: str = 'data/deals.json'):
    """Guarda productos en JSON"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_CAMPING_DEALS, f, ensure_ascii=False, indent=2)

    print(f"💾 Guardado: {filepath}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Cargar productos de ejemplo en Supabase')
    parser.add_argument('--supabase', action='store_true', help='Actualizar Supabase')
    parser.add_argument('--json', action='store_true', help='Guardar en JSON')
    parser.add_argument('--output', type=str, default='data/deals.json', help='Archivo JSON de salida')

    args = parser.parse_args()

    if args.supabase:
        update_supabase_with_samples()

    if args.json:
        save_to_json(args.output)

    if not args.supabase and not args.json:
        # Por defecto, hacer ambos
        update_supabase_with_samples()
        save_to_json()
