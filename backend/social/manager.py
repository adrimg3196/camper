import os
import sys
import json
import subprocess
import time
import uuid
import shutil
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import video_config, is_runway_enabled

from .uploader import TikTokUploader
from .dialogue_generator import DialogueGenerator
from .tts_service import TTSService
from .runway_generator import RunwayVideoGenerator, generate_product_dialogue_for_runway


class SocialManager:
    def __init__(self, enable_tts: bool = True, enable_runway: bool = None):
        print("📱 Inicializando Social Manager (TikTok/Instagram)...")
        self.uploader = TikTokUploader()
        self.temp_dir = os.path.join(os.getcwd(), "backend", "temp_assets")
        os.makedirs(self.temp_dir, exist_ok=True)
        # Remotion project lives in video/ at repo root
        self.video_dir = os.path.join(os.getcwd(), "video")
        self.max_retries = video_config.MAX_RETRIES
        self.remotion_concurrency = video_config.REMOTION_CONCURRENCY
        self.remotion_timeout = video_config.REMOTION_TIMEOUT

        # Servicios de voz
        self.enable_tts = enable_tts
        if enable_tts:
            self.dialogue_generator = DialogueGenerator()
            self.tts_service = TTSService(voice="es-ES-ElviraNeural")
            print("   🗣️ TTS habilitado (voz: Elvira)")

        # Generador de video AI con Runway ML (usar config si no se especifica)
        self.enable_runway = enable_runway if enable_runway is not None else is_runway_enabled()
        if self.enable_runway:
            self.runway_generator = RunwayVideoGenerator()
            print("   🎬 Runway ML habilitado (Gen-4 Turbo)")
        else:
            print("   ℹ️ Runway deshabilitado (ENABLE_RUNWAY=false o sin API key)")

    def process_deal(self, deal_data: dict):
        """Toma una oferta y gestiona su publicación en redes."""
        print(f"🎬 Creando contenido para: {deal_data.get('title')}")

        video_path = None

        # Opción 1: Intentar generar video AI con Runway (producto animado 3D)
        if self.enable_runway:
            try:
                video_path = self._generate_runway_video(deal_data)
            except Exception as e:
                print(f"   ⚠️ Runway falló: {e}")
                video_path = None

        # Opción 2: Fallback a Remotion (video con TTS y subtítulos)
        if not video_path:
            try:
                video_path = self.generate_remotion_video(deal_data)
            except Exception as e:
                print(f"   ⚠️ Falló Remotion: {e}")
                video_path = None

        if video_path and os.path.exists(video_path):
            self.upload_to_tiktok(video_path, deal_data)

    def _generate_runway_video(self, deal_data: dict) -> str:
        """
        Genera video con Runway ML donde el producto cobra vida como personaje 3D.
        """
        deal_id = deal_data.get('id') or str(uuid.uuid4())[:8]
        image_url = deal_data.get('image_url')

        if not image_url:
            raise Exception("No hay imagen del producto")

        # Generar diálogo específico para actuación 3D
        dialogue = generate_product_dialogue_for_runway(deal_data)
        print(f"   🎭 Diálogo para Runway: {dialogue[:60]}...")

        # Generar video
        output_path = os.path.join(self.temp_dir, f"runway_{deal_id}.mp4")
        result = self.runway_generator.generate_video(
            deal_data=deal_data,
            dialogue=dialogue,
            image_url=image_url,
            output_path=output_path,
            duration=5,  # 5 segundos
            timeout=300,  # 5 minutos máximo
        )

        if result and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"   ✅ Video Runway generado: {output_path} ({file_size // 1024}KB)")
            return output_path

        return None

    def _generate_talking_product_audio(self, deal_data: dict) -> dict:
        """
        Genera diálogo y audio TTS para video de 'producto que habla'.

        Returns:
            dict con:
            - audio_file: nombre del archivo de audio (para Remotion)
            - dialogue_segments: lista de segmentos con timing
            - full_script: texto completo del diálogo
        """
        deal_id = deal_data.get('id') or str(uuid.uuid4())[:8]

        # 1. Generar diálogo persuasivo con Gemini
        print("   🧠 Generando diálogo con IA...")
        segments = self.dialogue_generator.generate_product_dialogue(deal_data)

        if not segments:
            return None

        # 2. Generar audio TTS
        full_script = self.dialogue_generator.get_full_script(segments)
        audio_filename = f"tts_{deal_id}.mp3"
        audio_path = os.path.join(self.video_dir, "public", audio_filename)

        print(f"   🔊 Generando audio TTS: '{full_script[:50]}...'")
        try:
            audio_info = self.tts_service.synthesize(full_script, audio_path)
        except Exception as e:
            print(f"   ⚠️ Error generando TTS: {e}")
            return None

        return {
            "audio_file": audio_filename,
            "dialogue_segments": segments,
            "full_script": full_script,
            "duration_seconds": audio_info.get('duration_seconds', 12),
        }

    def _download_product_image(self, image_url, deal_id):
        """Descarga la imagen del producto con retry y validación."""
        dest = os.path.join(self.video_dir, "public", "product.jpg")
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.get(image_url, headers=headers, timeout=20)

                if resp.status_code != 200:
                    raise Exception(f"HTTP {resp.status_code}")

                content = resp.content
                content_len = len(content)

                # Validar tamaño mínimo (evitar 404 HTML pages disfrazadas)
                if content_len < 1000:
                    raise Exception(f"Muy pequeña ({content_len} bytes)")

                # Validar que es una imagen real (JPEG magic bytes)
                if not (content[:2] == b'\xff\xd8' or  # JPEG
                        content[:8] == b'\x89PNG\r\n\x1a\n' or  # PNG
                        content[:4] == b'RIFF'):  # WebP
                    raise Exception("No es una imagen válida (magic bytes incorrectos)")

                with open(dest, 'wb') as f:
                    f.write(content)

                print(f"   📷 Imagen descargada: {content_len} bytes -> {dest}")
                return "product.jpg"

            except Exception as e:
                last_error = e
                print(f"   ⚠️ Intento {attempt}/{self.max_retries} falló: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff: 2s, 4s, 8s

        # Fallback: usar placeholder si todos los intentos fallan
        print(f"   ⚠️ Usando imagen placeholder para deal {deal_id}")
        return self._get_or_create_placeholder()

    def _get_or_create_placeholder(self):
        """Crea una imagen placeholder si no existe y devuelve su nombre."""
        placeholder_path = os.path.join(self.video_dir, "public", "placeholder.jpg")

        if not os.path.exists(placeholder_path):
            try:
                from PIL import Image, ImageDraw, ImageFont
                # Crear imagen con gradiente de marca
                img = Image.new('RGB', (700, 700), color='#1a1a2e')
                draw = ImageDraw.Draw(img)

                # Gradiente simple (franjas)
                for i in range(700):
                    ratio = i / 700
                    r = int(26 + (34 - 26) * ratio)
                    g = int(26 + (87 - 26) * ratio)
                    b = int(46 + (122 - 46) * ratio)
                    draw.line([(0, i), (700, i)], fill=(r, g, b))

                # Texto centrado
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                except OSError:
                    font = ImageFont.load_default()

                text = "OFERTA"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (700 - text_width) // 2
                y = (700 - text_height) // 2
                draw.text((x, y), text, fill='#facc15', font=font)

                img.save(placeholder_path, 'JPEG', quality=85)
                print(f"   📷 Placeholder creado: {placeholder_path}")

            except ImportError:
                # Sin PIL: crear JPEG mínimo válido (1x1 pixel gris)
                minimal_jpeg = bytes([
                    0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
                    0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
                    0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
                    0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
                    0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
                    0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
                    0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
                    0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
                    0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x1F, 0x00, 0x00,
                    0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x09, 0x0A, 0x0B, 0xFF, 0xC4, 0x00, 0xB5, 0x10, 0x00, 0x02, 0x01, 0x03,
                    0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7D,
                    0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06,
                    0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08,
                    0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0, 0x24, 0x33, 0x62, 0x72,
                    0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28,
                    0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45,
                    0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
                    0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75,
                    0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
                    0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3,
                    0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6,
                    0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9,
                    0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2,
                    0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4,
                    0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01,
                    0x00, 0x00, 0x3F, 0x00, 0xFB, 0xD5, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xD9
                ])
                with open(placeholder_path, 'wb') as f:
                    f.write(minimal_jpeg)
                print(f"   📷 Placeholder mínimo creado: {placeholder_path}")

        return "placeholder.jpg"

    def _map_category(self, deal_data):
        """Mapea categoría del deal a categoría de video."""
        title = (deal_data.get('title') or '').lower()
        cat = (deal_data.get('category') or '').lower()
        combined = f"{title} {cat}"

        if any(w in combined for w in ['cocina', 'estufa', 'hornillo', 'sartén', 'olla']):
            return 'cocina-camping'
        elif any(w in combined for w in ['saco', 'dormir', 'colchón', 'esterilla', 'almohada']):
            return 'dormir'
        elif any(w in combined for w in ['mochila', 'bolsa', 'petate']):
            return 'mochilas'
        elif any(w in combined for w in ['linterna', 'frontal', 'luz', 'solar', 'panel']):
            return 'iluminacion'
        elif any(w in combined for w in ['tienda', 'carpa', 'toldo', 'hamaca']):
            return 'tiendas'
        elif any(w in combined for w in ['agua', 'filtro', 'botella', 'cantimplora']):
            return 'hidratacion'
        return 'camping'

    def generate_remotion_video(self, deal_data):
        """Genera un video profesional con Remotion (React) + voz AI opcional."""
        image_url = deal_data.get('image_url')
        if not image_url:
            raise Exception("No hay URL de imagen")

        title = deal_data.get('marketing_title') or deal_data.get('title') or 'Oferta Camping'
        price = deal_data.get('price')
        original_price = deal_data.get('original_price')
        discount = deal_data.get('discount')

        # 1. Descargar imagen al public/ de Remotion
        print(f"   🔨 Renderizando video Remotion para: {title}")
        image_filename = self._download_product_image(image_url, deal_data.get('id'))

        # 2. Generar audio TTS (si está habilitado)
        audio_data = None
        if self.enable_tts:
            try:
                audio_data = self._generate_talking_product_audio(deal_data)
            except Exception as e:
                print(f"   ⚠️ Error generando audio TTS: {e}")
                audio_data = None

        # 3. Preparar props
        affiliate_url = deal_data.get('affiliate_url') or deal_data.get('url') or ''
        props = {
            "title": title[:80],
            "imageUrl": image_filename,
            "price": float(price) if price else 0,
            "category": self._map_category(deal_data),
        }
        if original_price:
            props["originalPrice"] = float(original_price)
        if discount:
            props["discount"] = int(discount)
        if affiliate_url:
            props["affiliateUrl"] = affiliate_url

        # Añadir datos de audio si existen
        if audio_data:
            props["audioFile"] = audio_data["audio_file"]
            props["dialogueSegments"] = audio_data["dialogue_segments"]
            print(f"   🎤 Video con voz: '{audio_data['full_script'][:50]}...'")

        # Escribir props a archivo temporal (evita problemas de shell escaping)
        props_path = os.path.join(self.temp_dir, "remotion_props.json")
        with open(props_path, 'w') as f:
            json.dump(props, f, ensure_ascii=False)

        # 4. Renderizar con Remotion CLI
        deal_id = deal_data.get('id') or str(uuid.uuid4())[:8]
        output_filename = f"video_{deal_id}.mp4"
        output_path = os.path.join(self.temp_dir, output_filename)

        cmd = [
            "npx", "remotion", "render",
            "DealVideo",
            output_path,
            f"--props={props_path}",
            f"--concurrency={self.remotion_concurrency}",
        ]

        print(f"   ▶️  Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=self.video_dir,
            capture_output=True,
            text=True,
            timeout=self.remotion_timeout,
        )

        if result.returncode != 0:
            print(f"   ❌ Remotion stderr: {result.stderr[-500:]}")
            raise Exception(f"Remotion render falló (exit {result.returncode})")

        file_size = os.path.getsize(output_path)
        print(f"   ✅ Video Remotion generado: {output_path} ({file_size // 1024}KB)")

        # Limpiar archivo de audio temporal
        if audio_data:
            audio_path = os.path.join(self.video_dir, "public", audio_data["audio_file"])
            if os.path.exists(audio_path):
                os.remove(audio_path)

        return output_path

    def upload_to_tiktok(self, video_path, deal_data):
        """Sube a TikTok via API."""
        title = deal_data.get('marketing_title') or deal_data.get('title') or ''
        affiliate_url = deal_data.get('affiliate_url') or deal_data.get('url') or ''

        # Construir caption con link de afiliado
        parts = [f"{title} 🔥"]
        if affiliate_url:
            parts.append(f"🛒 {affiliate_url}")
        parts.append("#camping #ofertas #amazon #outdoor")
        caption = " ".join(parts)

        print(f"   🚀 Iniciando subida a TikTok: {caption}")

        success = self.uploader.upload_video(video_path, caption)

        if success:
            print("   ✅ Publicado exitosamente.")
        else:
            print("   ❌ Falló la subida.")

    def close(self):
        self.uploader.close()


if __name__ == "__main__":
    manager = SocialManager(enable_tts=True)
    manager.process_deal({
        "title": "Lixada Hornillo Camping Gas Portátil",
        "marketing_title": "Hornillo PRO para aventureros",
        "id": "test123",
        "image_url": "https://m.media-amazon.com/images/I/61jlrkrWhiL._AC_SL1000_.jpg",
        "price": 14.99,
        "original_price": 19.99,
        "discount": 25,
        "category": "cocina-camping",
    })
    manager.close()
