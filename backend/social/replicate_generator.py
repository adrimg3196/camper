"""
Replicate Video Generator - Genera videos AI animados usando Replicate.

Usa modelos de Replicate para convertir imágenes de productos en videos animados.
Opciones disponibles:
- minimax/video-01 (Hailuo) - Mejor calidad, ~$0.50/video
- wan-video/wan-2.5-i2v-fast - Rápido y económico
- stability-ai/stable-video-diffusion - Clásico SVD
"""

import os
import sys
import time
import base64
import tempfile
import subprocess
import requests
from typing import Optional, Dict

# Intentar importar replicate
try:
    import replicate
    HAS_REPLICATE = True
except ImportError:
    HAS_REPLICATE = False
    print("   ⚠️ replicate no instalado. Instalar con: pip install replicate")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configuración
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# Modelos disponibles (ordenados por calidad/costo)
MODELS = {
    # Modelo rápido y económico - Wan 2.5
    "wan-fast": {
        "id": "wan-video/wan-2.5-i2v-480p",
        "description": "Wan 2.5 - Rápido y económico",
        "cost_approx": "$0.05",
    },
    # Modelo de alta calidad - Minimax Hailuo
    "hailuo": {
        "id": "minimax/video-01",
        "description": "Hailuo/Minimax - Alta calidad",
        "cost_approx": "$0.50",
    },
    # Stable Video Diffusion clásico
    "svd": {
        "id": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        "description": "Stable Video Diffusion",
        "cost_approx": "$0.18",
    },
}

# Modelo por defecto (el más económico)
DEFAULT_MODEL = "wan-fast"


