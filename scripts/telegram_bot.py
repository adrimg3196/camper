#!/usr/bin/env python3
"""
Camper Deals - Bot de Telegram
Publica ofertas automáticamente en el canal de Telegram
"""

import os
import sqlite3
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '@camperdeals')
DB_PATH = Path(__file__).parent.parent / 'data' / 'offers.db'

# Emojis por categoría
CATEGORY_EMOJIS = {
    'tiendas-campana': '⛺',
    'sacos-dormir': '🛏️',
    'mochilas': '🎒',
    'cocina-camping': '🍳',
    'iluminacion': '🔦',
    'mobiliario': '🪑',
    'herramientas': '🔧',
    'accesorios': '🧭',
}


def get_new_offers(hours: int = 6) -> list:
    """Obtiene ofertas añadidas en las últimas X horas"""
    if not DB_PATH.exists():
        logger.warning("Base de datos no encontrada")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    
    cursor.execute('''
        SELECT * FROM products 
        WHERE last_updated > ?
        ORDER BY discount_percentage DESC
        LIMIT 20
    ''', (cutoff,))
    
    offers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return offers


def format_offer_message(offer: dict) -> str:
    """Formatea una oferta para Telegram"""
    emoji = CATEGORY_EMOJIS.get(offer['category'], '🏕️')
    
    message = f"""
{emoji} *¡OFERTA -{offer['discount_percentage']}%!*

📦 {offer['title'][:100]}...

💰 ~~{offer['original_price']:.2f}€~~ → *{offer['discounted_price']:.2f}€*
💵 Ahorras: {offer['original_price'] - offer['discounted_price']:.2f}€

{"✅ Prime" if offer.get('is_prime') else ""}
{"⭐ " + str(offer['rating']) + "/5" if offer.get('rating') else ""}

🔗 [Ver en Amazon]({offer['affiliate_url']})

_Enlace de afiliado Amazon. Los precios pueden variar._
"""
    return message.strip()


async def send_telegram_message(message: str, photo_url: Optional[str] = None):
    """Envía un mensaje al canal de Telegram"""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Token de Telegram no configurado")
        return False
    
    try:
        from telegram import Bot
        from telegram.constants import ParseMode
        
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        if photo_url and not photo_url.startswith('http://via.placeholder'):
            await bot.send_photo(
                chat_id=TELEGRAM_CHANNEL_ID,
                photo=photo_url,
                caption=message,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
        
        return True
        
    except ImportError:
        logger.error("python-telegram-bot no instalado. Ejecuta: pip install python-telegram-bot")
        return False
    except Exception as e:
        logger.error(f"Error enviando mensaje: {e}")
        return False


async def publish_new_offers():
    """Publica las nuevas ofertas en Telegram"""
    offers = get_new_offers(hours=6)
    
    if not offers:
        logger.info("No hay nuevas ofertas para publicar")
        return 0
    
    logger.info(f"📤 Publicando {len(offers)} ofertas en Telegram...")
    
    published = 0
    for offer in offers:
        message = format_offer_message(offer)
        success = await send_telegram_message(message, offer.get('image_url'))
        
        if success:
            published += 1
            logger.info(f"✅ Publicada: {offer['title'][:50]}...")
            # Rate limiting - esperar entre mensajes
            await asyncio.sleep(3)
        else:
            logger.error(f"❌ Error publicando: {offer['title'][:50]}...")
    
    return published


def test_message():
    """Mensaje de prueba"""
    test_offer = {
        'category': 'tiendas-campana',
        'title': 'Tienda de Campaña 4 Estaciones TEST - Impermeable',
        'original_price': 199.99,
        'discounted_price': 99.99,
        'discount_percentage': 50,
        'is_prime': True,
        'rating': 4.5,
        'affiliate_url': 'https://amazon.es',
    }
    
    print("\n--- MENSAJE DE PRUEBA ---")
    print(format_offer_message(test_offer))
    print("-------------------------\n")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Camper Deals Telegram Bot')
    parser.add_argument('--test', action='store_true', help='Mostrar mensaje de prueba')
    parser.add_argument('--publish-new', action='store_true', help='Publicar nuevas ofertas')
    
    args = parser.parse_args()
    
    if args.test:
        test_message()
    elif args.publish_new:
        asyncio.run(publish_new_offers())
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
