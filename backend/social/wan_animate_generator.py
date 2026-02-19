"""
Wan2.2 Animate Video Generator - Producto gesticulando (GRATIS)

Usa HuggingFace Spaces para animar productos con movimientos
humanos extraídos de videos plantilla.

Basado en: https://huggingface.co/spaces/Wan-AI/Wan2.2-Animate
"""
import os
import time
import tempfile
import requests
from pathlib import Path

try:
    from gradio_client import Client, handle_file
    HAS_GRADIO = True
except ImportError:
    HAS_GRADIO = False


def is_wan_animate_enabled() -> bool:
    """Verifica si Wan Animate está habilitado."""
    if not HAS_GRADIO:
        return False
    return os.environ.get("ENABLE_WAN_ANIMATE", "true").lower() in {"1", "true", "yes", "on"}


class WanAnimateGenerator:
    """
    Genera videos con Wan2.2 Animate donde el producto se mueve
    con gestos humanos extraídos de videos plantilla.
    """

    # Spaces disponibles
    SPACES = [
        "Wan-AI/Wan2.2-Animate",
        "alexnasa/Wan2.2-Animate-ZEROGPU",
    ]

    # Gestos disponibles (mapeo a URLs de videos de ejemplo)
    # Estos son videos cortos de personas gesticulando
    GESTURE_URLS = {
        "excited": "https://huggingface.co/spaces/Wan-AI/Wan2.2-Animate/resolve/main/examples/driving/pose2.mp4",
        "presenting": "https://huggingface.co/spaces/Wan-AI/Wan2.2-Animate/resolve/main/examples/driving/pose1.mp4",
        "waving": "https://huggingface.co/spaces/Wan-AI/Wan2.2-Animate/resolve/main/examples/driving/pose3.mp4",
    }

    # Mapeo de categorías de producto a gestos
    CATEGORY_TO_GESTURE = {
        "cocina-camping": "excited",      # Emocionado por cocinar
        "dormir": "presenting",           # Presentando comodidad
        "mochilas": "excited",            # Aventura emocionante
        "hidratacion": "waving",          # Saludo amigable
        "iluminacion": "presenting",      # Mostrando la luz
        "tiendas": "excited",             # Emoción por acampar
    }

    def __init__(self):
        self.client = None
        self.connected_space = None
        self.temp_dir = tempfile.gettempdir()
        self._connect_to_space()

    def _connect_to_space(self):
        """Intenta conectar a un Space de HuggingFace disponible."""
        if not HAS_GRADIO:
            print("   ⚠️ gradio_client no instalado")
            return

        for space in self.SPACES:
            try:
                print(f"   🔗 Conectando a {space}...")
                self.client = Client(space, verbose=False)
                self.connected_space = space
                print(f"   ✅ Conectado a {space}")
                return
            except Exception as e:
                print(f"   ⚠️ {space} no disponible: {e}")
                continue

        print("   ❌ No se pudo conectar a ningún Space de Wan Animate")

    def is_available(self) -> bool:
        """Verifica si el generador está disponible."""
        return self.client is not None

    def _download_gesture_video(self, gesture_type: str) -> str:
        """Descarga video de gesto de ejemplo."""
        url = self.GESTURE_URLS.get(gesture_type, self.GESTURE_URLS["excited"])
        output_path = os.path.join(self.temp_dir, f"gesture_{gesture_type}.mp4")

        # Usar cache si existe
        if os.path.exists(output_path):
            return output_path

        try:
            print(f"   📥 Descargando gesto '{gesture_type}'...")
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(resp.content)

            print(f"   📹 Gesto descargado: {len(resp.content) // 1024}KB")
            return output_path

        except Exception as e:
            print(f"   ⚠️ Error descargando gesto: {e}")
            return None

    def generate_video(
        self,
        image_path: str,
        gesture_type: str = "excited",
        output_path: str = None,
        mode: str = "animation",
        timeout: int = 600,
    ) -> bool:
        """
        Genera un video donde el producto se mueve con gestos humanos.

        Args:
            image_path: Ruta a la imagen del producto
            gesture_type: Tipo de gesto (excited, presenting, waving)
            output_path: Donde guardar el video resultado
            mode: "animation" (animar imagen) o "replacement" (reemplazar persona)
            timeout: Timeout en segundos

        Returns:
            True si se generó exitosamente
        """
        if not self.is_available():
            print("   ❌ Wan Animate no disponible")
            return False

        if not output_path:
            output_path = os.path.join(self.temp_dir, "wan_output.mp4")

        # Descargar video de gesto
        gesture_video = self._download_gesture_video(gesture_type)
        if not gesture_video:
            print("   ❌ No se pudo obtener video de gesto")
            return False

        try:
            print(f"   🎬 Generando video Wan Animate...")
            print(f"      Imagen: {image_path}")
            print(f"      Gesto: {gesture_type}")
            print(f"      Modo: {mode}")

            # Verificar imagen
            if not os.path.exists(image_path):
                print(f"   ❌ Imagen no existe: {image_path}")
                return False

            start_time = time.time()

            # Llamar a Wan Animate
            # API típica: predict(character_image, driving_video, mode)
            result = self.client.predict(
                character_image=handle_file(image_path),
                driving_video=handle_file(gesture_video),
                mode=mode,
                api_name="/generate"
            )

            elapsed = time.time() - start_time
            print(f"   ⏱️ Generación completada en {elapsed:.1f}s")

            # El resultado puede ser una ruta al video o una tupla
            video_result = result[0] if isinstance(result, (list, tuple)) else result

            if video_result and os.path.exists(str(video_result)):
                import shutil
                shutil.copy(str(video_result), output_path)

                file_size = os.path.getsize(output_path)
                print(f"   ✅ Video Wan Animate: {output_path} ({file_size // 1024}KB)")
                return True
            else:
                print(f"   ❌ No se obtuvo video válido: {result}")
                return False

        except Exception as e:
            print(f"   ❌ Error Wan Animate: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_from_deal(
        self,
        deal_data: dict,
        output_path: str,
        audio_path: str = None,
        temp_dir: str = None,
    ) -> bool:
        """
        Genera video Wan Animate desde datos de oferta.

        Args:
            deal_data: Diccionario con imagen_url, categoría, etc.
            output_path: Donde guardar el video
            audio_path: Audio TTS para combinar (opcional)
            temp_dir: Directorio temporal

        Returns:
            True si se generó exitosamente
        """
        image_url = deal_data.get("image_url")
        if not image_url:
            print("   ❌ No hay URL de imagen en deal_data")
            return False

        temp_dir = temp_dir or self.temp_dir
        image_path = os.path.join(temp_dir, "wan_input.jpg")

        # Descargar imagen
        try:
            print(f"   📥 Descargando imagen: {image_url[:60]}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                              'AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            }
            resp = requests.get(image_url, headers=headers, timeout=30)
            resp.raise_for_status()

            with open(image_path, 'wb') as f:
                f.write(resp.content)

            print(f"   📷 Imagen descargada: {len(resp.content) // 1024}KB")

        except Exception as e:
            print(f"   ❌ Error descargando imagen: {e}")
            return False

        # Seleccionar gesto según categoría
        category = deal_data.get("category", "").lower()
        gesture = self.CATEGORY_TO_GESTURE.get(category, "excited")
        print(f"   🎭 Categoría '{category}' → Gesto '{gesture}'")

        # Generar video sin audio primero
        video_no_audio = os.path.join(temp_dir, "wan_no_audio.mp4")
        success = self.generate_video(
            image_path=image_path,
            gesture_type=gesture,
            output_path=video_no_audio,
        )

        if not success:
            return False

        # Si hay audio, combinar con FFmpeg
        if audio_path and os.path.exists(audio_path):
            return self._combine_with_audio(video_no_audio, audio_path, output_path)
        else:
            import shutil
            shutil.copy(video_no_audio, output_path)
            return True

    def _combine_with_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
    ) -> bool:
        """Combina video con audio TTS usando FFmpeg."""
        import subprocess

        try:
            print(f"   🔊 Combinando video + audio...")

            # Obtener duración del audio
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 5.0

            # Obtener duración del video
            probe_cmd[5] = video_path
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            video_duration = float(result.stdout.strip()) if result.stdout.strip() else 5.0

            # Calcular loops necesarios
            final_duration = max(audio_duration, 5.0)
            loops = int(final_duration / video_duration) + 1

            # Combinar con FFmpeg
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", str(loops),
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                "-t", str(final_duration),
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"   ✅ Video final: {output_path} ({file_size // 1024}KB)")
                return True
            else:
                print(f"   ❌ FFmpeg error: {result.stderr[:500]}")
                return False

        except Exception as e:
            print(f"   ❌ Error combinando: {e}")
            return False


# Test
if __name__ == "__main__":
    print("🎬 Test Wan Animate Generator")
    print(f"   Habilitado: {is_wan_animate_enabled()}")

    if is_wan_animate_enabled():
        gen = WanAnimateGenerator()
        print(f"   Disponible: {gen.is_available()}")
        print(f"   Space conectado: {gen.connected_space}")
