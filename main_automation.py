#!/usr/bin/env python3
"""
Camping Deals - Pipeline de Automatización Principal
Orquesta todo el flujo: scraping → base de datos → marketing → redes sociales
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar scraper mejorado si está disponible
try:
    from scraper.enhanced_scraper import MultiSourceScraper, AmazonScraper
    HAS_ENHANCED_SCRAPER = True
except ImportError:
    HAS_ENHANCED_SCRAPER = False

from scraper.amazon_scraper import FreeAmazonScraper
from database.supabase_client import FreeDatabase
from marketing.email_sender import FreeEmailMarketing
from social.social_poster import FreeSocialPoster
from analytics.dashboard import FreeDashboard, MonitoringSystem


class CampingDealsBot:
    """Bot principal de automatización - 100% gratuito"""
    
    def __init__(self, use_enhanced: bool = True):
        print("🏕️ Inicializando Camping Deals Bot...")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("-" * 50)

        # Usar scraper mejorado si está disponible
        if use_enhanced and HAS_ENHANCED_SCRAPER:
            print("✅ Usando Enhanced Multi-Source Scraper")
            self.multi_scraper = MultiSourceScraper(sources=['amazon'])
            self.scraper = None
        else:
            print("📌 Usando scraper básico")
            self.scraper = FreeAmazonScraper()
            self.multi_scraper = None

        self.db = FreeDatabase()
        self.email = FreeEmailMarketing()
        self.social = FreeSocialPoster()
        self.dashboard = FreeDashboard()
        self.monitor = MonitoringSystem()
    
    def run_complete_cycle(self, dry_run: bool = False) -> dict:
        """Ejecuta el ciclo completo de automatización"""
        results = {
            'deals_scraped': 0,
            'deals_stored': 0,
            'emails_sent': 0,
            'posts_published': 0,
            'errors': [],
        }
        
        try:
            # 1. Scrapear ofertas (Enhanced o básico)
            print("\n🔍 PASO 1: Scrapeando ofertas...")
            if self.multi_scraper:
                deal_objects = self.multi_scraper.scrape_all(max_pages=2)
                # Convertir a formato compatible
                deals = [d.to_supabase_format() for d in deal_objects]
            else:
                deals = self.scraper.scrape_all_categories()
            results['deals_scraped'] = len(deals)
            
            if not deals:
                print("⚠️ No se encontraron ofertas")
                return results
            
            # 2. Guardar en base de datos
            print("\n💾 PASO 2: Guardando en base de datos...")
            if not dry_run:
                results['deals_stored'] = self.db.insert_deals(deals)
            else:
                print("  (dry-run: no se guardó)")
            
            # 3. Actualizar JSON para GitHub Pages
            print("\n📄 PASO 3: Actualizando JSON para web...")
            if not dry_run:
                if self.multi_scraper:
                    self.multi_scraper.save_to_json(deal_objects, 'data/deals.json')
                else:
                    self.scraper.save_deals_json(deals, 'data/deals.json')
            
            # 4. Publicar en redes sociales (top 3 ofertas)
            print("\n📱 PASO 4: Publicando en redes sociales...")
            if not dry_run and self.social.telegram_enabled:
                results['posts_published'] = self.social.post_multiple_deals(
                    deals, 
                    max_posts=3, 
                    delay_seconds=30
                )
            
            # 5. Registrar métricas
            print("\n📊 PASO 5: Registrando métricas...")
            discounts = [d.get('discount', 0) for d in deals]
            metrics = {
                'deals_scraped': results['deals_scraped'],
                'deals_stored': results['deals_stored'],
                'telegram_posts': results['posts_published'],
                'avg_discount': round(sum(discounts) / len(discounts)) if discounts else 0,
                'max_discount': max(discounts) if discounts else 0,
            }
            
            if not dry_run:
                self.dashboard.track_daily_metrics(metrics)
            
        except Exception as e:
            error_msg = f"Error en ciclo: {str(e)}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            self.monitor.send_alert(error_msg)
        
        # Resumen
        print("\n" + "=" * 50)
        print("📊 RESUMEN DEL CICLO")
        print("=" * 50)
        print(f"  🔍 Ofertas scrapeadas: {results['deals_scraped']}")
        print(f"  💾 Ofertas guardadas: {results['deals_stored']}")
        print(f"  📱 Posts publicados: {results['posts_published']}")
        if results['errors']:
            print(f"  ❌ Errores: {len(results['errors'])}")
        print("=" * 50)
        
        return results
    
    def send_daily_newsletter(self) -> int:
        """Envía newsletter diario a suscriptores"""
        print("\n📧 Enviando newsletter diario...")
        
        # Obtener mejores ofertas
        deals = self.db.get_deals(min_discount=30, limit=10)
        
        if not deals:
            print("⚠️ No hay ofertas para enviar")
            return 0
        
        # Obtener lista de emails (desde Supabase o archivo local)
        email_list = self._get_subscriber_list()
        
        if not email_list:
            print("⚠️ No hay suscriptores")
            return 0
        
        return self.email.send_daily_deals(email_list, deals)
    
    def _get_subscriber_list(self) -> list:
        """Obtiene lista de suscriptores (placeholder)"""
        # En producción, esto vendría de Supabase
        subscribers_file = 'data/subscribers.json'
        
        try:
            with open(subscribers_file, 'r') as f:
                data = json.load(f)
                return data.get('emails', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def health_check(self) -> bool:
        """Verifica que todo el sistema funciona"""
        print("\n🔍 Verificando salud del sistema...")
        
        health = self.monitor.check_system_health()
        
        all_ok = all(health.values())
        
        for check, status in health.items():
            print(f"  {'✅' if status else '❌'} {check}")
        
        return all_ok


def main():
    parser = argparse.ArgumentParser(
        description='Camping Deals - Bot de Automatización 100% Gratis'
    )
    
    parser.add_argument(
        '--scrape', 
        action='store_true', 
        help='Ejecutar ciclo completo de scraping'
    )
    
    parser.add_argument(
        '--newsletter', 
        action='store_true', 
        help='Enviar newsletter diario'
    )
    
    parser.add_argument(
        '--health', 
        action='store_true', 
        help='Verificar salud del sistema'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Ejecutar sin guardar cambios'
    )
    
    parser.add_argument(
        '--all', 
        action='store_true', 
        help='Ejecutar todo: scrape + newsletter + health'
    )
    
    args = parser.parse_args()
    
    bot = CampingDealsBot()
    
    if args.all:
        bot.health_check()
        bot.run_complete_cycle(dry_run=args.dry_run)
        if not args.dry_run:
            bot.send_daily_newsletter()
    elif args.scrape:
        bot.run_complete_cycle(dry_run=args.dry_run)
    elif args.newsletter:
        bot.send_daily_newsletter()
    elif args.health:
        bot.health_check()
    else:
        # Por defecto, ejecutar ciclo de scraping
        bot.run_complete_cycle(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
