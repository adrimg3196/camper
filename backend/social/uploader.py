"""
TikTok Video Uploader - Selenium con Xvfb (display virtual).
Usa Chrome REAL (no headless) en un display virtual para evitar
detección anti-bot de TikTok que bloquea la publicación.
"""
import os
import json
import time
import subprocess


def _start_xvfb():
    """Inicia Xvfb (display virtual) para ejecutar Chrome real sin pantalla."""
    display = ":99"
    env_display = os.environ.get("DISPLAY")
    if env_display:
        print(f"[XVFB] DISPLAY ya configurado: {env_display}")
        return env_display

    try:
        # Matar cualquier Xvfb existente
        subprocess.run(["pkill", "-f", "Xvfb"], capture_output=True)
        time.sleep(1)

        # Iniciar Xvfb con resolución alta
        proc = subprocess.Popen(
            ["Xvfb", display, "-screen", "0", "1920x1080x24", "-ac", "-nolisten", "tcp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(2)

        if proc.poll() is not None:
            print("[XVFB] ERROR: Xvfb no arrancó")
            return None

        os.environ["DISPLAY"] = display
        print(f"[XVFB] Iniciado en {display} (PID: {proc.pid})")
        return display
    except FileNotFoundError:
        print("[XVFB] No instalado - usando headless como fallback")
        return None


def _get_chrome_driver():
    """Crea un Chrome WebDriver con máxima evasión anti-bot."""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    # Intentar Xvfb primero (Chrome real > headless)
    display = _start_xvfb()
    use_headless = display is None

    options = webdriver.ChromeOptions()

    # Anti-detección básica
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    if use_headless:
        # Fallback: headless solo si Xvfb no está disponible
        print("[CHROME] Modo headless (fallback sin Xvfb)")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        # Chrome REAL en display virtual - indetectable
        print(f"[CHROME] Modo REAL con display virtual {display}")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-gpu")

    # User-agent realista (no menciona HeadlessChrome)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    })

    driver_path = ChromeDriverManager().install()
    if "THIRD_PARTY" in driver_path:
        driver_path = driver_path.replace(
            "THIRD_PARTY_NOTICES.chromedriver", "chromedriver"
        )
    os.chmod(driver_path, 0o755)

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    # CDP stealth patches - eliminar todas las huellas de automatización
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """
        // 1. Eliminar navigator.webdriver
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        delete navigator.__proto__.webdriver;

        // 2. Chrome runtime
        window.chrome = {
            runtime: {},
            loadTimes: function() { return {}; },
            csi: function() { return {}; },
            app: { isInstalled: false }
        };

        // 3. Plugins realistas
        Object.defineProperty(navigator, 'plugins', {
            get: () => {
                const plugins = [
                    {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                    {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                    {name: 'Native Client', filename: 'internal-nacl-plugin'}
                ];
                plugins.length = 3;
                return plugins;
            }
        });

        // 4. Languages
        Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'es', 'en-US', 'en']});

        // 5. Platform
        Object.defineProperty(navigator, 'platform', {get: () => 'Linux x86_64'});

        // 6. Permissions query - evitar leak
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );

        // 7. WebGL vendor/renderer (evitar "Google SwiftShader")
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter.call(this, parameter);
        };

        // 8. Eliminar cdc_ markers del ChromeDriver
        for (let key in window) {
            if (key.match(/^cdc_/) || key.match(/^\\$cdc_/)) {
                delete window[key];
            }
        }

        // 9. Canvas fingerprint noise (sutil)
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {
            if (type === 'image/png' && this.width > 0 && this.height > 0) {
                const ctx = this.getContext('2d');
                if (ctx) {
                    const imageData = ctx.getImageData(0, 0, 1, 1);
                    imageData.data[0] = imageData.data[0] ^ 1; // 1 pixel noise
                    ctx.putImageData(imageData, 0, 0);
                }
            }
            return toDataURL.apply(this, arguments);
        };

        // 10. Ocultar Automation flags
        Object.defineProperty(document, 'hidden', {get: () => false});
        Object.defineProperty(document, 'visibilityState', {get: () => 'visible'});
    """})

    # Configurar timeouts
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)

    print(f"[CHROME] Driver creado. Headless={use_headless}")
    return driver


