"""
TikTok Video Uploader usando tiktok-uploader library.
Crea un browser_agent propio para evitar el bug de ChromeDriver path
en webdriver-manager, y lo pasa a la librería.
"""
import os
import json
import tempfile


def _get_chrome_driver():
    """Crea un Chrome WebDriver con el path correcto del chromedriver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver_path = ChromeDriverManager().install()
    # Fix: webdriver-manager a veces devuelve path a THIRD_PARTY_NOTICES
    if "THIRD_PARTY" in driver_path:
        driver_path = driver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )
    os.chmod(driver_path, 0o755)

    return webdriver.Chrome(service=Service(driver_path), options=options)


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

            self.cookies_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.txt', delete=False
            )

            # Formato Netscape cookies.txt
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

                self.cookies_file.write(
                    f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n"
                )

            self.cookies_file.close()
            print(f"✅ Cookies preparadas: {len(cookies)} cookies cargadas")

        except Exception as e:
            print(f"❌ Error preparando cookies: {e}")
            self.cookies_file = None

    def upload_video(self, video_path, description):
        """Sube y publica un video a TikTok usando tiktok-uploader."""
        if not self.cookies_file:
            print("❌ No hay cookies configuradas.")
            return False

        try:
            from tiktok_uploader.upload import upload_video

            print(f"🚀 Subiendo video a TikTok: {video_path}")
            print(f"📝 Descripción: {description[:100]}...")

            # Crear browser con ChromeDriver path correcto
            driver = _get_chrome_driver()
            print("✅ Chrome browser creado correctamente.")

            # Pasar browser_agent para que la librería no cree su propio driver
            upload_video(
                filename=os.path.abspath(video_path),
                description=description,
                cookies=self.cookies_file.name,
                browser_agent=driver,
            )

            print("✅ Video publicado exitosamente en TikTok!")
            return True

        except ImportError:
            print("❌ tiktok-uploader no instalado.")
            return False

        except Exception as e:
            print(f"❌ Error subiendo video: {e}")
            import traceback
            traceback.print_exc()
            return False

    def close(self):
        """Limpia recursos."""
        if self.cookies_file and os.path.exists(self.cookies_file.name):
            try:
                os.unlink(self.cookies_file.name)
            except:
                pass
