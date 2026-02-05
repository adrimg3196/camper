"""
TikTok Video Uploader - API directa (sin Selenium).
Usa la API interna de TikTok via /top/v1 proxy para subir y publicar videos.
Basado en makiisthenes/TiktokAutoUploader (endpoints actualizados 2024).
"""
import os
import json
import re
import time
import uuid
import zlib
import string
import secrets
import requests


def _crc32(content):
    """Calcula CRC32 de bytes."""
    prev = zlib.crc32(content, 0)
    return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)


def _extract_all_cookies(cookies_json_str):
    """Extrae TODAS las cookies de TIKTOK_COOKIES_JSON."""
    all_cookies = []
    session_id = None
    try:
        cookies = json.loads(cookies_json_str)
        for cookie in cookies:
            name = cookie.get('name', '')
            value = cookie.get('value', '')
            domain = cookie.get('domain', '.tiktok.com')
            if name and value:
                all_cookies.append((name, value, domain))
                if name == 'sessionid':
                    session_id = value
        print(f"[COOKIES] Total cookies: {len(all_cookies)}")
        if session_id:
            print(f"[COOKIES] sessionid: {session_id[:8]}...{session_id[-4:]}")
        else:
            print("[COOKIES] WARNING: No se encontró sessionid")
    except Exception as e:
        print(f"[COOKIES] Error parseando cookies: {e}")
    return all_cookies, session_id


