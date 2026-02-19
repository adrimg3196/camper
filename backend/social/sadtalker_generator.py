"""
SadTalker Video Generator - Producto que habla (GRATIS)

Usa HuggingFace Spaces para generar videos donde el producto
"cobra vida" y habla sincronizado con audio TTS.

Basado en: https://huggingface.co/spaces/vinthony/SadTalker
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


def is_sadtalker_enabled() -> bool:
    """Verifica si SadTalker está habilitado."""
    if not HAS_GRADIO:
        return False
    return os.environ.get("ENABLE_SADTALKER", "true").lower() in {"1", "true", "yes", "on"}


class SadTalkerGenerator:
    """
    Genera videos con SadTalker donde el producto "habla".

    SadTalker anima una imagen estática para que parezca que está
    hablando, sincronizado con un audio de entrada.
    """

    # Spaces disponibles (orden de prioridad)
    SPACES = [
        "vinthony/SadTalker",
        "abreza/SadTalker",
    ]

    # Configuración por defecto
    DEFAULT_PREPROCESS = "crop"  # crop, resize, full
    DEFAULT_STILL_MODE = False   # True = menos movimiento
    DEFAULT_ENHANCER = "gfpgan"  # gfpgan, RestoreFormer, None

    def __init__(self):
        self.client = None
        self.connected_space = None
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

        print("   ❌ No se pudo conectar a ningún Space de SadTalker")

    def is_available(self) -> bool:
        """Verifica si el generador está disponible."""
        return self.client is not None

    def generate_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        preprocess: str = None,
        still_mode: bool = None,
        use_enhancer: bool = True,
        timeout: int = 300,
    ) -> bool:
        """
        Genera un video donde la imagen "habla" el audio.

        Args:
            image_path: Ruta a la imagen del producto
            audio_path: Ruta al audio TTS
            output_path: Donde guardar el video resultado
            preprocess: Modo de preprocesamiento (crop/resize/full)
            still_mode: True para menos movimiento
            use_enhancer: True para mejorar calidad facial
            timeout: Timeout en segundos

        Returns:
            True si se generó exitosamente
        """
        if not self.is_available():
            print("   ❌ SadTalker no disponible")
            return False

        preprocess = preprocess or self.DEFAULT_PREPROCESS
        still_mode = still_mode if still_mode is not None else self.DEFAULT_STILL_MODE
        enhancer = self.DEFAULT_ENHANCER if use_enhancer else None

        try:
            print(f"   🎭 Generando video SadTalker...")
            print(f"      Imagen: {image_path}")
            print(f"      Audio: {audio_path}")
            print(f"      Preprocess: {preprocess}, Still: {still_mode}")

            # Verificar archivos
            if not os.path.exists(image_path):
                print(f"   ❌ Imagen no existe: {image_path}")
                return False
            if not os.path.exists(audio_path):
                print(f"   ❌ Audio no existe: {audio_path}")
                return False

            start_time = time.time()

            # Llamar a SadTalker
            # La API típica de SadTalker en Gradio:
            # predict(source_image, driven_audio, preprocess, still_mode, use_enhancer, ...)
            result = self.client.predict(
                source_image=handle_file(image_path),
                driven_audio=handle_file(audio_path),
                preprocess=preprocess,
                still_mode=still_mode,
                use_enhancer=use_enhancer,
                batch_size=1,
                size=256,
                pose_style=0,
                api_name="/predict"
            )

            elapsed = time.time() - start_time
            print(f"   ⏱️ Generación completada en {elapsed:.1f}s")

            # El resultado puede ser una ruta al video o una tupla
            video_result = result[0] if isinstance(result, (list, tuple)) else result

            if video_result and os.path.exists(str(video_result)):
                # Copiar/mover al output_path
                import shutil
                shutil.copy(str(video_result), output_path)

                file_size = os.path.getsize(output_path)
                print(f"   ✅ Video SadTalker: {output_path} ({file_size // 1024}KB)")
                return True
            else:
                print(f"   ❌ No se obtuvo video válido: {result}")
                return False

        except Exception as e:
            print(f"   ❌ Error SadTalker: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_from_deal(
        self,
        deal_data: dict,
        audio_path: str,
        output_path: str,
        temp_dir: str = None,
    ) -> bool:
        """
        Genera video SadTalker desde datos de oferta.

        Args:
            deal_data: Diccionario con imagen_url, título, etc.
            audio_path: Ruta al audio TTS ya generado
            output_path: Donde guardar el video
            temp_dir: Directorio temporal para descargas

        Returns:
            True si se generó exitosamente
        """
        image_url = deal_data.get("image_url")
        if not image_url:
            print("   ❌ No hay URL de imagen en deal_data")
            return False

        temp_dir = temp_dir or tempfile.gettempdir()
        image_path = os.path.join(temp_dir, "sadtalker_input.jpg")

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

        # Generar video
        return self.generate_video(
            image_path=image_path,
            audio_path=audio_path,
            output_path=output_path,
        )


# Test
if __name__ == "__main__":
    print("🎭 Test SadTalker Generator")
    print(f"   Habilitado: {is_sadtalker_enabled()}")

    if is_sadtalker_enabled():
        gen = SadTalkerGenerator()
        print(f"   Disponible: {gen.is_available()}")
        print(f"   Space conectado: {gen.connected_space}")
