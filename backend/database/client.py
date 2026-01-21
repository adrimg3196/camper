import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SupabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseManager, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance
    
    def _init_client(self):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        
        if not self.url or not self.key:
            print("⚠️ ADVERTENCIA: Credenciales Supabase no encontradas.")
            print("   -> Modo SIMULACIÓN activado.")
            self.enabled = False
        else:
            self.enabled = True
            self.headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            print("✅ Cliente Supabase (REST) configurado.")

    def save_deal(self, deal_data: dict):
        """Guarda oferta vía REST API."""
        if self.enabled:
            try:
                endpoint = f"{self.url}/rest/v1/deals"
                response = requests.post(endpoint, headers=self.headers, json=deal_data)
                
                if response.status_code in [200, 201, 204]:
                    print(f"💾 Oferta guardada en DB: {deal_data.get('title')}")
                else:
                    print(f"❌ Error Supabase {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error conexión Supabase: {e}")
        else:
            print(f"🔧 [SIMULACIÓN DB] Guardando oferta: {deal_data.get('title')}")
            return deal_data