class TikTokUploader:
    def __init__(self):
        self.driver = None

    def _inject_cookies(self, driver):
        """Inyecta cookies de TikTok desde variable de entorno."""
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("[COOKIES] No hay TIKTOK_COOKIES_JSON configurado.")
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
        """Verifica que la sesión está activa."""
        driver.get("https://www.tiktok.com")
        time.sleep(5)

        login_check = driver.execute_script("""
            const cookies = document.cookie;
            const hasSid = cookies.includes('sid_tt') || cookies.includes('sessionid');
            const avatar = document.querySelector('[data-e2e="profile-icon"]') ||
                           document.querySelector('img[alt*="avatar"]') ||
                           document.querySelector('[class*="avatar"]');
            return {
                hasSidCookie: hasSid,
                hasAvatar: !!avatar,
                url: window.location.href
            };
        """)
        print(f"[SESSION] sid={login_check.get('hasSidCookie')}, avatar={login_check.get('hasAvatar')}")

        # Navegar a TikTok Studio Upload
        driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=es")
        time.sleep(8)

        current_url = driver.current_url
        print(f"[SESSION] URL: {current_url}")

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

        print("[SESSION] OK")
        return True

    def _dismiss_overlays(self, driver):
        """Cierra overlays de tutorial (react-joyride) y popups modales."""
        try:
            result = driver.execute_script("""
                let dismissed = [];
                document.querySelectorAll('[class*="react-joyride"]').forEach(el => {
                    el.remove();
                    dismissed.push('joyride');
                });
                document.querySelectorAll('.react-joyride__overlay').forEach(el => {
                    el.remove();
                    dismissed.push('overlay');
                });
                // Cerrar containers joyride con z-index alto
                document.querySelectorAll('[class*="joyride"]').forEach(el => {
                    el.remove();
                    dismissed.push('joyride-container');
                });
                // Click botones de dismiss
                document.querySelectorAll('button').forEach(btn => {
                    const t = btn.textContent.toLowerCase().trim();
                    if (['skip', 'got it', 'close', 'omitir', 'cerrar',
                         'entendido', 'skip tour', 'dismiss', 'ok'].includes(t)) {
                        btn.click();
                        dismissed.push('clicked:' + t);
                    }
                });
                // Cerrar modales genéricos
                document.querySelectorAll('[class*="modal-mask"], [class*="modal-overlay"]').forEach(el => {
                    el.remove();
                    dismissed.push('modal');
                });
                return dismissed.join(', ') || 'none';
            """)
            if result != 'none':
                print(f"[OVERLAY] Cerrados: {result}")
                time.sleep(1)
        except Exception as e:
            print(f"[OVERLAY] Error: {e}")

    def _wait_for_video_processing(self, driver, timeout=120):
        """Espera a que TikTok termine de procesar el video."""
        print(f"[PROCESS] Esperando procesamiento (max {timeout}s)...")
        start = time.time()
        last_status = ""
        retries_done = 0
        max_retries = 3

        while time.time() - start < timeout:
            status = driver.execute_script("""
                const postBtn = document.querySelector('button[data-e2e="post_video_button"]');
                const retryBtn = Array.from(document.querySelectorAll('button')).find(b =>
                    b.textContent.trim().toLowerCase() === 'retry' ||
                    b.textContent.trim().toLowerCase() === 'reintentar');
                const bodyText = document.body.innerText;
                const hasErrorText = bodyText.includes('Something went wrong') ||
                                     bodyText.includes('Upload failed') ||
                                     bodyText.includes('Algo salió mal');
                let info = {
                    hasErrorText: hasErrorText,
                    hasRetryBtn: !!retryBtn,
                    postBtnExists: !!postBtn,
                    postBtnDisabled: postBtn ? postBtn.disabled : null,
                    postBtnText: postBtn ? postBtn.textContent.trim() : ''
                };
                const pctMatch = bodyText.match(/(\\d+)%/);
                if (pctMatch) info.percentage = pctMatch[1];
                return JSON.stringify(info);
            """)

            if status != last_status:
                print(f"[PROCESS] {status}")
                last_status = status

            info = json.loads(status)

            # Retry si hay error
            if info.get('hasErrorText') and info.get('hasRetryBtn') and retries_done < max_retries:
                retries_done += 1
                print(f"[PROCESS] Error detectado - Retry {retries_done}/{max_retries}")
                driver.execute_script("""
                    const btns = document.querySelectorAll('button');
                    for (const b of btns) {
                        const t = b.textContent.trim().toLowerCase();
                        if (t === 'retry' || t === 'reintentar') { b.click(); break; }
                    }
                """)
                time.sleep(10)
                last_status = ""
                continue

            if info.get('hasErrorText') and retries_done >= max_retries:
                print(f"[PROCESS] ERROR persistente tras {max_retries} retries")
                return False

            # Listo si Post está habilitado y sin errores
            if (info.get('postBtnExists') and
                    info.get('postBtnDisabled') is False and
                    not info.get('hasErrorText')):
                print("[PROCESS] OK - Post button habilitado")
                return True

            time.sleep(5)

        print(f"[PROCESS] Timeout {timeout}s")
        return False

    def _human_like_click(self, driver, element):
        """Click simulando comportamiento humano con ActionChains."""
        from selenium.webdriver.common.action_chains import ActionChains
        import random

        try:
            # Scroll al elemento
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(random.uniform(0.3, 0.8))

            # Mover mouse al elemento y click
            actions = ActionChains(driver)
            actions.move_to_element(element)
            actions.pause(random.uniform(0.2, 0.5))
            actions.click()
            actions.perform()
            return True
        except Exception as e:
            print(f"[CLICK] ActionChains falló: {e}, usando click directo")
            try:
                element.click()
                return True
            except Exception as e2:
                print(f"[CLICK] Click directo falló: {e2}, usando JS click")
                driver.execute_script("arguments[0].click();", element)
                return True

    def _verify_publish(self, driver):
        """Verificación REAL de que el video se publicó.
        Busca cambios reales: redirect a /manage, modal de éxito,
        desaparición del editor, etc.
        """
        print("[VERIFY] Verificando publicación real...")

        # Capturar estado antes
        pre_url = driver.current_url
        print(f"[VERIFY] URL pre-publish: {pre_url}")

        # Esperar 20s para que TikTok procese la publicación
        for i in range(4):
            time.sleep(5)
            current_url = driver.current_url
            page_state = driver.execute_script("""
                const body = document.body.innerText;
                const url = window.location.href;

                // Indicadores REALES de éxito (no "uploaded" que es del file upload)
                const successIndicators = [
                    body.includes('Your video is being uploaded'),
                    body.includes('Manage your posts'),
                    body.includes('Upload another video'),
                    body.includes('Subir otro video'),
                    body.includes('Video publicado'),
                    body.includes('successfully posted'),
                    body.includes('being processed'),
                    body.includes('Gestionar tus publicaciones'),
                    url.includes('/manage'),
                    url.includes('/content'),
                    url.includes('/post/'),
                ];

                // Indicadores de fallo
                const failIndicators = [
                    body.includes('Something went wrong'),
                    body.includes('Algo salió mal'),
                    body.includes('Upload failed'),
                    body.includes('Try again'),
                    body.includes('Reintentar'),
                ];

                // El editor desapareció (señal de éxito)
                const editorGone = !document.querySelector('.public-DraftEditor-content[contenteditable="true"]');

                // El botón Post desapareció o cambió
                const postBtn = document.querySelector('button[data-e2e="post_video_button"]');
                const postBtnGone = !postBtn;

                return {
                    url: url,
                    urlChanged: url !== arguments[0],
                    successCount: successIndicators.filter(Boolean).length,
                    failCount: failIndicators.filter(Boolean).length,
                    editorGone: editorGone,
                    postBtnGone: postBtnGone,
                    title: document.title,
                    bodySnippet: body.substring(0, 500)
                };
            """, pre_url)

            print(f"[VERIFY] Check {i+1}/4: url_changed={page_state.get('urlChanged')}, "
                  f"success={page_state.get('successCount')}, fail={page_state.get('failCount')}, "
                  f"editor_gone={page_state.get('editorGone')}, post_btn_gone={page_state.get('postBtnGone')}")

            # ÉXITO claro: URL cambió a manage/content o indicadores de éxito
            if page_state.get('urlChanged') and (
                '/manage' in str(page_state.get('url', '')) or
                '/content' in str(page_state.get('url', ''))
            ):
                print("[VERIFY] ÉXITO: Redirigido a gestión de contenido")
                return True

            if page_state.get('successCount', 0) >= 1:
                print("[VERIFY] ÉXITO: Indicadores de publicación detectados")
                return True

            # FALLO claro
            if page_state.get('failCount', 0) >= 1:
                print("[VERIFY] FALLO: Error detectado post-publicación")
                print(f"[VERIFY] Body: {page_state.get('bodySnippet', '')[:300]}")
                return False

        # Si después de 20s nada cambió, es probable que TikTok bloqueó silenciosamente
        final_state = driver.execute_script("""
            return {
                url: window.location.href,
                title: document.title,
                body: document.body.innerText.substring(0, 800),
                postBtnExists: !!document.querySelector('button[data-e2e="post_video_button"]'),
                hasFileInput: !!document.querySelector('input[type="file"]')
            };
        """)
        print(f"[VERIFY] Estado final: url={final_state.get('url')}")
        print(f"[VERIFY] Post btn existe: {final_state.get('postBtnExists')}")
        print(f"[VERIFY] Body: {final_state.get('body', '')[:400]}")

        driver.save_screenshot("/tmp/tiktok_verify_final.png")

        # Si la URL no cambió y el botón Post sigue ahí, NO se publicó
        if final_state.get('postBtnExists') and not page_state.get('urlChanged'):
            print("[VERIFY] FALLO: Nada cambió - TikTok probablemente bloqueó la publicación")
            return False

        # Si el editor desapareció, puede ser éxito
        if page_state.get('editorGone') and page_state.get('postBtnGone'):
            print("[VERIFY] POSIBLE ÉXITO: Editor y botón Post desaparecieron")
            return True

        print("[VERIFY] INCIERTO: No se pudo confirmar. Asumiendo fallo.")
        return False

    def upload_video(self, video_path, description):
        """Sube y publica un video a TikTok."""
        from selenium.webdriver.common.by import By

        print(f"[UPLOAD] Video: {video_path}")
        print(f"[UPLOAD] Desc: {description[:80]}...")

        # Verificar archivo
        if not os.path.exists(video_path):
            print(f"[UPLOAD] ERROR: Archivo no existe")
            return False
        file_size = os.path.getsize(video_path)
        print(f"[UPLOAD] Tamaño: {file_size} bytes ({file_size // 1024}KB)")
        if file_size < 10000:
            print("[UPLOAD] ERROR: Archivo muy pequeño")
            return False

        try:
            driver = _get_chrome_driver()

            if not self._inject_cookies(driver):
                driver.quit()
                return False

            if not self._verify_session(driver):
                driver.quit()
                return False

            # Diagnóstico
            page_info = driver.execute_script("""
                return JSON.stringify({
                    url: location.href,
                    title: document.title,
                    fileInputs: document.querySelectorAll('input[type="file"]').length
                });
            """)
            print(f"[PAGE] {page_info}")

            # Buscar file input
            print("[UPLOAD] Buscando file input...")
            file_input = None

            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            if file_inputs:
                file_input = file_inputs[0]
                print("[UPLOAD] File input encontrado")

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
                print("[UPLOAD] ERROR: No file input")
                driver.save_screenshot("/tmp/tiktok_no_input.png")
                driver.quit()
                return False

            # Enviar archivo
            abs_path = os.path.abspath(video_path)
            file_input.send_keys(abs_path)
            print(f"[UPLOAD] Archivo enviado")

            try:
                driver.switch_to.default_content()
            except Exception:
                pass

            # Cerrar overlays
            time.sleep(5)
            self._dismiss_overlays(driver)

            # Esperar procesamiento
            processing_ok = self._wait_for_video_processing(driver, timeout=120)
            self._dismiss_overlays(driver)

            if not processing_ok:
                print("[UPLOAD] ABORTANDO: Video no se procesó")
                driver.save_screenshot("/tmp/tiktok_process_fail.png")
                driver.quit()
                return False

            # Escribir descripción
            time.sleep(2)
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
                print(f"[DESC] {desc_result}")
            except Exception as e:
                print(f"[DESC] Error: {e}")

            # === PUBLICAR ===
            print("[PUBLISH] Buscando botón Post...")

            # Log todos los botones
            all_buttons = driver.execute_script("""
                return Array.from(document.querySelectorAll('button')).map(b => ({
                    text: b.textContent.trim().substring(0, 30),
                    disabled: b.disabled,
                    e2e: b.getAttribute('data-e2e') || '',
                    visible: b.offsetParent !== null
                }));
            """)
            print(f"[PUBLISH] Botones: {json.dumps(all_buttons, ensure_ascii=False)}")

            published = False

            # Método 1: data-e2e selector + human-like click
            try:
                post_btn = driver.find_element(By.XPATH, "//button[@data-e2e='post_video_button']")
                if post_btn:
                    is_disabled = post_btn.get_attribute("disabled")
                    btn_text = post_btn.text.strip()
                    print(f"[PUBLISH] Botón: text='{btn_text}', disabled={is_disabled}")

                    if is_disabled:
                        print("[PUBLISH] Deshabilitado - esperando 30s...")
                        time.sleep(30)
                        self._dismiss_overlays(driver)
                        is_disabled = post_btn.get_attribute("disabled")

                    if not is_disabled:
                        # Cerrar overlays justo antes del click
                        self._dismiss_overlays(driver)
                        time.sleep(1)

                        # Click humano (ActionChains)
                        self._human_like_click(driver, post_btn)
                        print("[PUBLISH] Click realizado!")
                        published = True
            except Exception as e:
                print(f"[PUBLISH] Método 1 falló: {e}")

            # Método 2: JS click
            if not published:
                result = driver.execute_script("""
                    let btn = document.querySelector('button[data-e2e="post_video_button"]');
                    if (btn && !btn.disabled) {
                        btn.click();
                        return 'clicked-e2e: ' + btn.textContent.trim();
                    }
                    const buttons = document.querySelectorAll('button');
                    for (const b of buttons) {
                        const t = b.textContent.trim().toLowerCase();
                        if ((t === 'post' || t === 'publicar') && !b.disabled) {
                            b.click();
                            return 'clicked-text: ' + b.textContent.trim();
                        }
                    }
                    return 'none';
                """)
                print(f"[PUBLISH] JS: {result}")
                if result and result.startswith('clicked'):
                    published = True

            # === VERIFICAR PUBLICACIÓN REAL ===
            if published:
                driver.save_screenshot("/tmp/tiktok_post_clicked.png")
                success = self._verify_publish(driver)

                if success:
                    print("[RESULT] VIDEO PUBLICADO EXITOSAMENTE!")
                else:
                    print("[RESULT] FALLO: Video NO se publicó realmente")

                driver.quit()
                return success
            else:
                print("[PUBLISH] FALLO: No se pudo clickear Post")
                driver.save_screenshot("/tmp/tiktok_no_post.png")
                driver.quit()
                return False

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
