"""
TikTok Video Uploader - API directa (sin Selenium).
Usa la API interna de TikTok para subir y publicar videos
directamente con requests HTTP, sin necesidad de navegador.
Basado en el trabajo de MiniGlome (https://github.com/MiniGlome/Tiktok-uploader).
"""
import os
import json
import time
import datetime
import hashlib
import hmac
import random
import zlib
import requests


def _sign(key, msg):
    """HMAC-SHA256 para AWS SigV4."""
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def _get_signature_key(key, date_stamp, region, service):
    """Deriva la clave de firma AWS SigV4."""
    k_date = _sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    k_signing = _sign(k_service, 'aws4_request')
    return k_signing


def _aws_signature(access_key, secret_key, request_parameters, headers,
                   method="GET", payload='', region="us-east-1", service="vod"):
    """Genera firma AWS SigV4 para ByteVcloud."""
    canonical_uri = '/'
    canonical_querystring = request_parameters
    canonical_headers = '\n'.join([f"{k}:{v}" for k, v in headers.items()]) + '\n'
    signed_headers = ';'.join(headers.keys())
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    canonical_request = (method + '\n' + canonical_uri + '\n' + canonical_querystring +
                         '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash)

    amzdate = headers["x-amz-date"]
    datestamp = amzdate.split('T')[0]
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = (algorithm + '\n' + amzdate + '\n' + credential_scope + '\n' +
                      hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())

    signing_key = _get_signature_key(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def _crc32(content):
    """Calcula CRC32 de bytes."""
    prev = zlib.crc32(content, 0)
    return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)


def _extract_session_ids(cookies_json_str):
    """Extrae todas las posibles session IDs de TIKTOK_COOKIES_JSON."""
    session_ids = []
    try:
        cookies = json.loads(cookies_json_str)
        # Prioridad: sessionid > sessionid_ss > sid_tt
        priority_names = ['sessionid', 'sessionid_ss', 'sid_tt']
        for target_name in priority_names:
            for cookie in cookies:
                name = cookie.get('name', '')
                if name == target_name:
                    value = cookie.get('value', '')
                    if value and value not in [s[1] for s in session_ids]:
                        session_ids.append((name, value))
        # Log
        print(f"[COOKIES] Session cookies encontradas: {[s[0] for s in session_ids]}")
        for name, val in session_ids:
            print(f"[COOKIES]   {name}: {val[:8]}...{val[-4:] if len(val) > 8 else val}")
    except Exception as e:
        print(f"[COOKIES] Error parseando cookies: {e}")
    return session_ids


class TikTokUploader:
    """Sube videos a TikTok usando la API interna (sin Selenium)."""

    def __init__(self):
        self.session_id = None

    def _get_session_ids(self):
        """Obtiene todas las session IDs de las cookies del entorno."""
        cookies_json = os.environ.get("TIKTOK_COOKIES_JSON")
        if not cookies_json:
            print("[AUTH] No hay TIKTOK_COOKIES_JSON")
            return []

        return _extract_session_ids(cookies_json)

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

        # Obtener todas las session IDs y probar cada una
        session_ids = self._get_session_ids()
        if not session_ids:
            print("[AUTH] ❌ ERROR CRÍTICO: No hay session IDs en las cookies.")
            print("[AUTH] ❌ Necesitas actualizar TIKTOK_COOKIES_JSON con cookies frescas.")
            print("[AUTH] ❌ Pasos: 1) Inicia sesión en tiktok.com 2) Exporta cookies con 'Get cookies.txt' 3) Actualiza el secreto en GitHub")
            return False

        for cookie_name, session_id in session_ids:
            print(f"\n[AUTH] Probando cookie '{cookie_name}': {session_id[:8]}...")
            try:
                result = self._upload_via_api(session_id, video_path, description)
                if result:
                    return True
                print(f"[AUTH] Cookie '{cookie_name}' no funcionó, probando siguiente...")
            except Exception as e:
                print(f"[AUTH] Cookie '{cookie_name}' error: {e}")
                continue

        print("\n[AUTH] ❌ TODAS las cookies de sesión fallaron.")
        print("[AUTH] ❌ Las cookies han EXPIRADO. Necesitas renovarlas:")
        print("[AUTH] ❌ 1) Abre TikTok en tu navegador e inicia sesión")
        print("[AUTH] ❌ 2) Usa la extensión 'Get cookies.txt' para exportar cookies")
        print("[AUTH] ❌ 3) Actualiza el secreto TIKTOK_COOKIES_JSON en GitHub Settings > Secrets")
        return False

    def _upload_via_api(self, session_id, video_path, description):
        """Upload completo via API interna de TikTok."""
        session = requests.Session()
        session.cookies.set("sessionid", session_id, domain=".tiktok.com")
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })

        # === PASO 1: Verificar sesión ===
        print("[API] Paso 1: Verificando sesión...")
        url = "https://www.tiktok.com/passport/web/account/info/"
        r = session.get(url)
        if r.status_code != 200:
            print(f"[API] ERROR: account/info status={r.status_code}")
            print(f"[API] Response: {r.text[:500]}")
            return False

        data = r.json()
        if data.get("message") != "success":
            print(f"[API] ERROR: sesión inválida: {data}")
            return False

        user_id = data.get("data", {}).get("user_id_str", "")
        username = data.get("data", {}).get("username", "")
        print(f"[API] Sesión OK: user={username} (id={user_id})")

        # === PASO 2: Obtener credenciales AWS para upload ===
        print("[API] Paso 2: Obteniendo credenciales de upload...")
        url = "https://www.tiktok.com/api/v1/video/upload/auth/"
        r = session.get(url)
        if r.status_code != 200:
            print(f"[API] ERROR: upload/auth status={r.status_code}")
            return False

        token_data = r.json().get("video_token_v5", {})
        access_key = token_data.get("access_key_id")
        secret_key = token_data.get("secret_acess_key")  # Nota: typo de TikTok
        session_token = token_data.get("session_token")

        if not all([access_key, secret_key, session_token]):
            print(f"[API] ERROR: credenciales AWS incompletas")
            print(f"[API] Keys: ak={'yes' if access_key else 'no'}, sk={'yes' if secret_key else 'no'}, st={'yes' if session_token else 'no'}")
            return False
        print("[API] Credenciales AWS obtenidas")

        # === PASO 3: Leer video ===
        with open(video_path, "rb") as f:
            video_content = f.read()
        file_size = len(video_content)
        print(f"[API] Video leído: {file_size} bytes")

        # === PASO 4: Inicializar upload en ByteVcloud ===
        print("[API] Paso 4: Inicializando upload en ByteVcloud...")
        vod_url = "https://vod-us-east-1.bytevcloudapi.com/"
        request_params = (f'Action=ApplyUploadInner&FileSize={file_size}&FileType=video'
                          f'&IsInner=1&SpaceName=tiktok&Version=2020-11-19&s=zdxefu8qvq8')

        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        headers = {
            "x-amz-date": amzdate,
            "x-amz-security-token": session_token,
        }
        signature = _aws_signature(access_key, secret_key, request_params, headers)
        authorization = (f"AWS4-HMAC-SHA256 Credential={access_key}/{datestamp}/us-east-1/vod/aws4_request, "
                         f"SignedHeaders=x-amz-date;x-amz-security-token, Signature={signature}")
        headers["authorization"] = authorization

        r = session.get(f"{vod_url}?{request_params}", headers=headers)
        if r.status_code != 200:
            print(f"[API] ERROR: ApplyUploadInner status={r.status_code}")
            print(f"[API] Response: {r.text[:500]}")
            return False

        upload_node = r.json()["Result"]["InnerUploadAddress"]["UploadNodes"][0]
        video_id = upload_node["Vid"]
        store_uri = upload_node["StoreInfos"][0]["StoreUri"]
        video_auth = upload_node["StoreInfos"][0]["Auth"]
        upload_host = upload_node["UploadHost"]
        session_key = upload_node["SessionKey"]
        print(f"[API] Upload node: vid={video_id}, host={upload_host}")

        # === PASO 5: Crear sesión multipart ===
        print("[API] Paso 5: Creando sesión multipart...")
        url = f"https://{upload_host}/{store_uri}?uploads"
        rand = ''.join(random.choice('0123456789') for _ in range(30))
        headers = {
            "Authorization": video_auth,
            "Content-Type": f"multipart/form-data; boundary=---------------------------{rand}",
        }
        data = f"-----------------------------{rand}--"
        r = session.post(url, headers=headers, data=data)
        if r.status_code != 200:
            print(f"[API] ERROR: multipart init status={r.status_code}")
            return False
        upload_id = r.json()["payload"]["uploadID"]
        print(f"[API] Upload ID: {upload_id}")

        # === PASO 6: Subir chunks ===
        print("[API] Paso 6: Subiendo video en chunks...")
        chunk_size = 5242880  # 5MB
        chunks = []
        i = 0
        while i < file_size:
            chunks.append(video_content[i:i + chunk_size])
            i += chunk_size

        crcs = []
        for idx, chunk in enumerate(chunks):
            crc = _crc32(chunk)
            crcs.append(crc)
            url = f"https://{upload_host}/{store_uri}?partNumber={idx + 1}&uploadID={upload_id}"
            headers = {
                "Authorization": video_auth,
                "Content-Type": "application/octet-stream",
                "Content-Disposition": 'attachment; filename="undefined"',
                "Content-Crc32": crc,
            }
            r = session.post(url, headers=headers, data=chunk)
            if r.status_code != 200:
                print(f"[API] ERROR: chunk {idx + 1}/{len(chunks)} status={r.status_code}")
                return False
            print(f"[API]   Chunk {idx + 1}/{len(chunks)} subido ({len(chunk)} bytes)")

        # === PASO 7: Completar upload ===
        print("[API] Paso 7: Completando upload...")
        url = f"https://{upload_host}/{store_uri}?uploadID={upload_id}"
        headers = {
            "Authorization": video_auth,
            "Content-Type": "text/plain;charset=UTF-8",
        }
        data = ','.join([f"{i + 1}:{crcs[i]}" for i in range(len(crcs))])
        r = requests.post(url, headers=headers, data=data)
        if r.status_code != 200:
            print(f"[API] ERROR: complete upload status={r.status_code}")
            return False
        print("[API] Upload completado")

        # === PASO 8: Commit upload ===
        print("[API] Paso 8: Commit upload...")
        request_params = 'Action=CommitUploadInner&SpaceName=tiktok&Version=2020-11-19'
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        commit_data = '{"SessionKey":"' + session_key + '","Functions":[]}'
        amzcontentsha256 = hashlib.sha256(commit_data.encode('utf-8')).hexdigest()
        headers = {
            "x-amz-content-sha256": amzcontentsha256,
            "x-amz-date": amzdate,
            "x-amz-security-token": session_token,
        }
        signature = _aws_signature(access_key, secret_key, request_params, headers,
                                   method="POST", payload=commit_data)
        authorization = (f"AWS4-HMAC-SHA256 Credential={access_key}/{datestamp}/us-east-1/vod/aws4_request, "
                         f"SignedHeaders=x-amz-content-sha256;x-amz-date;x-amz-security-token, "
                         f"Signature={signature}")
        headers["authorization"] = authorization
        headers["Content-Type"] = "text/plain;charset=UTF-8"
        r = session.post(f"{vod_url}?{request_params}", headers=headers, data=commit_data)
        if r.status_code != 200:
            print(f"[API] ERROR: CommitUpload status={r.status_code}")
            return False
        print("[API] Commit OK")

        # === PASO 9: Preparar título y hashtags ===
        print("[API] Paso 9: Preparando publicación...")
        # Separar título y hashtags del description
        text = description
        text_extra = []

        # Extraer hashtags existentes del texto
        import re
        hashtag_pattern = re.compile(r'#(\w+)')
        found_tags = hashtag_pattern.findall(description)

        # Reconstruir texto sin hashtags
        clean_text = hashtag_pattern.sub('', description).strip()
        text = clean_text

        # Verificar y agregar hashtags
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

        print(f"[API] Texto final: {text[:100]}...")

        # === PASO 10: PUBLICAR ===
        print("[API] Paso 10: PUBLICANDO video...")
        url = "https://www.tiktok.com/api/v1/item/create/"

        # Obtener CSRF token
        csrf_headers = {
            "X-Secsdk-Csrf-Request": "1",
            "X-Secsdk-Csrf-Version": "1.2.8",
        }
        r = session.head(url, headers=csrf_headers)
        print(f"[API] CSRF head status={r.status_code}")

        # Publicar
        params = {
            "video_id": video_id,
            "visibility_type": "0",  # 0=público
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
        print(f"[API] Publicación status={r.status_code}")

        if r.status_code != 200:
            print(f"[API] ERROR: Publicación falló: {r.text[:500]}")
            return False

        result = r.json()
        status_code = result.get("status_code", -1)
        status_msg = result.get("status_msg", "")

        if status_code == 0:
            print(f"[API] ✅ VIDEO PUBLICADO EXITOSAMENTE!")
            print(f"[API] Response: {json.dumps(result, ensure_ascii=False)[:300]}")
            return True
        else:
            print(f"[API] ERROR: status_code={status_code}, msg={status_msg}")
            print(f"[API] Response completa: {json.dumps(result, ensure_ascii=False)[:500]}")
            return False

    def close(self):
        """Limpia recursos."""
        pass
