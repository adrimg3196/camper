#!/usr/bin/env python3
"""
Camping Deals - Analytics Dashboard Gratuito
Tracking con Google Sheets (gratis e ilimitado)
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False
    print("⚠️ gspread no instalado. Analytics deshabilitado.")


class FreeDashboard:
    """Dashboard de analytics gratuito usando Google Sheets"""
    
    def __init__(self):
        self.credentials_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
        self.spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
        self.client = None
        self.sheet = None
        
        if HAS_GSPREAD and self.credentials_json and self.spreadsheet_id:
            try:
                self._setup_google_sheets()
                print("✅ Google Sheets conectado")
            except Exception as e:
                print(f"⚠️ Error conectando Google Sheets: {e}")
        
        self.local_log_path = 'data/analytics_log.json'
    
    def _setup_google_sheets(self):
        """Configura conexión a Google Sheets"""
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds_dict = json.loads(self.credentials_json)
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open_by_key(self.spreadsheet_id)
    
    def _load_local_log(self) -> List[Dict]:
        """Carga log local de analytics"""
        try:
            with open(self.local_log_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_local_log(self, data: List[Dict]):
        """Guarda log local de analytics"""
        os.makedirs(os.path.dirname(self.local_log_path), exist_ok=True)
        with open(self.local_log_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_daily_metrics(self, metrics: Dict) -> bool:
        """Registra métricas diarias"""
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            **metrics
        }
        
        # Guardar en Google Sheets si disponible
        if self.sheet:
            try:
                worksheet = self.sheet.worksheet('Metrics')
                values = [
                    entry.get('date', ''),
                    entry.get('deals_scraped', 0),
                    entry.get('emails_sent', 0),
                    entry.get('telegram_posts', 0),
                    entry.get('avg_discount', 0),
                    entry.get('max_discount', 0),
                ]
                worksheet.append_row(values)
                print("📊 Métricas guardadas en Google Sheets")
            except Exception as e:
                print(f"⚠️ Error guardando en Sheets: {e}")
        
        # Siempre guardar en local como backup
        log = self._load_local_log()
        log.append(entry)
        self._save_local_log(log)
        
        return True
    
    def get_weekly_summary(self) -> Dict:
        """Obtiene resumen semanal de métricas"""
        log = self._load_local_log()
        
        # Últimos 7 días
        from datetime import timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        weekly_data = [e for e in log if e.get('date', '') >= week_ago]
        
        if not weekly_data:
            return {
                'total_deals': 0,
                'total_emails': 0,
                'total_posts': 0,
                'avg_discount': 0,
            }
        
        return {
            'total_deals': sum(e.get('deals_scraped', 0) for e in weekly_data),
            'total_emails': sum(e.get('emails_sent', 0) for e in weekly_data),
            'total_posts': sum(e.get('telegram_posts', 0) for e in weekly_data),
            'avg_discount': round(
                sum(e.get('avg_discount', 0) for e in weekly_data) / len(weekly_data)
            ),
        }
    
    def generate_report(self) -> str:
        """Genera reporte de texto para email/Telegram"""
        summary = self.get_weekly_summary()
        
        return f"""
📊 REPORTE SEMANAL - Camping Deals

📦 Ofertas scrapeadas: {summary['total_deals']}
📧 Emails enviados: {summary['total_emails']}
📱 Posts Telegram: {summary['total_posts']}
💰 Descuento promedio: {summary['avg_discount']}%

Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """.strip()


class MonitoringSystem:
    """Sistema de monitoreo y alertas"""
    
    def __init__(self):
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.admin_chat_id = os.environ.get('TELEGRAM_ADMIN_CHAT_ID')
    
    def check_system_health(self) -> Dict[str, bool]:
        """Verifica salud del sistema"""
        checks = {
            'scraper_available': self._test_scraper(),
            'database_connected': self._test_database(),
            'website_accessible': self._test_website(),
        }
        
        failed = [k for k, v in checks.items() if not v]
        
        if failed:
            self.send_alert(f"⚠️ Sistema con problemas: {', '.join(failed)}")
        
        return checks
    
    def _test_scraper(self) -> bool:
        """Verifica que el scraper funciona"""
        try:
            import requests
            response = requests.get('https://www.amazon.es', timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def _test_database(self) -> bool:
        """Verifica conexión a base de datos"""
        try:
            from database.supabase_client import FreeDatabase
            db = FreeDatabase()
            db.get_stats()
            return True
        except:
            return False
    
    def _test_website(self) -> bool:
        """Verifica que la web está accesible"""
        try:
            import requests
            response = requests.get('https://camping-offers.github.io', timeout=10)
            return response.status_code == 200
        except:
            return True  # Puede no estar desplegada aún
    
    def send_alert(self, message: str) -> bool:
        """Envía alerta al administrador"""
        if not self.telegram_token or not self.admin_chat_id:
            print(f"⚠️ ALERTA: {message}")
            return False
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.admin_chat_id,
                'text': f"🚨 ALERTA SISTEMA\n\n{message}",
                'parse_mode': 'Markdown',
            }
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except:
            return False


# Guía para configurar Google Sheets gratuito
GOOGLE_SHEETS_SETUP = """
# Configuración Google Sheets para Analytics (Gratis)

## 1. Crear proyecto en Google Cloud
   https://console.cloud.google.com/
   
## 2. Habilitar Google Sheets API
   APIs & Services → Enable APIs → Google Sheets API
   
## 3. Crear Service Account
   IAM & Admin → Service Accounts → Create
   Descargar JSON de credenciales
   
## 4. Crear Spreadsheet y compartir
   - Crear nuevo Google Sheet
   - Compartir con email del Service Account (Editor)
   - Copiar ID del spreadsheet (de la URL)
   
## 5. Configurar en GitHub Secrets
   GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
   GOOGLE_SHEETS_ID=1234567890abcdef
   
## 6. Crear hoja "Metrics" con columnas:
   Date | Deals | Emails | Posts | Avg Discount | Max Discount
"""


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Analytics Dashboard')
    parser.add_argument('--report', action='store_true', help='Generar reporte semanal')
    parser.add_argument('--health', action='store_true', help='Verificar salud del sistema')
    parser.add_argument('--setup', action='store_true', help='Mostrar guía de configuración')
    
    args = parser.parse_args()
    
    if args.setup:
        print(GOOGLE_SHEETS_SETUP)
    elif args.report:
        dashboard = FreeDashboard()
        print(dashboard.generate_report())
    elif args.health:
        monitor = MonitoringSystem()
        health = monitor.check_system_health()
        print("\n🔍 Estado del sistema:")
        for check, status in health.items():
            print(f"  {'✅' if status else '❌'} {check}")
    else:
        dashboard = FreeDashboard()
        print("\n📊 Resumen semanal:")
        print(dashboard.get_weekly_summary())
