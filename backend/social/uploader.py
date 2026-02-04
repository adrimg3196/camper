"""
TikTok Video Uploader - Selenium directo.
La librería tiktok-uploader no funciona con la UI actual de TikTok,
así que usamos Selenium directamente con selectores actualizados.
"""
import os
import json
import time


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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver_path = ChromeDriverManager().install()
    if "THIRD_PARTY" in driver_path:
        driver_path = driver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )
    os.chmod(driver_path, 0o755)

    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    # Anti-detección: eliminar navigator.webdriver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )
    return driver


class TikTokUploader:
    def __init__(self):
        self.driver = None

    def _inject_cookies(self, driver):
        """Inyecta cookies de TikTok desde variable de entorno."""
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("⚠️ No hay TIKTOK_COOKIES_JSON configurado.")
            return False

        driver.get("https://www.tiktok.com")
        time.sleep(2)

        cookies = json.loads(cookies_json)
        injected = 0
        for cookie in cookies:
            if 'sameSite' in cookie:
                if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                    cookie['sameSite'] = "Lax"
            if 'expirationDate' in cookie:
                cookie['expiry'] = int(cookie.pop('expirationDate'))
            for key in ['hostOnly', 'httpOnly', 'session', 'storeId', 'id']:
                cookie.pop(key, None)
            try:
                driver.add_cookie(cookie)
                injected += 1
            except Exception:
                pass

        print(f"🍪 {injected}/{len(cookies)} cookies inyectadas.")
        driver.refresh()
        time.sleep(3)
        return True

    def _verify_session(self, driver):
        """Verifica que la sesión está activa."""
        driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
        time.sleep(5)

        current_url = driver.current_url
        print(f"📍 URL actual: {current_url}")

        if "login" in current_url:
            print("⚠️ Sesión no activa, reintentando...")
            driver.get("https://www.tiktok.com")
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
            driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
            time.sleep(5)
            if "login" in driver.current_url:
                print("❌ Cookies expiradas. No se pudo iniciar sesión.")
                return False

        print("✅ Sesión verificada.")
        return True

    def upload_video(self, video_path, description):
        """Sube y publica un video a TikTok usando Selenium."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys

        print(f"🚀 Subiendo video a TikTok: {video_path}")
        print(f"📝 Descripción: {description[:100]}...")

        try:
            driver = _get_chrome_driver()
            print("✅ Chrome browser creado.")

            # Inyectar cookies y verificar sesión
            if not self._inject_cookies(driver):
                driver.quit()
                return False

            if not self._verify_session(driver):
                driver.quit()
                return False

            # Buscar el input de archivo (puede estar oculto)
            print("📤 Buscando input de archivo...")
            file_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(os.path.abspath(video_path))
            print("✅ Archivo enviado. Esperando procesamiento...")

            # Esperar a que se procese el video (30s)
            time.sleep(30)

            # Capturar screenshot para debug
            driver.save_screenshot("/tmp/tiktok_after_upload.png")
            print(f"📸 Screenshot guardado en /tmp/tiktok_after_upload.png")
            print(f"📍 URL: {driver.current_url}")
            print(f"📄 Título: {driver.title}")

            # Intentar añadir descripción
            try:
                caption_selectors = [
                    "//div[@contenteditable='true']",
                    "//div[contains(@class,'notranslate')][@contenteditable='true']",
                    "//div[@data-placeholder][@contenteditable='true']",
                    "//span[@data-text='true']",
                ]
                caption_el = None
                for sel in caption_selectors:
                    try:
                        caption_el = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, sel))
                        )
                        if caption_el:
                            break
                    except Exception:
                        continue

                if caption_el:
                    caption_el.click()
                    time.sleep(0.5)
                    # Seleccionar todo y borrar
                    caption_el.send_keys(Keys.CONTROL + "a")
                    caption_el.send_keys(Keys.BACKSPACE)
                    time.sleep(0.5)
                    caption_el.send_keys(description)
                    print(f"✅ Descripción añadida.")
                else:
                    print("⚠️ No se encontró campo de descripción.")
            except Exception as e:
                print(f"⚠️ Error en descripción: {e}")

            # Intentar hacer clic en Publicar
            print("🔍 Buscando botón Publicar...")
            publish_selectors = [
                "//button[@data-e2e='post_video_button']",
                "//button[contains(text(),'Publicar')]",
                "//button[contains(text(),'Post')]",
                "//button[contains(text(),'Subir')]",
                "//div[contains(@class,'btn-post')]//button",
                "//button[contains(@class,'TUXButton--primary') and contains(@class,'TUXButton--large')]",
            ]

            published = False
            for sel in publish_selectors:
                try:
                    btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                    btn.click()
                    print(f"✅ Botón Publicar clickeado: {sel}")
                    published = True
                    break
                except Exception:
                    continue

            if not published:
                # Fallback: buscar botones por JavaScript
                print("🔍 Buscando botón por JavaScript...")
                result = driver.execute_script("""
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        const text = btn.textContent.toLowerCase();
                        if (text.includes('publicar') || text.includes('post') ||
                            text.includes('subir') || text.includes('upload')) {
                            btn.click();
                            return 'clicked: ' + btn.textContent.trim();
                        }
                    }
                    // Listar todos los botones para debug
                    return 'buttons: ' + Array.from(buttons).map(b => b.textContent.trim()).filter(t => t).join(' | ');
                """)
                print(f"🔍 JS resultado: {result}")
                if result and result.startswith('clicked'):
                    published = True

            # Esperar confirmación
            if published:
                time.sleep(10)
                driver.save_screenshot("/tmp/tiktok_after_publish.png")
                print("✅ Video publicado exitosamente en TikTok!")
            else:
                driver.save_screenshot("/tmp/tiktok_no_publish_btn.png")
                print("⚠️ No se encontró botón Publicar. Video subido como borrador.")

            driver.quit()
            return published

        except Exception as e:
            print(f"❌ Error subiendo video: {e}")
            import traceback
            traceback.print_exc()
            try:
                driver.quit()
            except Exception:
                pass
            return False

    def close(self):
        """Limpia recursos."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
