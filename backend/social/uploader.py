"""
TikTok Video Uploader usando tiktok-uploader library
Esta librería tiene bypass anti-bot integrado y funciona con cookies exportadas.
"""
import os
import json
import tempfile


class TikTokUploader:
    def __init__(self):
        self.cookies_file = None
        self._setup_cookies()

    def _setup_cookies(self):
        """Prepara el archivo de cookies desde la variable de entorno."""
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("⚠️ No hay TIKTOK_COOKIES_JSON configurado.")
            return

        try:
            cookies = json.loads(cookies_json)

            # Crear archivo temporal con las cookies en formato Netscape
            self.cookies_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False
            )

            # Escribir en formato Netscape cookies.txt
            self.cookies_file.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                domain = cookie.get('domain', '.tiktok.com')
                if not domain.startswith('.'):
                    domain = '.' + domain

                flag = "TRUE" if domain.startswith('.') else "FALSE"
                path = cookie.get('path', '/')
                secure = "TRUE" if cookie.get('secure', False) else "FALSE"
                expiry = str(int(cookie.get('expirationDate', 0)))
                name = cookie.get('name', '')
                value = cookie.get('value', '')

                line = f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n"
                self.cookies_file.write(line)

            self.cookies_file.close()
            print(f"✅ Cookies preparadas: {len(cookies)} cookies cargadas")

        except Exception as e:
            print(f"❌ Error preparando cookies: {e}")
            self.cookies_file = None

    def upload_video(self, video_path, description):
        """
        Sube un video a TikTok usando tiktok-uploader library.
        Esta librería tiene bypass anti-bot integrado.
        """
        if not self.cookies_file:
            print("❌ No hay cookies configuradas. Configura TIKTOK_COOKIES_JSON.")
            return False

        try:
            # Importar la librería aquí para evitar errores si no está instalada
            from tiktok_uploader.upload import upload_video

            print(f"🚀 Subiendo video a TikTok: {video_path}")
            print(f"📝 Descripción: {description[:100]}...")

            # La librería maneja todo: bypass anti-bot, login con cookies, upload y publicación
            upload_video(
                filename=os.path.abspath(video_path),
                description=description,
                cookies=self.cookies_file.name,
                headless=True,  # Modo headless para CI
                # browser='chrome'  # Por defecto usa Chrome
            )

            print("✅ Video publicado exitosamente en TikTok!")
            return True

        except ImportError:
            print("❌ tiktok-uploader no está instalado. Ejecuta: pip install tiktok-uploader")
            return self._fallback_upload(video_path, description)

        except Exception as e:
            print(f"❌ Error subiendo video: {e}")
            # Intentar método fallback
            return self._fallback_upload(video_path, description)

    def _fallback_upload(self, video_path, description):
        """
        Método fallback usando Selenium directo si tiktok-uploader falla.
        Solo sube el video, no publica automáticamente.
        """
        print("🔄 Intentando método fallback con Selenium...")

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            import time

            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

            driver_path = ChromeDriverManager().install()
            if "THIRD_PARTY" in driver_path:
                driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
            os.chmod(driver_path, 0o755)

            driver = webdriver.Chrome(service=Service(driver_path), options=options)

            # Inyectar cookies
            driver.get("https://www.tiktok.com")
            cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
            if cookies_json:
                cookies = json.loads(cookies_json)
                for cookie in cookies:
                    if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                        del cookie['sameSite']
                    try:
                        driver.add_cookie(cookie)
                    except:
                        pass

            driver.refresh()
            time.sleep(3)

            # Ir a upload
            driver.get("https://www.tiktok.com/upload?lang=es")
            time.sleep(5)

            # Subir archivo
            file_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(os.path.abspath(video_path))

            print("⏳ Esperando procesamiento (20s)...")
            time.sleep(20)

            print("✅ Video subido (fallback). Requiere publicación manual.")
            driver.quit()
            return True

        except Exception as e:
            print(f"❌ Fallback también falló: {e}")
            return False

    def close(self):
        """Limpia recursos."""
        if self.cookies_file and os.path.exists(self.cookies_file.name):
            try:
                os.unlink(self.cookies_file.name)
            except:
                pass


if __name__ == "__main__":
    # Test rápido
    uploader = TikTokUploader()

    # Crear un video dummy para probar
    test_video = "test_video.mp4"
    if not os.path.exists(test_video):
        print("⚠️ No hay video de prueba. Crea test_video.mp4")
    else:
        uploader.upload_video(test_video, "Test automatizado #camping #ofertas")

    uploader.close()
