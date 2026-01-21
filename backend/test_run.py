from main import job

print("🧪 Iniciando Test de Integración...")
try:
    job()
    print("✅ Test completado con éxito.")
except Exception as e:
    print(f"❌ Falló el test: {e}")
