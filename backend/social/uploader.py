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
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
    })

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
        {"source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'es', 'en']});
        """},
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
        time.sleep(3)

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
        time.sleep(8)

        current_url = driver.current_url
        print(f"📍 URL actual: {current_url}")

        if "login" in current_url:
            print("⚠️ Sesión no activa, reintentando...")
            driver.get("https://www.tiktok.com")
            time.sleep(3)
            driver.refresh()
            time.sleep(3)
            driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
            time.sleep(8)
            if "login" in driver.current_url:
                print("❌ Cookies expiradas. No se pudo iniciar sesión.")
                return False

        print("✅ Sesión verificada.")
        return True

    def _find_file_input(self, driver):
        """Busca el input de archivo, incluyendo dentro de iframes."""
        from selenium.webdriver.common.by import By

        # 1. Diagnóstico: listar la estructura de la página
        page_info = driver.execute_script("""
            let info = {
                url: window.location.href,
                title: document.title,
                iframes: [],
                fileInputs: [],
                allInputs: []
            };
            // Buscar iframes
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach((f, i) => {
                info.iframes.push({
                    index: i,
                    src: f.src || '(empty)',
                    id: f.id || '(none)',
                    name: f.name || '(none)'
                });
            });
            // Buscar file inputs en el main document
            const fileInputs = document.querySelectorAll('input[type="file"]');
            fileInputs.forEach((inp, i) => {
                info.fileInputs.push({
                    index: i,
                    name: inp.name || '(none)',
                    accept: inp.accept || '(none)',
                    id: inp.id || '(none)',
                    visible: inp.offsetParent !== null
                });
            });
            // Buscar todos los inputs
            const allInputs = document.querySelectorAll('input');
            allInputs.forEach((inp, i) => {
                info.allInputs.push({
                    index: i,
                    type: inp.type,
                    name: inp.name || '(none)',
                    id: inp.id || '(none)'
                });
            });
            return JSON.stringify(info);
        """)
        print(f"📊 Diagnóstico página: {page_info}")

        # 2. Intentar buscar file input en el documento principal
        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        if file_inputs:
            print(f"✅ Encontrado {len(file_inputs)} file input(s) en documento principal")
            return file_inputs[0]

        # 3. Buscar dentro de iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"🔍 Encontrados {len(iframes)} iframes. Buscando file input dentro...")

        for i, iframe in enumerate(iframes):
            try:
                iframe_src = iframe.get_attribute("src") or "(vacío)"
                print(f"  🔍 Iframe {i}: {iframe_src[:80]}")
                driver.switch_to.frame(iframe)
                file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                if file_inputs:
                    print(f"  ✅ File input encontrado en iframe {i}")
                    return file_inputs[0]
                driver.switch_to.default_content()
            except Exception as e:
                print(f"  ⚠️ Error en iframe {i}: {e}")
                driver.switch_to.default_content()

        # 4. Fallback: crear file input con JavaScript
        print("🔧 Creando file input via JavaScript...")
        driver.switch_to.default_content()
        driver.execute_script("""
            // Buscar cualquier zona de drop/upload
            const uploadArea = document.querySelector('[class*="upload"]') ||
                               document.querySelector('[class*="drop"]') ||
                               document.querySelector('[data-e2e*="upload"]');
            if (uploadArea) {
                console.log('Upload area found:', uploadArea.className);
            }
            // Crear input oculto y añadirlo
            let input = document.createElement('input');
            input.type = 'file';
            input.id = 'selenium_file_input';
            input.accept = 'video/*';
            input.style.position = 'fixed';
            input.style.top = '0';
            input.style.left = '0';
            input.style.opacity = '0.01';
            document.body.appendChild(input);
        """)
        time.sleep(1)

        file_inputs = driver.find_elements(By.ID, "selenium_file_input")
        if file_inputs:
            print("⚠️ Usando file input creado por JS (puede no funcionar)")
            return file_inputs[0]

        # 5. Último intento: buscar con JS dentro de shadow DOM
        result = driver.execute_script("""
            function findFileInput(root) {
                if (!root) return null;
                const inputs = root.querySelectorAll('input[type="file"]');
                if (inputs.length > 0) return inputs[0];
                // Buscar en shadow DOMs
                const allElements = root.querySelectorAll('*');
                for (const el of allElements) {
                    if (el.shadowRoot) {
                        const found = findFileInput(el.shadowRoot);
                        if (found) return found;
                    }
                }
                return null;
            }
            const input = findFileInput(document);
            if (input) {
                input.id = 'shadow_file_input';
                return true;
            }
            return false;
        """)
        if result:
            file_inputs = driver.find_elements(By.ID, "shadow_file_input")
            if file_inputs:
                print("✅ File input encontrado en Shadow DOM")
                return file_inputs[0]

        return None

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

            # Guardar screenshot de la página de upload
            driver.save_screenshot("/tmp/tiktok_upload_page.png")
            print(f"📸 Screenshot página upload: /tmp/tiktok_upload_page.png")
            print(f"📍 URL: {driver.current_url}")
            print(f"📄 Título: {driver.title}")

            # Buscar el input de archivo (con manejo de iframes)
            print("📤 Buscando input de archivo...")
            file_input = self._find_file_input(driver)

            if not file_input:
                # Intentar con la URL legacy de upload
                print("🔄 Intentando URL legacy: /creator#/upload")
                driver.switch_to.default_content()
                driver.get("https://www.tiktok.com/creator#/upload?lang=es")
                time.sleep(8)
                print(f"📍 URL legacy: {driver.current_url}")
                driver.save_screenshot("/tmp/tiktok_legacy_upload.png")
                file_input = self._find_file_input(driver)

            if not file_input:
                # Intentar URL /upload directa
                print("🔄 Intentando URL directa: /upload")
                driver.switch_to.default_content()
                driver.get("https://www.tiktok.com/upload?lang=es")
                time.sleep(8)
                print(f"📍 URL directa: {driver.current_url}")
                driver.save_screenshot("/tmp/tiktok_direct_upload.png")
                file_input = self._find_file_input(driver)

            if not file_input:
                print("❌ No se encontró input de archivo en ninguna URL.")
                # Dump del HTML para debug
                page_source = driver.page_source
                print(f"📄 HTML length: {len(page_source)}")
                # Buscar pistas en el HTML
                for keyword in ['file', 'upload', 'input', 'iframe', 'drop']:
                    count = page_source.lower().count(keyword)
                    print(f"   '{keyword}' aparece {count} veces en HTML")
                driver.quit()
                return False

            # Enviar el archivo
            file_input.send_keys(os.path.abspath(video_path))
            print("✅ Archivo enviado. Esperando procesamiento...")

            # Esperar a que se procese el video
            time.sleep(30)

            # Volver al contexto principal por si estábamos en un iframe
            try:
                driver.switch_to.default_content()
            except Exception:
                pass

            # Capturar screenshot para debug
            driver.save_screenshot("/tmp/tiktok_after_upload.png")
            print(f"📸 Screenshot post-upload: /tmp/tiktok_after_upload.png")
            print(f"📍 URL: {driver.current_url}")
            print(f"📄 Título: {driver.title}")

            # Intentar añadir descripción
            try:
                caption_selectors = [
                    "//div[@contenteditable='true']",
                    "//div[contains(@class,'notranslate')][@contenteditable='true']",
                    "//div[@data-placeholder][@contenteditable='true']",
                    "//span[@data-text='true']",
                    "//div[contains(@class,'public-DraftEditor-content')]",
                    "//div[@role='textbox']",
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
                    caption_el.send_keys(Keys.CONTROL + "a")
                    caption_el.send_keys(Keys.BACKSPACE)
                    time.sleep(0.5)
                    caption_el.send_keys(description)
                    print("✅ Descripción añadida.")
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
