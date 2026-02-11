"""
Generador de videos AI usando Google Veo 3.1.
Crea animaciones 3D donde el producto cobra vida y habla al espectador.
"""
import os
import time
import base64
import requests
from typing import Optional, Dict

# Plantillas de escenas por categoría de producto
SCENE_TEMPLATES = {
    "cocina-camping": {
        "setting": "fogata de camping en la montaña al atardecer",
        "action": "salta emocionado cerca del fuego",
        "emotion": "entusiasmado y aventurero",
        "lighting": "cálida luz de fuego, ambiente acogedor de montaña",
    },
    "mochilas": {
        "setting": "sendero de montaña con vistas espectaculares",
        "action": "se mueve con energía como listo para la aventura",
        "emotion": "determinado y fuerte",
        "lighting": "luz natural de amanecer en la montaña",
    },
    "dormir": {
        "setting": "tienda de camping bajo las estrellas",
        "action": "se acurruca cómodamente, luego mira a cámara",
        "emotion": "relajado pero convincente",
        "lighting": "luz suave de luna y estrellas",
    },
    "iluminacion": {
        "setting": "bosque oscuro de noche",
        "action": "brilla con intensidad, iluminando todo a su alrededor",
        "emotion": "poderoso y confiable",
        "lighting": "contraste dramático entre oscuridad y luz del producto",
    },
    "hidratacion": {
        "setting": "cima de montaña con sol brillante",
        "action": "suda gotas de agua fresca, se ve refrescante",
        "emotion": "fresco y revitalizante",
        "lighting": "luz solar brillante, cielo azul",
    },
    "camping": {
        "setting": "campamento en la naturaleza",
        "action": "se presenta con personalidad",
        "emotion": "amigable y útil",
        "lighting": "luz natural de exterior",
    },
}


class VeoVideoGenerator:
    """Genera videos animados con Veo 3.1 donde el producto cobra vida."""

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_AI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "veo-3.1-generate-preview"

    def _build_animation_prompt(self, deal_data: dict, dialogue: str) -> str:
        """
        Construye el prompt para Veo que anima el producto como personaje.
        """
        title = deal_data.get('title', 'producto')
        category = deal_data.get('category', 'camping')
        price = deal_data.get('price', 0)
        discount = deal_data.get('discount', 0)

        # Obtener plantilla de escena
        scene = SCENE_TEMPLATES.get(category, SCENE_TEMPLATES['camping'])

        prompt = f"""Animación 3D estilo TikTok viral, formato 9:16.

PERSONAJE: El producto "{title}" cobra vida como personaje animado con ojos expresivos y personalidad carismática.

ESCENA: {scene['setting']}

ACCIÓN: El producto {scene['action']}. Mira directo a cámara con actitud {scene['emotion']}. Gesticula de forma exagerada y cómica mientras habla.

ESTILO VISUAL:
- Animación 3D estilizada, colores vibrantes
- Iluminación: {scene['lighting']}
- Cámara fija con micro movimientos sutiles
- El producto es el protagonista absoluto

DIÁLOGO (que el personaje actúa):
"{dialogue}"

IMPORTANTE:
- El producto debe verse REAL pero con elementos animados (ojos, boca, expresiones)
- Movimientos exagerados estilo cartoon
- Energía alta, ritmo rápido
- Sin subtítulos en el video
- Duración: 8 segundos máximo
"""
        return prompt

    def _encode_image_base64(self, image_path: str) -> str:
        """Codifica una imagen local en base64."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _download_image(self, url: str, dest_path: str) -> str:
        """Descarga una imagen de URL."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(resp.content)
        return dest_path

    def generate_video(
        self,
        deal_data: dict,
        dialogue: str,
        image_path: str,
        output_path: str,
        timeout: int = 300,
    ) -> Optional[Dict]:
        """
        Genera un video animado donde el producto habla.

        Args:
            deal_data: Datos del producto (title, category, price, etc.)
            dialogue: El texto que el producto "dice"
            image_path: Ruta a la imagen del producto (local o URL)
            output_path: Donde guardar el video generado
            timeout: Tiempo máximo de espera en segundos

        Returns:
            dict con información del video generado o None si falla
        """
        if not self.api_key:
            print("   ⚠️ GOOGLE_AI_API_KEY no configurada para Veo")
            return None

        # Preparar imagen
        if image_path.startswith("http"):
            temp_image = "/tmp/veo_product_image.jpg"
            try:
                self._download_image(image_path, temp_image)
                image_path = temp_image
            except Exception as e:
                print(f"   ⚠️ Error descargando imagen: {e}")
                return None

        # Codificar imagen
        try:
            image_b64 = self._encode_image_base64(image_path)
        except Exception as e:
            print(f"   ⚠️ Error codificando imagen: {e}")
            return None

        # Construir prompt
        prompt = self._build_animation_prompt(deal_data, dialogue)
        print(f"   🎬 Generando video con Veo 3.1...")
        print(f"   📝 Prompt: {prompt[:100]}...")

        # Llamar a la API
        try:
            # Iniciar generación (operación de larga duración)
            response = requests.post(
                f"{self.base_url}/models/{self.model}:predictLongRunning",
                params={"key": self.api_key},
                json={
                    "instances": [{
                        "prompt": prompt,
                        "image": {
                            "bytesBase64Encoded": image_b64,
                        },
                    }],
                    "parameters": {
                        "aspectRatio": "9:16",
                        "sampleCount": 1,
                    },
                },
                timeout=60,
            )

            if response.status_code != 200:
                print(f"   ⚠️ Error Veo API ({response.status_code}): {response.text[:200]}")
                return None

            operation = response.json()
            operation_name = operation.get("name")

            if not operation_name:
                print(f"   ⚠️ No se obtuvo operation name: {operation}")
                return None

            print(f"   ⏳ Operación iniciada: {operation_name}")

            # Polling hasta que termine
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Verificar estado
                status_resp = requests.get(
                    f"{self.base_url}/{operation_name}",
                    params={"key": self.api_key},
                    timeout=30,
                )

                if status_resp.status_code != 200:
                    print(f"   ⚠️ Error verificando estado: {status_resp.text[:100]}")
                    time.sleep(10)
                    continue

                status = status_resp.json()

                if status.get("done"):
                    # Operación completada
                    if "error" in status:
                        print(f"   ❌ Error en generación: {status['error']}")
                        return None

                    # Extraer video
                    result = status.get("response", {})
                    videos = result.get("generatedVideos", [])

                    if not videos:
                        print("   ⚠️ No se generaron videos")
                        return None

                    video_data = videos[0]
                    video_uri = video_data.get("video", {}).get("uri")

                    if video_uri:
                        # Descargar video
                        video_resp = requests.get(video_uri, timeout=60)
                        with open(output_path, "wb") as f:
                            f.write(video_resp.content)

                        file_size = os.path.getsize(output_path)
                        print(f"   ✅ Video Veo generado: {output_path} ({file_size // 1024}KB)")

                        return {
                            "path": output_path,
                            "size": file_size,
                            "duration_seconds": 8,
                            "source": "veo-3.1",
                        }

                    # Si hay bytes directos
                    video_bytes = video_data.get("video", {}).get("bytesBase64Encoded")
                    if video_bytes:
                        with open(output_path, "wb") as f:
                            f.write(base64.b64decode(video_bytes))

                        file_size = os.path.getsize(output_path)
                        print(f"   ✅ Video Veo generado: {output_path} ({file_size // 1024}KB)")

                        return {
                            "path": output_path,
                            "size": file_size,
                            "duration_seconds": 8,
                            "source": "veo-3.1",
                        }

                    print("   ⚠️ No se encontró video en la respuesta")
                    return None

                # Aún procesando
                elapsed = int(time.time() - start_time)
                print(f"   ⏳ Generando video... ({elapsed}s)")
                time.sleep(10)

            print(f"   ⚠️ Timeout después de {timeout}s")
            return None

        except Exception as e:
            print(f"   ⚠️ Error generando video Veo: {e}")
            return None


