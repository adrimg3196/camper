import os
import requests
from dotenv import load_dotenv

# Cargar .env desde backend
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    print("❌ Error: No se encontraron las credenciales en backend/.env")
    exit(1)

print(f"🔧 Conectando a {URL}...")

# Intentamos usar la API REST para 'rpc' (Remote Procedure Call) si existiera, 
# pero para DDL (Create/Alter) necesitamos SQL Editor o Service Role.
# Sin embargo, vamos a intentar un truco: Si no podemos alterar la tabla,
# podemos asegurarnos que el cliente Python maneje la falta de columna sin crashear,
# O (mejor) le pedimos al usuario que corra esto en el Dashboard SQL Editor.

sql_query = "ALTER TABLE deals ADD COLUMN IF NOT EXISTS asin text;"

print("\n⚠️  ATENCIÓN AUTOMÁTICA NO POSIBLE VÍA REST PÚBLICO ⚠️")
print("Supabase no permite alterar tablas vía API REST estándar por seguridad.")
print("\nPor favor, ve a tu Dashboard de Supabase -> SQL Editor y ejecuta:")
print("-" * 50)
print(sql_query)
print("-" * 50)
print("\nAlternativamente, si tienes la 'service_role' key (empieza por eyJ...), ponla en el .env temporalmente.")
