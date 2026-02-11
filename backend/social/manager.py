import os
import json
import subprocess
import time
import uuid
import requests
from .uploader import TikTokUploader


class SocialManager:
    def __init__(self):
        print("📱 Inicializando Social Manager (TikTok/Instagram)...")
        self.uploader = TikTokUploader()
        self.temp_dir = os.path.join(os.getcwd(), "backend", "temp_assets")
        os.makedirs(self.temp_dir, exist_ok=True)
        # Remotion project lives in video/ at repo root
        self.video_dir = os.path.join(os.getcwd(), "video")
        self.max_retries = 3

    def process_deal(self, deal_data: dict):
        """Toma una oferta y gestiona su publicación en redes."""
        print(f"🎬 Creando contenido para: {deal_data.get('title')}")

        try:
            video_path = self.generate_remotion_video(deal_data)
        except Exception as e:
            print(f"⚠️ Falló Remotion: {e}")
            video_path = None

        if video_path and os.path.exists(video_path):
            self.upload_to_tiktok(video_path, deal_data)

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

        raise Exception(f"Descarga fallida tras {self.max_retries} intentos: {last_error}")

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
        """Genera un video profesional con Remotion (React)."""
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

        # 2. Preparar props
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

        # Escribir props a archivo temporal (evita problemas de shell escaping)
        props_path = os.path.join(self.temp_dir, "remotion_props.json")
        with open(props_path, 'w') as f:
            json.dump(props, f, ensure_ascii=False)

        # 3. Renderizar con Remotion CLI
        deal_id = deal_data.get('id') or str(uuid.uuid4())[:8]
        output_filename = f"video_{deal_id}.mp4"
        output_path = os.path.join(self.temp_dir, output_filename)

        cmd = [
            "npx", "remotion", "render",
            "DealVideo",
            output_path,
            f"--props={props_path}",
            "--concurrency=2",
        ]

        print(f"   ▶️  Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=self.video_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            print(f"   ❌ Remotion stderr: {result.stderr[-500:]}")
            raise Exception(f"Remotion render falló (exit {result.returncode})")

        file_size = os.path.getsize(output_path)
        print(f"   ✅ Video Remotion generado: {output_path} ({file_size // 1024}KB)")
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
    manager = SocialManager()
    manager.process_deal({
        "title": "Tienda Test",
        "marketing_title": "Tienda Increíble",
        "id": "123",
        "image_url": "https://picsum.photos/700/700",
        "price": 29.99,
    })
    manager.close()
