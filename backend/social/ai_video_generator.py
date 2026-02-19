"""
AI Video Generator - Genera videos profesionales con producto animado + voz.

Usa servicios gratuitos:
1. Hugging Face Spaces (Stable Video Diffusion) - Anima la imagen del producto
2. gTTS/Edge TTS - Genera la voz del producto
3. FFmpeg - Combina video animado + audio

El resultado: Un video donde el producto "cobra vida" y habla al espectador.
"""

import os
import sys
import time
import base64
import tempfile
import subprocess
import requests
from typing import Optional, Dict
from io import BytesIO

# Intentar importar gradio_client para HuggingFace Spaces
try:
    from gradio_client import Client, handle_file
    HAS_GRADIO_CLIENT = True
except ImportError:
    HAS_GRADIO_CLIENT = False
    print("   ⚠️ gradio_client no instalado. Instalar con: pip install gradio_client")

# Intentar importar PIL para procesamiento de imágenes
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AIVideoGenerator:
    """
    Genera videos profesionales donde el producto cobra vida.

    Pipeline:
    1. Descarga y prepara la imagen del producto
    2. Usa Stable Video Diffusion (HuggingFace) para animar la imagen
    3. Genera audio TTS con el diálogo
    4. Combina video + audio con FFmpeg
    5. Añade loop si es necesario para alcanzar duración mínima
    """

    # Espacios de HuggingFace para image-to-video (gratis)
    HF_SPACES = [
        "multimodalart/stable-video-diffusion",  # SVD 1.1 - Principal
        "stabilityai/stable-video-diffusion",     # SVD oficial (puede tener cola)
    ]

    # Plantillas de diálogo por categoría
    DIALOGUE_TEMPLATES = {
        "cocina-camping": [
            "¡Oye! ¿Sigues cocinando con esa cosa vieja? ¡Mírame! Soy potente, compacto y perfecto para tu aventura. ¡Llévame contigo!",
            "¡Para para para! ¿En serio vas a dejarme aquí? Soy el hornillo que necesitas. ¡Mira qué bonito soy! ¡Cómprame ya!",
        ],
        "dormir": [
            "¡Brrr! ¿Todavía pasas frío por las noches? ¡Yo te abrigo hasta en las peores condiciones! Sácame de aquí y llévame al monte.",
            "¡Oye aventurero! Tu viejo saco ya no da más. Mírame, soy cómodo, calentito y te espero. ¿Qué dices?",
        ],
        "mochilas": [
            "¡Ey! ¿Esa mochila vieja otra vez? ¡Mírame! Soy cómoda, resistente, y tu espalda me lo va a agradecer. ¡Vamos!",
            "¡Tu próxima aventura me necesita! Soy espaciosa, ligera y estoy lista para acompañarte. ¡Dale, llévame!",
        ],
        "hidratacion": [
            "¡Basta de agua tibia! Yo mantengo tu bebida fría todo el día. Soy de acero, soy resistente. ¡Adóptame!",
            "¿Cuántas botellas has perdido ya? Yo no me rompo, no pierdo líquido. ¡Soy la última botella que necesitarás!",
        ],
        "iluminacion": [
            "¡OSCURIDAD! ¿Te da miedo? ¡Pues yo la destruyo! Soy potente, recargable y cubro todo tu campamento. ¡Cómprame!",
            "¡Sin luz no hay aventura! Yo ilumino tu camino, tu tienda, tu vida. ¿Qué esperas? ¡Llévame!",
        ],
        "default": [
            "¡Oye tú! Sí, TÚ. ¡Mírame! Soy exactamente lo que necesitas para tu próxima aventura. ¿Qué esperas? ¡Cómprame ya!",
            "¡Para! ¿Vas a dejarme aquí? Soy increíble, soy útil, y estoy esperándote. ¡Dale, llévame contigo!",
        ],
    }

    def __init__(self):
        """Inicializa el generador."""
        self.hf_client = None
        self._init_hf_client()

    def _init_hf_client(self):
        """Inicializa el cliente de HuggingFace Spaces."""
        if not HAS_GRADIO_CLIENT:
            print("   ⚠️ HuggingFace Spaces no disponible (falta gradio_client)")
            return

        # Intentar conectar a cada Space
        for space in self.HF_SPACES:
            try:
                print(f"   🔌 Conectando a HuggingFace Space: {space}...")
                self.hf_client = Client(space, hf_token=os.getenv("HUGGINGFACE_API_KEY"))
                print(f"   ✅ Conectado a {space}")
                self.active_space = space
                return
            except Exception as e:
                print(f"   ⚠️ No se pudo conectar a {space}: {e}")
                continue

        print("   ❌ No se pudo conectar a ningún Space de HuggingFace")

    def _get_dialogue_for_category(self, category: str) -> str:
        """Obtiene un diálogo según la categoría del producto."""
        import random

        category_lower = category.lower() if category else ""

        for key, dialogues in self.DIALOGUE_TEMPLATES.items():
            if key in category_lower or category_lower in key:
                return random.choice(dialogues)

        return random.choice(self.DIALOGUE_TEMPLATES["default"])

    def _download_image(self, image_url: str, output_path: str) -> bool:
        """Descarga una imagen y la guarda localmente."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            return True
        except Exception as e:
            print(f"   ❌ Error descargando imagen: {e}")
            return False

    def _prepare_image(self, image_path: str, target_size: tuple = (1024, 576)) -> str:
        """
        Prepara la imagen para SVD (redimensiona y ajusta aspect ratio).
        SVD funciona mejor con 1024x576 (16:9) o 576x1024 (9:16).
        """
        if not HAS_PIL:
            return image_path  # Sin PIL, usar imagen original

        try:
            img = Image.open(image_path)

            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Calcular nuevo tamaño manteniendo aspect ratio
            original_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]

            if original_ratio > target_ratio:
                # Imagen más ancha - ajustar por altura
                new_height = target_size[1]
                new_width = int(new_height * original_ratio)
            else:
                # Imagen más alta - ajustar por ancho
                new_width = target_size[0]
                new_height = int(new_width / original_ratio)

            # Redimensionar
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Recortar al centro para obtener tamaño exacto
            left = (new_width - target_size[0]) // 2
            top = (new_height - target_size[1]) // 2
            right = left + target_size[0]
            bottom = top + target_size[1]
            img = img.crop((left, top, right, bottom))

            # Guardar imagen preparada
            prepared_path = image_path.replace(".jpg", "_prepared.jpg").replace(".png", "_prepared.png")
            if prepared_path == image_path:
                prepared_path = image_path + "_prepared.jpg"

            img.save(prepared_path, "JPEG", quality=95)
            print(f"   📐 Imagen preparada: {target_size[0]}x{target_size[1]}")

            return prepared_path

        except Exception as e:
            print(f"   ⚠️ Error preparando imagen: {e}")
            return image_path

    def _generate_video_svd(self, image_path: str, output_path: str, motion: int = 127) -> bool:
        """
        Genera video usando Stable Video Diffusion via HuggingFace Spaces.

        Args:
            image_path: Ruta a la imagen de entrada
            output_path: Ruta donde guardar el video
            motion: Intensidad del movimiento (1-255, default 127)

        Returns:
            True si el video se generó exitosamente
        """
        if not self.hf_client:
            print("   ❌ Cliente HuggingFace no disponible")
            return False

        try:
            print(f"   🎬 Generando video con SVD (motion={motion})...")
            start_time = time.time()

            # Llamar a la API del Space
            result = self.hf_client.predict(
                image=handle_file(image_path),
                seed=0,  # Random seed
                randomize_seed=True,
                motion_bucket_id=motion,
                fps_id=6,  # 6 FPS para SVD
                api_name="/video"
            )

            elapsed = time.time() - start_time
            print(f"   ⏱️ Video generado en {elapsed:.1f}s")

            # El resultado puede ser una ruta de archivo o una tupla
            if isinstance(result, tuple):
                video_result = result[0]  # Primer elemento suele ser el video
            else:
                video_result = result

            # Si es una ruta, copiar al destino
            if isinstance(video_result, str) and os.path.exists(video_result):
                import shutil
                shutil.copy(video_result, output_path)
                print(f"   ✅ Video SVD guardado: {output_path}")
                return True

            # Si es un dict con 'video' key
            if isinstance(video_result, dict) and 'video' in video_result:
                video_url = video_result['video']
                if video_url.startswith('http'):
                    # Descargar video
                    response = requests.get(video_url, timeout=120)
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    return True

            print(f"   ⚠️ Resultado inesperado: {type(video_result)}")
            return False

        except Exception as e:
            print(f"   ❌ Error generando video SVD: {e}")
            return False

    def _generate_tts_audio(self, text: str, output_path: str) -> bool:
        """Genera audio TTS usando gTTS (gratis y funciona en CI)."""
        try:
            from gtts import gTTS

            print(f"   🔊 Generando audio: '{text[:50]}...'")
            tts = gTTS(text=text, lang='es', slow=False)
            tts.save(output_path)

            file_size = os.path.getsize(output_path)
            print(f"   ✅ Audio TTS generado: {file_size // 1024}KB")
            return True

        except Exception as e:
            print(f"   ❌ Error generando TTS: {e}")
            return False

    def _get_media_duration(self, file_path: str) -> float:
        """Obtiene la duración de un archivo de audio/video usando ffprobe."""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return float(result.stdout.strip())
        except Exception as e:
            print(f"   ⚠️ Error obteniendo duración: {e}")
            return 0.0

    def _combine_video_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        target_duration: float = None
    ) -> bool:
        """
        Combina video y audio usando FFmpeg.
        Si el audio es más largo que el video, hace loop del video.
        """
        try:
            video_duration = self._get_media_duration(video_path)
            audio_duration = self._get_media_duration(audio_path)

            print(f"   📹 Video: {video_duration:.1f}s, Audio: {audio_duration:.1f}s")

            # Determinar duración objetivo
            if target_duration:
                final_duration = target_duration
            else:
                final_duration = max(audio_duration, 5.0)  # Mínimo 5 segundos

            # Construir comando FFmpeg
            if video_duration < final_duration:
                # Loop del video para alcanzar duración del audio
                loops = int(final_duration / video_duration) + 1
                cmd = [
                    "ffmpeg", "-y",
                    "-stream_loop", str(loops),
                    "-i", video_path,
                    "-i", audio_path,
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-shortest",
                    "-t", str(final_duration),
                    "-pix_fmt", "yuv420p",
                    "-preset", "fast",
                    output_path
                ]
            else:
                # Video suficientemente largo
                cmd = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-i", audio_path,
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-shortest",
                    "-pix_fmt", "yuv420p",
                    "-preset", "fast",
                    output_path
                ]

            print(f"   🔧 Combinando video + audio...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                print(f"   ❌ FFmpeg error: {result.stderr[-500:]}")
                return False

            final_size = os.path.getsize(output_path)
            print(f"   ✅ Video final: {output_path} ({final_size // 1024}KB)")
            return True

        except Exception as e:
            print(f"   ❌ Error combinando video/audio: {e}")
            return False

    def generate_product_video(
        self,
        deal_data: dict,
        output_path: str,
        custom_dialogue: str = None,
    ) -> Optional[Dict]:
        """
        Genera un video profesional donde el producto cobra vida y habla.

        Args:
            deal_data: Datos del producto (title, category, price, image_url, etc.)
            output_path: Ruta donde guardar el video final
            custom_dialogue: Diálogo personalizado (opcional)

        Returns:
            Dict con información del video si exitoso, None si falla
        """
        if not self.hf_client:
            raise Exception("HuggingFace client no disponible")

        title = deal_data.get("title", "Producto")
        image_url = deal_data.get("image_url")
        category = deal_data.get("category", "default")

        if not image_url:
            raise Exception("No hay URL de imagen")

        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp(prefix="ai_video_")

        try:
            # 1. Descargar imagen
            image_path = os.path.join(temp_dir, "product.jpg")
            print(f"   📷 Descargando imagen...")
            if not self._download_image(image_url, image_path):
                raise Exception("No se pudo descargar la imagen")

            # 2. Preparar imagen (redimensionar para SVD)
            prepared_image = self._prepare_image(image_path, target_size=(576, 1024))  # 9:16 para TikTok

            # 3. Generar video con SVD
            svd_video_path = os.path.join(temp_dir, "svd_video.mp4")
            if not self._generate_video_svd(prepared_image, svd_video_path, motion=150):
                raise Exception("No se pudo generar video con SVD")

            # 4. Generar diálogo
            dialogue = custom_dialogue or self._get_dialogue_for_category(category)

            # 5. Generar audio TTS
            audio_path = os.path.join(temp_dir, "dialogue.mp3")
            if not self._generate_tts_audio(dialogue, audio_path):
                raise Exception("No se pudo generar audio TTS")

            # 6. Combinar video + audio
            if not self._combine_video_audio(svd_video_path, audio_path, output_path):
                raise Exception("No se pudo combinar video y audio")

            return {
                "video_path": output_path,
                "dialogue": dialogue,
                "duration": self._get_media_duration(output_path),
                "status": "success",
            }

        finally:
            # Limpiar archivos temporales
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

    def is_available(self) -> bool:
        """Verifica si el generador está disponible."""
        return self.hf_client is not None


def generate_dialogue_for_product(deal_data: dict) -> str:
    """Genera un diálogo persuasivo para el producto."""
    generator = AIVideoGenerator()
    category = deal_data.get("category", "default")
    return generator._get_dialogue_for_category(category)


def is_ai_video_enabled() -> bool:
    """Verifica si el generador de video AI está disponible."""
    return HAS_GRADIO_CLIENT


# Test
if __name__ == "__main__":
    print("🎬 Test de AI Video Generator")

    generator = AIVideoGenerator()

    if not generator.is_available():
        print("❌ Generador no disponible")
        exit(1)

    test_deal = {
        "title": "Saco de Dormir Invierno -28°C",
        "category": "dormir",
        "price": 89.99,
        "image_url": "https://m.media-amazon.com/images/I/71xQhKPGDZL._AC_SL1500_.jpg",
    }

    result = generator.generate_product_video(
        deal_data=test_deal,
        output_path="/tmp/test_ai_video.mp4",
    )

    if result:
        print(f"✅ Video generado: {result}")
    else:
        print("❌ Falló la generación")
