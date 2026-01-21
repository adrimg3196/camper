
import sys
import os
import json
import time

# Añadir root al path para importar backend
sys.path.append(os.getcwd())

from backend.social.uploader import TikTokUploader

def main():
    print("🍪 iniciando Extractor de Cookies...")
    print("   -> Abriendo navegador con tu perfil persistente...")
    
    try:
        uploader = TikTokUploader()
        uploader.start_browser()
        
        print("🚀 Navegando a TikTok...")
        uploader.driver.get("https://www.tiktok.com")
        
        # Esperar un poco para que carguen cookies o el usuario se loguee
        print("⏳ Esperando 20 segundos para asegurar que la sesión carga...")
        print("   (Si no estás logueado, hazlo AHORA en la ventana que se ha abierto)")
        time.sleep(20)
        
        cookies = uploader.driver.get_cookies()
        
        # Filtrar o limpiar si es necesario, pero GitHub suele aceptar todo el JSON
        output_path = "tiktok_cookies.json"
        
        with open(output_path, "w") as f:
            json.dump(cookies, f, indent=2)
            
        print(f"✅ ¡ÉXITO! Cookies extraídas.")
        print(f"📄 Guardadas en: {os.path.abspath(output_path)}")
        
        uploader.driver.quit()
        
    except Exception as e:
        print(f"❌ Error extrayendo cookies: {e}")

if __name__ == "__main__":
    main()