def generate_product_dialogue_for_veo(deal_data: dict) -> str:
    """
    Genera el diálogo que el producto "dirá" en el video animado.
    Adaptado para actuación 3D (más corto y dramático).
    """
    title = deal_data.get('marketing_title') or deal_data.get('title', 'Producto')
    short_title = " ".join(title.split()[:3])
    price = deal_data.get('price', 0)
    discount = deal_data.get('discount', 0)
    category = deal_data.get('category', 'camping')

    # Diálogos específicos por categoría (cortos, dramáticos, para actuación)
    dialogues = {
        "cocina-camping": [
            f"¡Ey! ¿Sigues comiendo frío en el monte? ¡Venga ya! Soy {short_title}, y con solo {price:.0f} euros... ¡tendrás comida caliente donde quieras! ¡Dale al link, que vuelo!",
            f"¡Para! ¿Todavía sin hornillo? Mírame, soy {short_title}. {discount}% de descuento. ¡Corre al link antes de que desaparezca!",
        ],
        "mochilas": [
            f"¡Oye tú! ¿Tu espalda todavía sufriendo? Soy {short_title}, ¡y vengo a salvarte! Solo {price:.0f} euros. ¡Link en bio, date prisa!",
            f"¡Eh, aventurero! Deja esa mochila vieja. Yo soy {short_title}, {discount}% OFF. ¡Corre al link ahora!",
        ],
        "dormir": [
            f"¡Brrr! ¿Pasando frío por las noches? Soy {short_title}, ¡y te prometo calorcito! {discount}% de descuento. ¡Link en bio, ya!",
            f"¡Despierta! Tu saco viejo no sirve. Soy {short_title}, solo {price:.0f} euros. ¡Dale al link!",
        ],
        "iluminacion": [
            f"¡En la oscuridad no ves nada! Soy {short_title}, ¡tu salvación! {discount}% OFF. ¡Corre al link en bio!",
            f"¡Pssst! ¿Necesitas luz? Aquí estoy, {short_title}. Solo {price:.0f} euros. ¡Link en bio, vuela!",
        ],
        "hidratacion": [
            f"¡Eh, sediento! ¿Agua caliente en verano? ¡Puaj! Soy {short_title}, mantengo tu agua fría. {discount}% OFF. ¡Link en bio!",
            f"¡Para de comprar botellitas! Soy {short_title}, solo {price:.0f} euros. ¡Dale al link ahora!",
        ],
    }

    import random
    category_dialogues = dialogues.get(category, dialogues.get("cocina-camping"))
    return random.choice(category_dialogues)


if __name__ == "__main__":
    # Test
    generator = VeoVideoGenerator()

    test_deal = {
        "title": "Lixada Hornillo Camping Gas Portátil",
        "price": 14.99,
        "discount": 25,
        "category": "cocina-camping",
    }

    dialogue = generate_product_dialogue_for_veo(test_deal)
    print(f"Diálogo generado: {dialogue}")

    # Para probar la generación real necesitas GOOGLE_AI_API_KEY configurada
    # result = generator.generate_video(
    #     test_deal,
    #     dialogue,
    #     "https://m.media-amazon.com/images/I/61jlrkrWhiL._AC_SL1000_.jpg",
    #     "/tmp/test_veo_video.mp4"
    # )
