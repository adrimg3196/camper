"""
Runway ML Video Generator - Genera videos AI donde el producto cobra vida.

Usa la API de Runway ML (Gen-4 Turbo) para crear videos de productos animados
que hablan directamente al espectador, estilo TikTok viral.
"""

import os
import sys
import time
import base64
import requests
from typing import Optional, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_google_ai_key


# Configuración de Runway ML
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")
RUNWAY_BASE_URL = "https://api.runwayml.com/v1"
RUNWAY_API_VERSION = "2024-11-06"


class RunwayVideoGenerator:
    """
    Genera videos con Runway ML donde el producto se convierte en un
    personaje animado 3D que actúa y "habla" al espectador.
    """

    # Plantillas de escenas por categoría de producto
    SCENE_TEMPLATES = {
        "cocina-camping": {
            "setting": "en medio de un campamento al amanecer, con fogata humeante",
            "action": "salta emocionado y gira mostrando todas sus características",
            "emotion": "orgulloso y entusiasmado",
            "camera": "cámara con leve movimiento circular alrededor del producto",
        },
        "mochilas": {
            "setting": "en la cima de una montaña épica con vistas espectaculares",
            "action": "se infla de orgullo y hace poses heroicas",
            "emotion": "aventurero y confiado",
            "camera": "cámara dramática con zoom lento",
        },
        "dormir": {
            "setting": "dentro de una tienda acogedora de noche con luces cálidas",
            "action": "se estira cómodamente y bosteza de felicidad",
            "emotion": "relajado pero persuasivo",
            "camera": "cámara suave con movimiento mínimo",
        },
        "iluminacion": {
            "setting": "en un bosque oscuro misterioso de noche",
            "action": "enciende dramáticamente iluminando todo a su alrededor",
            "emotion": "heroico y protector",
            "camera": "cámara con efecto de luz dramático",
        },
        "tiendas": {
            "setting": "en un valle verde con montañas de fondo",
            "action": "se despliega majestuosamente y muestra su interior",
            "emotion": "imponente y acogedor",
            "camera": "cámara con movimiento de drone alejándose",
        },
        "hidratacion": {
            "setting": "junto a un río cristalino en un día soleado",
            "action": "salta y muestra el agua fresca en su interior",
            "emotion": "refrescante y energético",
            "camera": "cámara dinámica con gotas de agua",
        },
        "default": {
            "setting": "en un escenario de camping profesional iluminado",
            "action": "cobra vida y presenta sus características con energía",
            "emotion": "entusiasmado y convincente",
            "camera": "cámara con movimiento suave y profesional",
        },
    }

    def __init__(self):
        """Inicializa el generador de Runway."""
        self.api_key = RUNWAY_API_KEY
        if not self.api_key:
            print("   ⚠️ RUNWAY_API_KEY no configurada")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Runway-Version": RUNWAY_API_VERSION,
            "Content-Type": "application/json",
        }

    def _get_scene_template(self, category: str) -> dict:
        """Obtiene la plantilla de escena para una categoría."""
        return self.SCENE_TEMPLATES.get(category, self.SCENE_TEMPLATES["default"])

    def _build_animation_prompt(self, deal_data: dict, dialogue: str) -> str:
        """
        Construye el prompt de animación para Runway.
        Basado en el estilo viral de TikTok donde productos cobran vida.
        """
        title = deal_data.get("title", "Producto")
        category = deal_data.get("category", "default")
        scene = self._get_scene_template(category)

        # Prompt optimizado para Runway Gen-4 Turbo
        prompt = f"""Animación 3D estilo TikTok viral, formato vertical 9:16.

PERSONAJE: El producto "{title}" cobra vida como personaje animado con ojos expresivos y personalidad carismática. Tiene brazos y manos animados que gesticulan mientras "habla".

ESCENARIO: {scene['setting']}

ACCIÓN: El producto {scene['action']}. Mira directo a cámara con actitud {scene['emotion']} y gesticula de forma exagerada y cómica mientras actúa el diálogo. Movimientos fluidos y expresivos.

ESTILO VISUAL: Iluminación cinematográfica, colores vibrantes, estética premium. El producto es el protagonista absoluto.

CÁMARA: {scene['camera']}. Micro-movimientos naturales. Sin subtítulos.

TONO: Carismático, urgente, convincente. Como un vendedor entusiasta que REALMENTE cree en su producto."""

        return prompt

    def _download_image_as_base64(self, image_url: str) -> Optional[str]:
        """Descarga una imagen y la convierte a base64 data URI."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()

            # Detectar tipo de imagen
            content_type = response.headers.get("Content-Type", "image/jpeg")
            if "png" in content_type:
                mime_type = "image/png"
            elif "webp" in content_type:
                mime_type = "image/webp"
            else:
                mime_type = "image/jpeg"

            # Convertir a base64
            base64_data = base64.b64encode(response.content).decode("utf-8")
            return f"data:{mime_type};base64,{base64_data}"

        except Exception as e:
            print(f"   ⚠️ Error descargando imagen: {e}")
            return None

    def _create_video_task(
        self, prompt_text: str, image_data: str, duration: int = 5
    ) -> Optional[str]:
        """
        Crea una tarea de generación de video en Runway.

        Returns:
            Task ID si se creó exitosamente, None en caso contrario.
        """
        endpoint = f"{RUNWAY_BASE_URL}/image_to_video"

        payload = {
            "model": "gen4_turbo",
            "promptImage": image_data,
            "promptText": prompt_text,
            "ratio": "720:1280",  # Formato vertical para TikTok (9:16)
            "duration": duration,
        }

        try:
            response = requests.post(
                endpoint, headers=self.headers, json=payload, timeout=60
            )

            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                task_id = data.get("id")
                print(f"   🎬 Tarea Runway creada: {task_id}")
                return task_id
            else:
                print(f"   ❌ Error Runway API: {response.status_code}")
                print(f"   ❌ Respuesta: {response.text[:500]}")
                return None

        except Exception as e:
            print(f"   ❌ Error creando tarea Runway: {e}")
            return None

    def _poll_task_status(
        self, task_id: str, timeout: int = 300, poll_interval: int = 10
    ) -> Optional[Dict]:
        """
        Espera a que una tarea de Runway complete.

        Args:
            task_id: ID de la tarea
            timeout: Tiempo máximo de espera en segundos
            poll_interval: Intervalo entre consultas en segundos

        Returns:
            Diccionario con resultado si completó, None si falló/timeout
        """
        endpoint = f"{RUNWAY_BASE_URL}/tasks/{task_id}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(endpoint, headers=self.headers, timeout=30)

                if response.status_code != 200:
                    print(f"   ⚠️ Error consultando tarea: {response.status_code}")
                    time.sleep(poll_interval)
                    continue

                data = response.json()
                status = data.get("status", "UNKNOWN")

                if status == "SUCCEEDED":
                    print(f"   ✅ Video Runway generado exitosamente")
                    return data

                elif status == "FAILED":
                    error = data.get("error", "Unknown error")
                    print(f"   ❌ Tarea Runway falló: {error}")
                    return None

                elif status == "THROTTLED":
                    print(f"   ⚠️ Tarea throttled, reintentando...")
                    time.sleep(poll_interval * 2)

                elif status in ["PENDING", "RUNNING"]:
                    elapsed = int(time.time() - start_time)
                    print(f"   ⏳ Runway {status}... ({elapsed}s)")
                    time.sleep(poll_interval)

                else:
                    print(f"   ⚠️ Estado desconocido: {status}")
                    time.sleep(poll_interval)

            except Exception as e:
                print(f"   ⚠️ Error polling: {e}")
                time.sleep(poll_interval)

        print(f"   ❌ Timeout esperando video Runway ({timeout}s)")
        return None

    def _download_video(self, video_url: str, output_path: str) -> bool:
        """Descarga el video generado."""
        try:
            response = requests.get(video_url, timeout=120)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            file_size = os.path.getsize(output_path)
            print(f"   📥 Video descargado: {output_path} ({file_size // 1024}KB)")
            return True

        except Exception as e:
            print(f"   ❌ Error descargando video: {e}")
            return False

    def generate_video(
        self,
        deal_data: dict,
        dialogue: str,
        image_url: str,
        output_path: str,
        duration: int = 5,
        timeout: int = 300,
    ) -> Optional[Dict]:
        """
        Genera un video con Runway donde el producto cobra vida.

        Args:
            deal_data: Datos del producto (title, category, etc.)
            dialogue: Diálogo que "dirá" el producto (para el prompt)
            image_url: URL de la imagen del producto
            output_path: Ruta donde guardar el video
            duration: Duración del video (2-10 segundos)
            timeout: Timeout máximo en segundos

        Returns:
            Dict con información del video si exitoso, None si falla
        """
        if not self.api_key:
            raise Exception("RUNWAY_API_KEY no configurada")

        # 1. Descargar imagen como base64
        print(f"   📷 Procesando imagen para Runway...")
        image_data = self._download_image_as_base64(image_url)
        if not image_data:
            raise Exception("No se pudo procesar la imagen")

        # 2. Construir prompt de animación
        prompt = self._build_animation_prompt(deal_data, dialogue)
        print(f"   📝 Prompt: {prompt[:100]}...")

        # 3. Crear tarea de video
        task_id = self._create_video_task(prompt, image_data, duration)
        if not task_id:
            raise Exception("No se pudo crear la tarea en Runway")

        # 4. Esperar resultado
        result = self._poll_task_status(task_id, timeout)
        if not result:
            raise Exception("La tarea de Runway no completó")

        # 5. Descargar video
        output_data = result.get("output", [])
        if not output_data:
            raise Exception("No hay video en el resultado")

        video_url = output_data[0] if isinstance(output_data, list) else output_data
        if not self._download_video(video_url, output_path):
            raise Exception("No se pudo descargar el video")

        return {
            "task_id": task_id,
            "video_path": output_path,
            "duration": duration,
            "status": "success",
        }


def generate_product_dialogue_for_runway(deal_data: dict) -> str:
    """
    Genera un diálogo corto y dramático para la actuación del producto.
    Optimizado para videos cortos de 5-10 segundos.
    """
    title = deal_data.get("title", "este producto")
    price = deal_data.get("price")
    discount = deal_data.get("discount")
    category = deal_data.get("category", "").lower()

    # Diálogos por categoría (cortos, dramáticos, directos)
    dialogues = {
        "cocina-camping": [
            f"¡Oye! ¿Sigues cocinando con esa cosa vieja? ¡Mírame! Por solo {price}€ soy tuyo. ¡Cómprameee!",
            f"¡Para! ¿En serio vas a dejarme aquí? Soy {title}. ¡Me necesitas en tu próxima aventura!",
        ],
        "dormir": [
            f"¡Brrr! ¿Todavía duermes con frío? ¡Yo te abrigo a -28 grados! ¡Sácame de aquí y llévame al monte!",
            f"¡Oye aventurero! ¿Vas a seguir pasando frío? Por {price}€ duermes como un rey. ¡Vamos!",
        ],
        "mochilas": [
            f"¡Ey! ¿Esa mochila vieja otra vez? ¡Mírame! Soy cómoda, resistente y estoy esperándote. ¡Dale!",
            f"¡Tu espalda me lo agradecerá! Soy {title}. ¿Qué esperas? ¡A la aventura!",
        ],
        "hidratacion": [
            f"¿Agua caliente en verano? ¿En serio? ¡Yo mantengo todo FRÍO 24 horas! ¡Adóptame ya!",
            f"¡Basta de plástico! Soy de acero, mantengo la temperatura y soy tuya por {price}€. ¡Vamos!",
        ],
        "iluminacion": [
            f"¡OSCURIDAD! ¿Te da miedo? ¡Pues yo la destruyo! Soy potente y recargable. ¡Cómprame!",
            f"¡Oye! Sin mí en el camping estás perdido. ¡Ilumino todo! Solo {price}€. ¡Hazlo ya!",
        ],
    }

    # Seleccionar diálogo según categoría
    category_key = None
    for key in dialogues.keys():
        if key in category:
            category_key = key
            break

    if category_key:
        import random

        return random.choice(dialogues[category_key])

    # Diálogo genérico
    if discount and discount > 20:
        return f"¡PARA! ¡{discount}% de descuento! Soy {title} y me estoy REGALANDO. ¡No me dejes aquí!"
    else:
        return f"¡Oye tú! Sí, TÚ. Soy {title} y te estoy esperando. Solo {price}€. ¡Llévame contigo!"


def is_runway_enabled() -> bool:
    """Verifica si Runway está habilitado y configurado."""
    return bool(os.getenv("RUNWAY_API_KEY")) and os.getenv("ENABLE_RUNWAY", "false").lower() == "true"


# Test básico
if __name__ == "__main__":
    print("🎬 Test de Runway ML Video Generator")

    if not RUNWAY_API_KEY:
        print("❌ RUNWAY_API_KEY no configurada")
        exit(1)

    generator = RunwayVideoGenerator()

    test_deal = {
        "title": "Saco de Dormir Invierno -28°C",
        "category": "dormir",
        "price": 89.99,
        "discount": 25,
    }

    dialogue = generate_product_dialogue_for_runway(test_deal)
    print(f"Diálogo generado: {dialogue}")

    # Para test real, descomentar:
    # result = generator.generate_video(
    #     deal_data=test_deal,
    #     dialogue=dialogue,
    #     image_url="https://example.com/image.jpg",
    #     output_path="/tmp/test_video.mp4",
    #     duration=5
    # )
    # print(f"Resultado: {result}")