class TikTokUploader:
    """Sube videos a TikTok usando la API interna via /top/v1."""

    def __init__(self):
        self.session_id = None
        self.all_cookies = []

    def upload_video(self, video_path, description):
        """Sube y publica un video a TikTok usando la API directa."""
        print(f"[UPLOAD] Video: {video_path}")
        print(f"[UPLOAD] Desc: {description[:80]}...")

        # Verificar archivo
        if not os.path.exists(video_path):
            print("[UPLOAD] ERROR: Archivo no existe")
            return False
        file_size = os.path.getsize(video_path)
        print(f"[UPLOAD] Tamaño: {file_size} bytes ({file_size // 1024}KB)")
        if file_size < 10000:
            print("[UPLOAD] ERROR: Archivo muy pequeño")
            return False

        # Obtener TODAS las cookies
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("[AUTH] No hay TIKTOK_COOKIES_JSON")
            return False

        self.all_cookies, self.session_id = _extract_all_cookies(cookies_json)
        if not self.session_id:
            print("[AUTH] ERROR: No se encontró sessionid en las cookies")
            return False

        try:
            result = self._upload_via_api(video_path, description)
            if result:
                return True
        except Exception as e:
            print(f"[AUTH] Error: {e}")
            import traceback
            traceback.print_exc()

        print("\n[AUTH] La subida falló. Las cookies pueden haber EXPIRADO.")
        print("[AUTH] 1) Abre TikTok en tu navegador e inicia sesión")
        print("[AUTH] 2) Exporta las cookies y actualiza TIKTOK_COOKIES_JSON en GitHub")
        return False

    def _upload_via_api(self, video_path, description):
        """Upload completo via API interna de TikTok usando /top/v1."""
        session = requests.Session()
        # Cargar TODAS las cookies
        for name, value, domain in self.all_cookies:
            session.cookies.set(name, value, domain=domain)
        print(f"[API] Cookies cargadas: {len(self.all_cookies)}")
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        })

        # === PASO 0: Visitar página de upload ===
        print("[API] Paso 0: Visitando /upload/...")
        r = session.get("https://www.tiktok.com/upload/")
        print(f"[API] /upload/ status={r.status_code}")

        # === PASO 1: Verificar sesión ===
        print("[API] Paso 1: Verificando sesión...")
        url = "https://www.tiktok.com/passport/web/account/info/"
        r = session.get(url)
        if r.status_code != 200:
            print(f"[API] ERROR: account/info status={r.status_code}")
            return False

        data = r.json()
        if data.get("message") != "success":
            print(f"[API] ERROR: sesión inválida: {data}")
            return False

        username = data.get("data", {}).get("username", "")
        print(f"[API] Sesión OK: user={username}")

        # === PASO 2: Crear proyecto ===
        print("[API] Paso 2: Creando proyecto...")
        creation_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(21))
        project_url = f"https://www.tiktok.com/api/v1/web/project/create/?creation_id={creation_id}&type=1&aid=1988"
        r = session.post(project_url)
        print(f"[API] project/create status={r.status_code}")
        if r.status_code != 200:
            print(f"[API] ERROR: project/create response: {r.text[:500]}")
            return False
        project_data = r.json()
        print(f"[API] project/create response keys: {list(project_data.keys())}")
        project_id = project_data.get("project", {}).get("project_id", "")
        if not project_id:
            print(f"[API] WARNING: No project_id, response: {json.dumps(project_data)[:300]}")
        else:
            print(f"[API] Project ID: {project_id}")

        # === PASO 3: Obtener credenciales AWS ===
        print("[API] Paso 3: Obteniendo credenciales de upload...")
        url = "https://www.tiktok.com/api/v1/video/upload/auth/?aid=1988"
        r = session.get(url)
        if r.status_code != 200:
            print(f"[API] ERROR: upload/auth status={r.status_code}")
            return False

        auth_json = r.json()
        print(f"[API] upload/auth keys: {list(auth_json.keys())}")
        token_data = auth_json.get("video_token_v5", {})
        access_key = token_data.get("access_key_id")
        secret_key = token_data.get("secret_acess_key")  # Nota: typo de TikTok
        session_token = token_data.get("session_token")

        if not all([access_key, secret_key, session_token]):
            print(f"[API] ERROR: credenciales AWS incompletas")
            print(f"[API] auth response: {json.dumps(auth_json)[:500]}")
            return False
        print(f"[API] AWS creds OK: ak={access_key[:10]}...")

        # === PASO 4: Leer video ===
        with open(video_path, "rb") as f:
            video_content = f.read()
        file_size = len(video_content)
        print(f"[API] Video: {file_size} bytes")

        # === PASO 5: ApplyUploadInner via /top/v1 ===
        print("[API] Paso 5: ApplyUploadInner via /top/v1...")
        # Usar requests_auth_aws_sigv4 para firma correcta
        from requests_auth_aws_sigv4 import AWSSigV4
        aws_auth = AWSSigV4(
            "vod",
            region="ap-singapore-1",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
        )

        apply_url = (f"https://www.tiktok.com/top/v1?"
                     f"Action=ApplyUploadInner&Version=2020-11-19&SpaceName=tiktok"
                     f"&FileType=video&IsInner=1&FileSize={file_size}&s=g158iqx8434")
        r = session.get(apply_url, auth=aws_auth)
        print(f"[API] ApplyUploadInner status={r.status_code}")

        if r.status_code != 200:
            print(f"[API] ERROR: ApplyUploadInner response: {r.text[:500]}")
            return False

        resp_json = r.json()
        print(f"[API] ApplyUploadInner keys: {list(resp_json.keys())}")

        if "Result" not in resp_json:
            print(f"[API] ERROR: No 'Result' key: {json.dumps(resp_json)[:500]}")
            return False

        upload_node = resp_json["Result"]["InnerUploadAddress"]["UploadNodes"][0]
        video_id = upload_node["Vid"]
        store_uri = upload_node["StoreInfos"][0]["StoreUri"]
        video_auth = upload_node["StoreInfos"][0]["Auth"]
        upload_host = upload_node["UploadHost"]
        session_key = upload_node["SessionKey"]
        print(f"[API] Upload node: vid={video_id}, host={upload_host}")

        # === PASO 6: Subir chunks ===
        print("[API] Paso 6: Subiendo video en chunks...")
        chunk_size = 5242880  # 5MB
        chunks = []
        i = 0
        while i < file_size:
            chunks.append(video_content[i:i + chunk_size])
            i += chunk_size

        upload_id = str(uuid.uuid4())
        crcs = []
        for idx, chunk in enumerate(chunks):
            crc = _crc32(chunk)
            crcs.append(crc)
            url = f"https://{upload_host}/{store_uri}?partNumber={idx + 1}&uploadID={upload_id}&phase=transfer"
            headers = {
                "Authorization": video_auth,
                "Content-Type": "application/octet-stream",
                "Content-Disposition": 'attachment; filename="undefined"',
                "Content-Crc32": crc,
            }
            r = session.post(url, headers=headers, data=chunk)
            if r.status_code != 200:
                print(f"[API] ERROR: chunk {idx + 1}/{len(chunks)} status={r.status_code}")
                print(f"[API] Response: {r.text[:300]}")
                return False
            print(f"[API]   Chunk {idx + 1}/{len(chunks)} OK ({len(chunk)} bytes)")

        # === PASO 7: Finish upload ===
        print("[API] Paso 7: Finalizando upload...")
        url = f"https://{upload_host}/{store_uri}?uploadID={upload_id}&phase=finish&uploadmode=part"
        headers = {
            "Authorization": video_auth,
            "Content-Type": "text/plain;charset=UTF-8",
        }
        data = ','.join([f"{i + 1}:{crcs[i]}" for i in range(len(crcs))])
        r = requests.post(url, headers=headers, data=data)
        if r.status_code != 200:
            print(f"[API] ERROR: finish upload status={r.status_code}")
            return False
        print("[API] Upload finalizado")

        # === PASO 8: CommitUploadInner via /top/v1 ===
        print("[API] Paso 8: Commit upload...")
        commit_url = "https://www.tiktok.com/top/v1?Action=CommitUploadInner&Version=2020-11-19&SpaceName=tiktok"
        commit_data = '{"SessionKey":"' + session_key + '","Functions":[{"name":"GetMeta"}]}'
        r = session.post(commit_url, auth=aws_auth, data=commit_data)
        print(f"[API] CommitUploadInner status={r.status_code}")
        if r.status_code != 200:
            print(f"[API] ERROR: CommitUploadInner response: {r.text[:500]}")
            return False
        print("[API] Commit OK")

        # === PASO 9: Preparar texto y hashtags ===
        print("[API] Paso 9: Preparando publicación...")
        text_extra = []
        hashtag_pattern = re.compile(r'#(\w+)')
        found_tags = hashtag_pattern.findall(description)
        clean_text = hashtag_pattern.sub('', description).strip()
        text = clean_text

        for tag in found_tags:
            try:
                url = "https://www.tiktok.com/api/upload/challenge/sug/"
                params = {"keyword": tag}
                r = session.get(url, params=params)
                if r.status_code == 200:
                    sug_list = r.json().get("sug_list", [])
                    verified_tag = sug_list[0]["cha_name"] if sug_list else tag
                else:
                    verified_tag = tag
            except Exception:
                verified_tag = tag

            text += " #" + verified_tag
            text_extra.append({
                "start": len(text) - len(verified_tag) - 1,
                "end": len(text),
                "user_id": "",
                "type": 1,
                "hashtag_name": verified_tag,
            })

        print(f"[API] Texto: {text[:100]}...")

        # === PASO 10: PUBLICAR via /tiktok/web/project/post/v1/ ===
        print("[API] Paso 10: PUBLICANDO video...")

        # Primero visitar home para establecer msToken
        r = session.head("https://www.tiktok.com")

        publish_data = {
            "post_common_info": {
                "creation_id": creation_id,
                "enter_post_page_from": 1,
                "post_type": 3,
            },
            "feature_common_info_list": [{
                "geofencing_regions": [],
                "playlist_name": "",
                "playlist_id": "",
                "tcm_params": '{"commerce_toggle_info":{}}',
                "sound_exemption": 0,
                "anchors": [],
                "vedit_common_info": {
                    "draft": "",
                    "video_id": video_id,
                },
                "privacy_setting_info": {
                    "visibility_type": 0,
                    "allow_duet": 0,
                    "allow_stitch": 0,
                    "allow_comment": 1,
                },
            }],
            "single_post_req_list": [{
                "batch_index": 0,
                "video_id": video_id,
                "is_long_video": 0,
                "single_post_feature_info": {
                    "text": text,
                    "text_extra": text_extra,
                    "markup_text": text,
                    "music_info": {},
                    "poster_delay": 0,
                },
            }],
        }

        mstoken = session.cookies.get("msToken", "")
        publish_params = {
            "app_name": "tiktok_web",
            "channel": "tiktok_web",
            "device_platform": "web",
            "aid": 1988,
        }
        if mstoken:
            publish_params["msToken"] = mstoken

        publish_headers = {
            "Content-Type": "application/json",
        }

        publish_url = "https://www.tiktok.com/tiktok/web/project/post/v1/"
        r = session.post(
            publish_url,
            params=publish_params,
            data=json.dumps(publish_data),
            headers=publish_headers,
        )
        print(f"[API] Publicación status={r.status_code}")

        if r.status_code != 200:
            print(f"[API] ERROR publish: {r.text[:500]}")
            # Fallback: intentar endpoint antiguo
            print("[API] Intentando endpoint antiguo /api/v1/item/create/...")
            return self._publish_legacy(session, video_id, text, text_extra)

        result = r.json()
        status_code = result.get("status_code", -1)
        print(f"[API] Publish response: {json.dumps(result)[:500]}")

        if status_code == 0:
            print("[API] ✅ VIDEO PUBLICADO EXITOSAMENTE!")
            return True
        else:
            print(f"[API] ERROR: status_code={status_code}")
            # Fallback: intentar endpoint antiguo
            print("[API] Intentando endpoint antiguo /api/v1/item/create/...")
            return self._publish_legacy(session, video_id, text, text_extra)

    def _publish_legacy(self, session, video_id, text, text_extra):
        """Intenta publicar via el endpoint antiguo como fallback."""
        url = "https://www.tiktok.com/api/v1/item/create/"
        csrf_headers = {
            "X-Secsdk-Csrf-Request": "1",
            "X-Secsdk-Csrf-Version": "1.2.8",
        }
        session.head(url, headers=csrf_headers)

        params = {
            "video_id": video_id,
            "visibility_type": "0",
            "poster_delay": "0",
            "text": text,
            "text_extra": json.dumps(text_extra),
            "allow_comment": "1",
            "allow_duet": "0",
            "allow_stitch": "0",
            "sound_exemption": "0",
            "aid": "1988",
        }

        r = session.post(url, params=params, headers=csrf_headers)
        print(f"[API] Legacy publish status={r.status_code}")
        if r.status_code != 200:
            print(f"[API] Legacy ERROR: {r.text[:500]}")
            return False

        result = r.json()
        if result.get("status_code") == 0:
            print("[API] ✅ VIDEO PUBLICADO (legacy)!")
            return True
        print(f"[API] Legacy ERROR: {json.dumps(result)[:500]}")
        return False

    def close(self):
        """Limpia recursos."""
        pass
