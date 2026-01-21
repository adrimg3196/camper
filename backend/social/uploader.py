import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TikTokUploader:
    def __init__(self):
        self.driver = None

    def start_browser(self):
        """Inicia un navegador Chrome controlado por Selenium."""
        options = webdriver.ChromeOptions()
        
        # Detectar entorno CI/CD (GitHub Actions)
        is_ci = os.environ.get("CI") == "true"
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        
        if is_ci:
            print("🤖 Entorno CI detectado: Ejecutando en modo HEADLESS.")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            # En CI no usamos perfil persistente local, usaremos cookies inyectadas
        else:
            options.add_argument("--start-maximized")
            # Mantener sesión iniciada (Solo local)
            profile_path = os.path.join(os.getcwd(), "backend", "tiktok_profile")
            # Limpiar lock si existe
            lock_file = os.path.join(profile_path, "SingletonLock")
            if os.path.exists(lock_file):
                try: os.remove(lock_file)
                except: pass
            options.add_argument(f"user-data-dir={profile_path}")

        driver_path = ChromeDriverManager().install()
        # Fix mac-arm64
        if "THIRD_PARTY" in driver_path:
             driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")

        # Asegurar permisos
        os.chmod(driver_path, 0o755)

        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        
        # Inyectar cookies si estamos en CI
        if is_ci:
            self._inject_cookies()

    def _inject_cookies(self):
        """Inyecta cookies desde variable de entorno para mantener sesión en CI."""
        import json
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("⚠️ CI detectado pero no hay TIKTOK_COOKIES_JSON. El login fallará.")
            return

        print("🍪 Inyectando cookies de sesión...")
        try:
            # Necesitamos ir al dominio antes de poner cookies
            self.driver.get("https://www.tiktok.com")
            
            cookies = json.loads(cookies_json)
            for cookie in cookies:
                # Selenium exige ciertos campos, y rechaza 'sameSite' a veces si no es estricto
                if 'sameSite' in cookie:
                    if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                        del cookie['sameSite']
                
                # Asegurar dominio correcto (a veces exportan .tiktok.com)
                if 'domain' in cookie:
                     # Solo permitir cookies del dominio actual o subdominios validos
                     pass
                
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    # Ignorar errores de cookies individuales (a veces hay basura)
                    pass
            
            print(f"✅ {len(cookies)} cookies inyectadas. Refrescando...")
            self.driver.refresh()
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error inyectando cookies: {e}")

    def upload_video(self, video_path, description):
        """Sube un video a TikTok."""
        if not self.driver:
            self.start_browser()

        print("🚀 Abriendo TikTok para subir video...")
        self.driver.get("https://www.tiktok.com/upload?lang=es")

        # 1. Verificar Login
        print("👀 Verificando sesión...")
        time.sleep(5) 
        
        if "login" in self.driver.current_url:
            print("⚠️ NO LOGUEADO.")
            # Si estamos en CI, esto es fatal
            if os.environ.get("CI") == "true":
                print("❌ Error fatal en CI: Las cookies han expirado o son inválidas.")
                return False
                
            print("⏳ Esperando 60 segundos para login manual (Entorno Local)...")
            try:
                WebDriverWait(self.driver, 60).until(
                    lambda d: "upload" in d.current_url and "login" not in d.current_url
                )
                print("✅ Login detectado. Continuando...")
            except:
                print("❌ No se detectó el login a tiempo. Abortando.")
                return False

        # 2. Subir Archivo
        try:
            print(f"📤 Subiendo archivo: {video_path}")
            # Encontrar el input file oculto
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(video_path))
            
            # Esperar a que se procese (aparece barra de carga o cambio de UI)
            print("⏳ Esperando procesamiento de video (15s)...")
            time.sleep(15) 
            
            # 3. Poner Descripción
            # Nota: Los selectores de TikTok cambian mucho. Intentamos buscar el editor de texto.
            # Una estrategia robusta es esperar e inyectar el texto o buscar el div contenteditable
            
            # caption_input = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']")
            # caption_input.send_keys(description)
            # print("✍️ Descripción añadida.")
            
            print("⚠️ La descripción automática es compleja por los selectores dinámicos. Se ha subido el video, añade la descripción y pulsa Publicar manualmente por ahora para evitar baneos.")

            # 4. Publicar (Opcional - Riesgo de bloqueo si es muy rápido)
            # post_button = self.driver.find_element(By.XPATH, "//button[text()='Publicar']")
            # post_button.click()
            
            print("👋 El video se ha subido. Por favor, pulsa 'Publicar' manualmente en la ventana del navegador. El bot continuará el ciclo en segundo plano.")
            
            return True

        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
            
    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    # Test rápido
    uploader = TikTokUploader()
    # Crear un archivo dummy para probar si no existe
    if not os.path.exists("test_video.mp4"):
        with open("test_video.mp4", "w") as f:
            f.write("dummy content")
            
    uploader.upload_video("test_video.mp4", "Test #automatización")
    uploader.close()
