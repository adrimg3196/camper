#!/usr/bin/env python3
"""
Camping Deals - Social Media Poster
Publicación automática en Telegram + IFTTT (TikTok, Instagram)
"""

import os
import requests
import time
from typing import List, Dict, Optional
from datetime import datetime


class FreeSocialPoster:
    """Publicador automático en redes sociales (100% gratis)"""
    
    def __init__(self):
        # Telegram
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_channel = os.environ.get('TELEGRAM_CHANNEL_ID', '@campingdeals')
        
        # IFTTT Webhooks (para TikTok, Instagram, etc.)
        self.ifttt_key = os.environ.get('IFTTT_KEY')
        
        self.telegram_enabled = bool(self.telegram_token)
        self.ifttt_enabled = bool(self.ifttt_key)
        
        if self.telegram_enabled:
            print("✅ Telegram configurado")
        if self.ifttt_enabled:
            print("✅ IFTTT configurado")
    
    def post_to_telegram(self, deal: Dict, send_photo: bool = True) -> bool:
        """Publica una oferta en el canal de Telegram"""
        if not self.telegram_enabled:
            print("⚠️ Telegram no configurado")
            return False
        
        message = self._format_telegram_message(deal)
        
        try:
            if send_photo and deal.get('image_url'):
                return self._send_telegram_photo(deal['image_url'], message)
            else:
                return self._send_telegram_text(message)
        except Exception as e:
            print(f"❌ Error Telegram: {e}")
            return False
    
    def _format_telegram_message(self, deal: Dict) -> str:
        """Formatea el mensaje para Telegram"""
        savings = deal.get('original_price', 0) - deal.get('current_price', 0)
        
        # Emojis por categoría
        category_emojis = {
            'tiendas-campana': '⛺',
            'sacos-dormir': '🛏️',
            'mochilas': '🎒',
            'cocina-camping': '🍳',
            'iluminacion': '🔦',
            'mobiliario': '🪑',
            'herramientas': '🔧',
            'accesorios': '🧭',
        }
        
        emoji = category_emojis.get(deal.get('category', ''), '🏕️')
        
        # Rating estrellas
        rating = deal.get('rating', 0)
        stars = '⭐' * int(rating) if rating else ''
        
        message = f"""
{emoji} *¡OFERTA CAMPING!* {emoji}

📦 {deal.get('title', '')[:100]}

💰 *Precio:* ~€{deal.get('original_price', 0):.2f}~ → *€{deal.get('current_price', 0):.2f}*
📉 *Descuento:* -{deal.get('discount', 0)}%
💵 *Ahorras:* €{savings:.2f}
{f"⭐ *Valoración:* {stars} ({rating}/5)" if rating else ""}
{"✅ *Amazon Prime*" if deal.get('is_prime') else ""}

👉 [Ver en Amazon]({deal.get('affiliate_url', '#')})

_Enlace de afiliado. Precio actualizado: {datetime.now().strftime('%d/%m %H:%M')}_

#camping #ofertas #outdoor #amazon #descuentos
        """
        
        return message.strip()
    
    def _send_telegram_text(self, text: str) -> bool:
        """Envía mensaje de texto a Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        
        data = {
            'chat_id': self.telegram_channel,
            'text': text,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': False,
        }
        
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    
    def _send_telegram_photo(self, photo_url: str, caption: str) -> bool:
        """Envía foto con caption a Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
        
        data = {
            'chat_id': self.telegram_channel,
            'photo': photo_url,
            'caption': caption[:1024],  # Límite de caracteres
            'parse_mode': 'Markdown',
        }
        
        response = requests.post(url, json=data, timeout=15)
        return response.status_code == 200
    
    def trigger_ifttt_webhook(self, deal: Dict, event_name: str = 'camping_deal') -> bool:
        """Activa webhook IFTTT para automatizar otras plataformas"""
        if not self.ifttt_enabled:
            print("⚠️ IFTTT no configurado")
            return False
        
        url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{self.ifttt_key}"
        
        # IFTTT permite 3 valores
        data = {
            'value1': deal.get('title', '')[:200],
            'value2': f"€{deal.get('current_price', 0):.2f} (-{deal.get('discount', 0)}%)",
            'value3': deal.get('affiliate_url', ''),
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error IFTTT: {e}")
            return False
    
    def post_multiple_deals(self, deals: List[Dict], max_posts: int = 3, delay_seconds: int = 60) -> int:
        """Publica múltiples ofertas con delay entre ellas"""
        posted = 0
        
        # Ordenar por descuento
        sorted_deals = sorted(deals, key=lambda x: x.get('discount', 0), reverse=True)
        
        for i, deal in enumerate(sorted_deals[:max_posts]):
            print(f"\n📤 Publicando oferta {i+1}/{max_posts}...")
            
            # Telegram
            if self.post_to_telegram(deal):
                print(f"  ✅ Telegram: {deal.get('title', '')[:40]}...")
                posted += 1
            
            # IFTTT (para Instagram/TikTok)
            if self.trigger_ifttt_webhook(deal):
                print(f"  ✅ IFTTT webhook activado")
            
            # Delay para evitar rate limiting y spam
            if i < max_posts - 1:
                print(f"  ⏳ Esperando {delay_seconds}s...")
                time.sleep(delay_seconds)
        
        return posted
    
    def send_daily_summary(self, deals_count: int, top_discount: int) -> bool:
        """Envía resumen diario al canal"""
        if not self.telegram_enabled:
            return False
        
        message = f"""
📊 *Resumen del Día* 📊

🔢 *Ofertas activas:* {deals_count}
🔥 *Mayor descuento:* {top_discount}%
🏕️ *Categorías:* Tiendas, Sacos, Mochilas y más

👉 [Ver todas las ofertas](https://camping-offers.github.io)

_Actualizado {datetime.now().strftime('%d/%m/%Y %H:%M')}_
        """
        
        return self._send_telegram_text(message.strip())


# Configuración IFTTT recomendada:
IFTTT_SETUP_GUIDE = """
# Configuración IFTTT para automatizar redes sociales

## 1. Crear cuenta en IFTTT (gratis)
   https://ifttt.com/join

## 2. Crear Applet: Webhook → Twitter/Instagram
   - Trigger: Webhooks "Receive a web request"
   - Event Name: camping_deal
   - Action: Twitter "Post a tweet" o Instagram "Post a photo"
   
## 3. Obtener tu clave webhook
   https://ifttt.com/maker_webhooks
   Clic en "Documentation" para ver tu clave
   
## 4. Guardar en GitHub Secrets
   IFTTT_KEY=tu_clave_aqui
   
## Applets recomendados (gratis):
   - Webhook → Twitter (tweet automático)
   - Webhook → Telegram (backup)
   - Webhook → Email (notificación personal)
"""


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Poster')
    parser.add_argument('--test', action='store_true', help='Mostrar mensaje de prueba')
    parser.add_argument('--setup', action='store_true', help='Mostrar guía de configuración')
    
    args = parser.parse_args()
    
    if args.setup:
        print(IFTTT_SETUP_GUIDE)
    elif args.test:
        poster = FreeSocialPoster()
        test_deal = {
            'title': 'Tienda de Campaña TEST - 4 Personas Impermeable',
            'current_price': 99.99,
            'original_price': 199.99,
            'discount': 50,
            'category': 'tiendas-campana',
            'rating': 4.5,
            'is_prime': True,
            'affiliate_url': 'https://amazon.es',
            'image_url': 'https://via.placeholder.com/300',
        }
        print("\n--- MENSAJE DE PRUEBA ---")
        print(poster._format_telegram_message(test_deal))
    else:
        poster = FreeSocialPoster()
        print(f"\nTelegram enabled: {poster.telegram_enabled}")
        print(f"IFTTT enabled: {poster.ifttt_enabled}")
