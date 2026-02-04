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
            print("No hay TIKTOK_COOKIES_JSON configurado.")
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

        print(f"[COOKIES] {injected}/{len(cookies)} cookies inyectadas.")
        driver.refresh()
        time.sleep(3)
        return True

    def _verify_session(self, driver):
        """Verifica que la sesion esta activa comprobando username."""
        # Primero ir a tiktok.com y verificar login
        driver.get("https://www.tiktok.com")
        time.sleep(5)

        # Verificar si estamos logueados buscando indicadores
        login_check = driver.execute_script("""
            // Buscar cookie de sesion
            const cookies = document.cookie;
            const hasSid = cookies.includes('sid_tt') || cookies.includes('sessionid');
            // Buscar avatar o menu de usuario
            const avatar = document.querySelector('[data-e2e="profile-icon"]') ||
                           document.querySelector('img[alt*="avatar"]') ||
                           document.querySelector('[class*="avatar"]');
            return {
                hasSidCookie: hasSid,
                hasAvatar: !!avatar,
                cookies: cookies.substring(0, 200),
                url: window.location.href
            };
        """)
        print(f"[SESSION] Check: sid={login_check.get('hasSidCookie')}, avatar={login_check.get('hasAvatar')}, url={login_check.get('url')}")

        # Ahora navegar a TikTok Studio
        driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
        time.sleep(8)

        current_url = driver.current_url
        print(f"[SESSION] URL actual: {current_url}")

        if "login" in current_url:
            print("[SESSION] Redirigido a login. Reintentando...")
            driver.get("https://www.tiktok.com")
            time.sleep(3)
            driver.refresh()
            time.sleep(3)
            driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
            time.sleep(8)
            current_url = driver.current_url
            print(f"[SESSION] URL tras reintento: {current_url}")
            if "login" in current_url:
                print("[SESSION] FALLO: Cookies expiradas.")
                return False

        print("[SESSION] OK - En TikTok Studio")
        return True

    def _dismiss_overlays(self, driver):
        """Cierra overlays de tutorial (react-joyride) y popups modales."""
        try:
            result = driver.execute_script("""
                let dismissed = [];
                // Cerrar react-joyride
                document.querySelectorAll('[class*="react-joyride"]').forEach(el => {
                    el.remove();
                    dismissed.push('joyride-removed');
                });
                // Cerrar overlays
                document.querySelectorAll('.react-joyride__overlay').forEach(el => {
                    el.remove();
                    dismissed.push('overlay-removed');
                });
                // Clickear botones de dismiss
                document.querySelectorAll('button').forEach(btn => {
                    const t = btn.textContent.toLowerCase().trim();
                    if (['skip', 'got it', 'close', 'omitir', 'cerrar',
                         'entendido', 'skip tour', 'dismiss'].includes(t)) {
                        btn.click();
                        dismissed.push('clicked:' + t);
                    }
                });
                return dismissed.join(', ') || 'none';
            """)
            if result != 'none':
                print(f"[OVERLAY] Cerrados: {result}")
                time.sleep(1)
        except Exception as e:
            print(f"[OVERLAY] Error: {e}")

    def _wait_for_video_processing(self, driver, timeout=120):
        """Espera a que TikTok termine de procesar el video. Hace retry si hay error."""
        print(f"[PROCESS] Esperando procesamiento del video (max {timeout}s)...")
        start = time.time()
        last_status = ""
        retries_done = 0
        max_retries = 3

        while time.time() - start < timeout:
            status = driver.execute_script("""
                const progress = document.querySelector('[class*="progress"]');
                const processing = document.querySelector('[class*="processing"]');
                const uploading = document.querySelector('[class*="uploading"]');
                const postBtn = document.querySelector('button[data-e2e="post_video_button"]');
                const retryBtn = document.querySelector('button') ?
                    Array.from(document.querySelectorAll('button')).find(b =>
                        b.textContent.trim().toLowerCase() === 'retry') : null;
                // Buscar error SOLO en textos especificos, no en clases CSS
                const bodyText = document.body.innerText;
                const hasErrorText = bodyText.includes('Something went wrong') ||
                                     bodyText.includes('Upload failed') ||
                                     bodyText.includes('Algo salió mal');

                let info = {
                    hasProgress: !!progress,
                    hasProcessing: !!processing,
                    hasUploading: !!uploading,
                    hasErrorText: hasErrorText,
                    hasRetryBtn: !!retryBtn,
                    postBtnExists: !!postBtn,
                    postBtnDisabled: postBtn ? postBtn.disabled : null,
                    postBtnText: postBtn ? postBtn.textContent.trim() : ''
                };

                const pctMatch = bodyText.match(/(\\d+)%/);
                if (pctMatch) info.percentage = pctMatch[1];

                if (bodyText.toLowerCase().includes('uploaded')) info.uploaded = true;

                return JSON.stringify(info);
            """)

            if status != last_status:
                print(f"[PROCESS] Estado: {status}")
                last_status = status

            info = json.loads(status)

            # Si hay error con boton Retry, clickearlo
            if info.get('hasErrorText') and info.get('hasRetryBtn') and retries_done < max_retries:
                retries_done += 1
                print(f"[PROCESS] Error detectado, clickeando Retry ({retries_done}/{max_retries})...")
                driver.execute_script("""
                    const btns = document.querySelectorAll('button');
                    for (const b of btns) {
                        if (b.textContent.trim().toLowerCase() === 'retry') {
                            b.click();
                            break;
                        }
                    }
                """)
                time.sleep(10)
                last_status = ""  # Reset para volver a logear
                continue

            # Si hay error sin retry o ya agotamos retries
            if info.get('hasErrorText') and retries_done >= max_retries:
                print(f"[PROCESS] ERROR persistente tras {max_retries} retries")
                return False

            # Si el boton Post existe, NO esta disabled, y ya se subio
            if (info.get('postBtnExists') and
                    info.get('postBtnDisabled') is False and
                    not info.get('hasErrorText')):
                print("[PROCESS] Video procesado - boton Post habilitado, sin errores")
                return True

            time.sleep(5)

        print(f"[PROCESS] Timeout {timeout}s")
        return False

    def upload_video(self, video_path, description):
        """Sube y publica un video a TikTok usando Selenium."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        print(f"[UPLOAD] Video: {video_path}")
        print(f"[UPLOAD] Descripcion: {description[:100]}...")

        # Verificar que el archivo existe y tiene tamano
        if not os.path.exists(video_path):
            print(f"[UPLOAD] ERROR: Archivo no existe: {video_path}")
            return False
        file_size = os.path.getsize(video_path)
        print(f"[UPLOAD] Tamano archivo: {file_size} bytes")
        if file_size < 1000:
            print("[UPLOAD] ERROR: Archivo muy pequeno, probablemente dummy")
            return False

        try:
            driver = _get_chrome_driver()
            print("[UPLOAD] Chrome creado.")

            if not self._inject_cookies(driver):
                driver.quit()
                return False

            if not self._verify_session(driver):
                driver.quit()
                return False

            # Diagnostico de la pagina
            page_info = driver.execute_script("""
                return JSON.stringify({
                    url: location.href,
                    title: document.title,
                    fileInputs: document.querySelectorAll('input[type="file"]').length,
                    iframes: document.querySelectorAll('iframe').length,
                    bodyText: document.body.innerText.substring(0, 500)
                });
            """)
            print(f"[PAGE] Info: {page_info}")

            # Buscar file input
            print("[UPLOAD] Buscando input de archivo...")
            file_input = None

            # Intentar en el documento principal
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            if file_inputs:
                file_input = file_inputs[0]
                print(f"[UPLOAD] File input encontrado en documento principal")

            # Si no, buscar en iframes
            if not file_input:
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for i, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        fi = driver.find_elements(By.XPATH, "//input[@type='file']")
                        if fi:
                            file_input = fi[0]
                            print(f"[UPLOAD] File input en iframe {i}")
                            break
                        driver.switch_to.default_content()
                    except Exception:
                        driver.switch_to.default_content()

            if not file_input:
                print("[UPLOAD] ERROR: No se encontro file input")
                driver.save_screenshot("/tmp/tiktok_no_file_input.png")
                driver.quit()
                return False

            # Enviar archivo
            abs_path = os.path.abspath(video_path)
            file_input.send_keys(abs_path)
            print(f"[UPLOAD] Archivo enviado: {abs_path}")

            # Esperar procesamiento del video (con verificacion real)
            try:
                driver.switch_to.default_content()
            except Exception:
                pass

            # Cerrar overlays antes de esperar
            time.sleep(5)
            self._dismiss_overlays(driver)

            # Esperar a que el video se procese
            processing_ok = self._wait_for_video_processing(driver, timeout=120)

            # Cerrar overlays de nuevo por si aparecieron durante procesamiento
            self._dismiss_overlays(driver)

            # Screenshot post-procesamiento
            driver.save_screenshot("/tmp/tiktok_after_processing.png")
            print(f"[UPLOAD] URL: {driver.current_url}")

            if not processing_ok:
                print("[UPLOAD] ABORTANDO: El video no se proceso correctamente")
                driver.save_screenshot("/tmp/tiktok_processing_failed.png")
                driver.quit()
                return False

            # Escribir descripcion
            try:
                desc_result = driver.execute_script("""
                    const editor = document.querySelector(
                        '.public-DraftEditor-content[contenteditable="true"]'
                    ) || document.querySelector(
                        'div[contenteditable="true"][role="combobox"]'
                    ) || document.querySelector(
                        'div[contenteditable="true"]'
                    );
                    if (editor) {
                        editor.focus();
                        document.execCommand('selectAll', false, null);
                        document.execCommand('delete', false, null);
                        document.execCommand('insertText', false, arguments[0]);
                        editor.dispatchEvent(new Event('input', { bubbles: true }));
                        return 'ok: ' + editor.textContent.substring(0, 50);
                    }
                    return 'not_found';
                """, description)
                print(f"[DESC] Resultado: {desc_result}")
            except Exception as e:
                print(f"[DESC] Error: {e}")

            # === PUBLICAR ===
            print("[PUBLISH] Buscando boton Post...")

            # Primero listar todos los botones para debug
            all_buttons = driver.execute_script("""
                return Array.from(document.querySelectorAll('button')).map(b => ({
                    text: b.textContent.trim(),
                    disabled: b.disabled,
                    dataE2e: b.getAttribute('data-e2e') || '',
                    classes: b.className.substring(0, 80),
                    visible: b.offsetParent !== null
                }));
            """)
            print(f"[PUBLISH] Todos los botones: {json.dumps(all_buttons, ensure_ascii=False)}")

            published = False

            # Metodo 1: Selector data-e2e (mas fiable)
            try:
                post_btn = driver.find_element(By.XPATH, "//button[@data-e2e='post_video_button']")
                if post_btn:
                    is_disabled = post_btn.get_attribute("disabled")
                    btn_text = post_btn.text.strip()
                    print(f"[PUBLISH] Boton encontrado: text='{btn_text}', disabled={is_disabled}")

                    if is_disabled:
                        print("[PUBLISH] Boton deshabilitado - esperando 30s mas...")
                        time.sleep(30)
                        is_disabled = post_btn.get_attribute("disabled")
                        print(f"[PUBLISH] Tras espera: disabled={is_disabled}")

                    if not is_disabled:
                        post_btn.click()
                        print("[PUBLISH] Click en boton Post!")
                        published = True
            except Exception as e:
                print(f"[PUBLISH] data-e2e no encontrado: {e}")

            # Metodo 2: JavaScript click directo
            if not published:
                result = driver.execute_script("""
                    // Buscar boton Post por data-e2e
                    let btn = document.querySelector('button[data-e2e="post_video_button"]');
                    if (btn && !btn.disabled) {
                        btn.click();
                        return 'clicked-e2e: ' + btn.textContent.trim();
                    }
                    // Buscar por texto
                    const buttons = document.querySelectorAll('button');
                    for (const b of buttons) {
                        const t = b.textContent.trim().toLowerCase();
                        if ((t === 'post' || t === 'publicar') && !b.disabled) {
                            b.click();
                            return 'clicked-text: ' + b.textContent.trim();
                        }
                    }
                    // Listar todos
                    return 'none: ' + Array.from(buttons)
                        .map(b => b.textContent.trim() + '(disabled=' + b.disabled + ')')
                        .filter(t => t).join(' | ');
                """)
                print(f"[PUBLISH] JS resultado: {result}")
                if result and result.startswith('clicked'):
                    published = True

            # === VERIFICAR PUBLICACION ===
            if published:
                print("[VERIFY] Esperando confirmacion de publicacion...")
                time.sleep(15)

                # Verificar resultado
                verify = driver.execute_script("""
                    const body = document.body.innerText.toLowerCase();
                    const url = window.location.href;
                    return {
                        url: url,
                        title: document.title,
                        hasSuccess: body.includes('successfully') || body.includes('uploaded') ||
                                    body.includes('publicado') || body.includes('exitosamente'),
                        hasManage: url.includes('manage') || url.includes('content'),
                        hasUploadAnother: body.includes('upload another') || body.includes('subir otro'),
                        hasError: body.includes('failed') || body.includes('error') || body.includes('falló'),
                        bodySnippet: document.body.innerText.substring(0, 300)
                    };
                """)
                print(f"[VERIFY] Resultado: {json.dumps(verify, ensure_ascii=False)}")

                driver.save_screenshot("/tmp/tiktok_after_publish.png")

                if verify.get('hasError'):
                    print("[VERIFY] FALLO: Error detectado post-publicacion")
                    published = False
                elif verify.get('hasSuccess') or verify.get('hasManage') or verify.get('hasUploadAnother'):
                    print("[VERIFY] EXITO: Video publicado confirmado!")
                else:
                    print("[VERIFY] INCIERTO: No se detecto ni exito ni error")
                    # Esperar un poco mas y volver a verificar
                    time.sleep(10)
                    final_url = driver.current_url
                    final_body = driver.execute_script("return document.body.innerText.substring(0, 500)")
                    print(f"[VERIFY] URL final: {final_url}")
                    print(f"[VERIFY] Body final: {final_body[:200]}")
                    driver.save_screenshot("/tmp/tiktok_final_state.png")
            else:
                print("[PUBLISH] FALLO: No se pudo clickear ningun boton de publicar")
                driver.save_screenshot("/tmp/tiktok_no_publish.png")

            driver.quit()
            return published

        except Exception as e:
            print(f"[UPLOAD] ERROR: {e}")
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