class ReplicateVideoGenerator:
    """
    Genera videos animados usando la API de Replicate.
    El producto cobra vida con movimiento fluido.
    """

    # Plantillas de prompts por categoría
    ANIMATION_PROMPTS = {
        "cocina-camping": "The camping stove comes to life, flame ignites with a warm glow, steam rises gently, the product rotates slowly showing all angles, professional product photography lighting, smooth cinematic motion",
        "dormir": "The sleeping bag unfolds magically, fabric ripples like waves, zipper moves smoothly, cozy warm atmosphere, soft lighting, gentle floating motion, premium product showcase",
        "mochilas": "The backpack floats and rotates elegantly, straps sway gently, zippers open to reveal compartments, adventure spirit, dynamic lighting, professional product video",
        "hidratacion": "The water bottle rotates smoothly, condensation droplets form and slide down, refreshing splash effect, crystal clear water visible inside, premium product lighting",
        "iluminacion": "The flashlight powers on dramatically, light beam cuts through darkness, lens flares, the product rotates to show design, cinematic lighting transition",
        "tiendas": "The tent unfolds and assembles itself in stop-motion style, fabric ripples in gentle breeze, camping atmosphere, golden hour lighting, professional showcase",
        "default": "The product comes to life with smooth rotation, professional studio lighting, gentle floating motion, premium product showcase, cinematic quality",
    }

    # Diálogos para TTS
    DIALOGUE_TEMPLATES = {
        "cocina-camping": [
            "¡Oye! ¿Sigues cocinando con esa cosa vieja? ¡Mírame! Soy potente, compacto y perfecto para tu aventura. ¡Llévame contigo!",
            "¡Para! ¿En serio vas a dejarme aquí? Soy el hornillo que necesitas. ¡Cómprame ya!",
        ],
        "dormir": [
            "¡Brrr! ¿Todavía pasas frío por las noches? ¡Yo te abrigo hasta en las peores condiciones! ¡Sácame de aquí!",
            "¡Oye aventurero! Tu viejo saco ya no da más. Mírame, soy cómodo, calentito y te espero.",
        ],
        "mochilas": [
            "¡Ey! ¿Esa mochila vieja otra vez? ¡Mírame! Soy cómoda, resistente, y tu espalda me lo agradecerá.",
            "¡Tu próxima aventura me necesita! Soy espaciosa, ligera y lista para acompañarte.",
        ],
        "hidratacion": [
            "¡Basta de agua tibia! Yo mantengo tu bebida fría todo el día. ¡Soy de acero, adóptame!",
            "¿Cuántas botellas has perdido ya? Yo no me rompo. ¡Soy la última que necesitarás!",
        ],
        "iluminacion": [
            "¡OSCURIDAD! ¿Te da miedo? ¡Pues yo la destruyo! Soy potente y recargable. ¡Cómprame!",
            "¡Sin luz no hay aventura! Yo ilumino tu camino. ¿Qué esperas? ¡Llévame!",
        ],
        "default": [
            "¡Oye tú! ¡Mírame! Soy exactamente lo que necesitas para tu próxima aventura. ¡Cómprame ya!",
            "¡Para! ¿Vas a dejarme aquí? Soy increíble y estoy esperándote. ¡Llévame contigo!",
        ],
    }

    def __init__(self, model_key: str = DEFAULT_MODEL):
        """Inicializa el generador de Replicate."""
        self.api_token = REPLICATE_API_TOKEN
        self.model_key = model_key
        self.model_config = MODELS.get(model_key, MODELS[DEFAULT_MODEL])

        if self.api_token:
            os.environ["REPLICATE_API_TOKEN"] = self.api_token
            print(f"   🎬 Replicate configurado: {self.model_config['description']}")
        else:
            print("   ⚠️ REPLICATE_API_TOKEN no configurado")

    def _get_animation_prompt(self, category: str, title: str) -> str:
        """Genera el prompt de animación según la categoría."""
        category_lower = category.lower() if category else ""

        for key, prompt in self.ANIMATION_PROMPTS.items():
            if key in category_lower:
                return f"{title}. {prompt}"

        return f"{title}. {self.ANIMATION_PROMPTS['default']}"

    def _get_dialogue(self, category: str) -> str:
        """Obtiene un diálogo según la categoría."""
        import random
        category_lower = category.lower() if category else ""

        for key, dialogues in self.DIALOGUE_TEMPLATES.items():
            if key in category_lower:
                return random.choice(dialogues)

        return random.choice(self.DIALOGUE_TEMPLATES["default"])

    def _download_video(self, video_url: str, output_path: str) -> bool:
        """Descarga el video generado."""
        try:
            print(f"   📥 Descargando video...")
            response = requests.get(video_url, timeout=120, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            file_size = os.path.getsize(output_path)
            print(f"   ✅ Video descargado: {file_size // 1024}KB")
            return True

        except Exception as e:
            print(f"   ❌ Error descargando video: {e}")
            return False

    def _generate_tts_audio(self, text: str, output_path: str) -> bool:
        """Genera audio TTS usando gTTS."""
        try:
            from gtts import gTTS

            print(f"   🔊 Generando audio: '{text[:50]}...'")
            tts = gTTS(text=text, lang='es', slow=False)
            tts.save(output_path)

            file_size = os.path.getsize(output_path)
            print(f"   ✅ Audio TTS: {file_size // 1024}KB")
            return True

        except Exception as e:
            print(f"   ❌ Error generando TTS: {e}")
            return False

    def _get_media_duration(self, file_path: str) -> float:
        """Obtiene la duración de un archivo usando ffprobe."""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return float(result.stdout.strip())
        except:
            return 0.0

    def _combine_video_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> bool:
        """Combina video y audio con FFmpeg, haciendo loop del video si es necesario."""
        try:
            video_duration = self._get_media_duration(video_path)
            audio_duration = self._get_media_duration(audio_path)

            print(f"   📹 Video: {video_duration:.1f}s, Audio: {audio_duration:.1f}s")

            final_duration = max(audio_duration, 5.0)

            if video_duration < final_duration:
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
                print(f"   ❌ FFmpeg error: {result.stderr[-300:]}")
                return False

            return True

        except Exception as e:
            print(f"   ❌ Error combinando: {e}")
            return False

    def generate_video(
        self,
        deal_data: dict,
        output_path: str,
        add_audio: bool = True,
    ) -> Optional[Dict]:
        """
        Genera un video animado del producto usando Replicate.

        Args:
            deal_data: Datos del producto
            output_path: Ruta de salida
            add_audio: Si debe añadir audio TTS

        Returns:
            Dict con información del video si exitoso
        """
        if not HAS_REPLICATE:
            raise Exception("Módulo replicate no instalado")

        if not self.api_token:
            raise Exception("REPLICATE_API_TOKEN no configurado")

        title = deal_data.get("title", "Producto")
        category = deal_data.get("category", "default")
        image_url = deal_data.get("image_url")

        if not image_url:
            raise Exception("No hay URL de imagen")

        temp_dir = tempfile.mkdtemp(prefix="replicate_")

        try:
            # 1. Generar prompt de animación
            prompt = self._get_animation_prompt(category, title)
            print(f"   📝 Prompt: {prompt[:80]}...")

            # 2. Llamar a Replicate API
            print(f"   🎬 Generando video con {self.model_config['description']}...")
            start_time = time.time()

            # Configurar inputs según el modelo
            model_id = self.model_config["id"]

            if "wan-video" in model_id:
                # Wan Video models
                output = replicate.run(
                    model_id,
                    input={
                        "image": image_url,
                        "prompt": prompt,
                        "max_area": "480p",
                        "fast_mode": "Enabled",
                    }
                )
            elif "minimax" in model_id or "video-01" in model_id:
                # Minimax/Hailuo
                output = replicate.run(
                    model_id,
                    input={
                        "prompt": prompt,
                        "first_frame_image": image_url,
                    }
                )
            else:
                # Stable Video Diffusion y otros
                output = replicate.run(
                    model_id,
                    input={
                        "input_image": image_url,
                        "motion_bucket_id": 127,
                        "fps": 7,
                    }
                )

            elapsed = time.time() - start_time
            print(f"   ⏱️ Generado en {elapsed:.1f}s")

            # 3. Obtener URL del video
            if isinstance(output, list):
                video_url = output[0] if output else None
            elif hasattr(output, 'url'):
                video_url = output.url
            else:
                video_url = str(output)

            if not video_url:
                raise Exception("No se obtuvo URL de video")

            # 4. Descargar video
            raw_video_path = os.path.join(temp_dir, "raw_video.mp4")
            if not self._download_video(video_url, raw_video_path):
                raise Exception("Error descargando video")

            # 5. Añadir audio TTS si se solicita
            if add_audio:
                dialogue = self._get_dialogue(category)
                audio_path = os.path.join(temp_dir, "audio.mp3")

                if self._generate_tts_audio(dialogue, audio_path):
                    # Combinar video + audio
                    if self._combine_video_audio(raw_video_path, audio_path, output_path):
                        final_size = os.path.getsize(output_path)
                        print(f"   ✅ Video final con audio: {final_size // 1024}KB")
                    else:
                        # Si falla la combinación, usar video sin audio
                        import shutil
                        shutil.copy(raw_video_path, output_path)
                else:
                    import shutil
                    shutil.copy(raw_video_path, output_path)
            else:
                import shutil
                shutil.copy(raw_video_path, output_path)

            return {
                "video_path": output_path,
                "model": self.model_config["description"],
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
        return HAS_REPLICATE and bool(self.api_token)


def is_replicate_enabled() -> bool:
    """Verifica si Replicate está habilitado."""
    return HAS_REPLICATE and bool(os.getenv("REPLICATE_API_TOKEN"))


def generate_dialogue_for_replicate(deal_data: dict) -> str:
    """Genera un diálogo para el producto."""
    generator = ReplicateVideoGenerator()
    category = deal_data.get("category", "default")
    return generator._get_dialogue(category)


# Test
if __name__ == "__main__":
    print("🎬 Test de Replicate Video Generator")

    if not REPLICATE_API_TOKEN:
        print("❌ REPLICATE_API_TOKEN no configurado")
        exit(1)

    generator = ReplicateVideoGenerator()

    test_deal = {
        "title": "Saco de Dormir Invierno -28°C",
        "category": "dormir",
        "price": 89.99,
        "image_url": "https://m.media-amazon.com/images/I/71xQhKPGDZL._AC_SL1500_.jpg",
    }

    result = generator.generate_video(
        deal_data=test_deal,
        output_path="/tmp/test_replicate.mp4",
    )

    if result:
        print(f"✅ Video generado: {result}")
    else:
        print("❌ Falló la generación")
