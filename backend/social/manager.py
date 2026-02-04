import time
import os
from .uploader import TikTokUploader

class SocialManager:
    def __init__(self):
        print("📱 Inicializando Social Manager (TikTok/Instagram)...")
        self.uploader = TikTokUploader()
        self.temp_dir = os.path.join(os.getcwd(), "backend", "temp_assets")
        os.makedirs(self.temp_dir, exist_ok=True)

    def process_deal(self, deal_data: dict):
        """Toma una oferta y gestiona su publicación en redes."""
        print(f"🎬 Creando contenido para: {deal_data.get('title')}")
        
        # 1. Generar Video Real
        try:
            video_path = self.generate_real_video(deal_data)
        except Exception as e:
            print(f"⚠️ Falló la generación de video real: {e}. Usando dummy fallback.")
            video_path = self.generate_dummy_video(deal_data)
        
        # 2. Publicar (Real con Selenium)
        if video_path and os.path.exists(video_path):
            self.upload_to_tiktok(video_path, deal_data)

    def generate_real_video(self, deal_data):
        """Genera un video vertical (9:16) con zoom/pan para TikTok."""
        print(f"   🔨 Renderizando video real para {deal_data.get('title')}...")
        import requests
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont

        if not hasattr(Image, 'ANTIALIAS'):
            Image.ANTIALIAS = Image.LANCZOS

        from moviepy.editor import (
            ImageClip, CompositeVideoClip, ColorClip,
            AudioClip, concatenate_videoclips
        )

        image_url = deal_data.get('image_url')
        title = deal_data.get('marketing_title') or deal_data.get('title')
        price = deal_data.get('price')

        if not image_url:
            raise Exception("No hay URL de imagen")

        W, H = 1080, 1920
        DURATION = 15  # 15 segundos para TikTok

        # Descargar imagen
        img_filename = f"temp_{deal_data.get('id')}.jpg"
        img_path = os.path.join(self.temp_dir, img_filename)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Status {response.status_code} descargando imagen")
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"   📷 Imagen descargada: {len(response.content)} bytes")

        # Crear imagen del producto escalada
        pil_img = Image.open(img_path).convert('RGB')
        img_w, img_h = pil_img.size

        # Escalar para que quepa bien (80% del ancho)
        target_w = int(W * 0.8)
        ratio = target_w / img_w
        new_h = int(img_h * ratio)
        pil_img = pil_img.resize((target_w, new_h), Image.LANCZOS)

        # Crear frame completo con fondo degradado
        def make_frame_with_bg(product_img, title_text, price_text, t, duration):
            """Genera un frame con animacion de zoom lento."""
            frame = np.zeros((H, W, 3), dtype=np.uint8)

            # Fondo degradado oscuro (azul oscuro -> negro)
            for y in range(H):
                ratio_y = y / H
                r = int(15 * (1 - ratio_y))
                g = int(25 * (1 - ratio_y))
                b = int(50 * (1 - ratio_y))
                frame[y, :] = [r, g, b]

            # Efecto zoom lento en la imagen del producto
            progress = t / duration
            zoom = 1.0 + 0.1 * progress  # zoom del 100% al 110%
            zw = int(product_img.shape[1] * zoom)
            zh = int(product_img.shape[0] * zoom)
            # Centrar el crop
            pil_zoomed = Image.fromarray(product_img).resize((zw, zh), Image.LANCZOS)
            cx = (zw - product_img.shape[1]) // 2
            cy = (zh - product_img.shape[0]) // 2
            pil_cropped = pil_zoomed.crop((cx, cy, cx + product_img.shape[1], cy + product_img.shape[0]))
            prod_arr = np.array(pil_cropped)

            # Posicionar imagen en el centro vertical
            y_offset = (H - prod_arr.shape[0]) // 2
            x_offset = (W - prod_arr.shape[1]) // 2
            if y_offset > 0 and x_offset > 0:
                frame[y_offset:y_offset + prod_arr.shape[0],
                      x_offset:x_offset + prod_arr.shape[1]] = prod_arr

            return frame

        product_np = np.array(pil_img)

        # Crear video con moviepy usando make_frame
        def make_frame(t):
            return make_frame_with_bg(product_np, title, price, t, DURATION)

        video_clip = ColorClip(size=(W, H), color=(0, 0, 0)).set_duration(DURATION)
        video_clip = video_clip.fl(lambda gf, t: make_frame(t))

        # Crear textos con PIL
        overlays = []

        def create_text_overlay(text, fontsize, color, max_width):
            font_size = fontsize
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except Exception:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except Exception:
                    font = ImageFont.load_default()

            lines = []
            words = text.split()
            current_line = []
            dummy_img = Image.new('RGBA', (1, 1))
            draw = ImageDraw.Draw(dummy_img)

            for word in words:
                current_line.append(word)
                line_str = " ".join(current_line)
                bbox = draw.textbbox((0, 0), line_str, font=font)
                if bbox[2] - bbox[0] > max_width:
                    current_line.pop()
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))

            line_h = int(fontsize * 1.4)
            h_total = len(lines) * line_h + 20

            img_text = Image.new('RGBA', (max_width, h_total), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img_text)
            y = 10
            for line in lines:
                # Sombra
                draw.text((max_width // 2 + 2, y + 2), line, font=font, fill=(0, 0, 0, 180), anchor="ma")
                draw.text((max_width // 2, y), line, font=font, fill=color, anchor="ma")
                y += line_h

            return np.array(img_text)

        try:
            # Titulo arriba con fade-in
            title_arr = create_text_overlay(title, 52, (255, 255, 255, 255), W - 80)
            title_clip = (ImageClip(title_arr)
                          .set_duration(DURATION)
                          .set_position(('center', 150))
                          .crossfadein(1.0))
            overlays.append(title_clip)

            # Precio abajo con fade-in retrasado
            if price:
                price_str = f"OFERTA: {price} EUR"
                price_arr = create_text_overlay(price_str, 72, (255, 255, 0, 255), W - 80)
                price_clip = (ImageClip(price_arr)
                              .set_duration(DURATION - 2)
                              .set_start(2)
                              .set_position(('center', H - 400))
                              .crossfadein(1.0))
                overlays.append(price_clip)

            # CTA "Link en bio"
            cta_arr = create_text_overlay("Link en bio!", 44, (100, 200, 255, 255), W - 200)
            cta_clip = (ImageClip(cta_arr)
                        .set_duration(DURATION - 4)
                        .set_start(4)
                        .set_position(('center', H - 250))
                        .crossfadein(0.5))
            overlays.append(cta_clip)
        except Exception as e:
            print(f"   ⚠️ Error texto PIL: {e}")

        # Composicion final
        final_clip = CompositeVideoClip([video_clip] + overlays, size=(W, H))

        # Generar audio silencioso (TikTok prefiere videos con audio)
        silence = AudioClip(lambda t: [0], duration=DURATION, fps=44100).set_duration(DURATION)
        final_clip = final_clip.set_audio(silence)

        output_filename = f"video_{deal_data.get('id')}.mp4"
        output_path = os.path.join(self.temp_dir, output_filename)

        # Bitrate alto para que TikTok no rechace por calidad
        final_clip.write_videofile(
            output_path, fps=30, codec='libx264',
            audio_codec='aac', audio_bitrate='128k',
            bitrate='2000k',
            logger=None
        )

        file_size = os.path.getsize(output_path)
        print(f"   ✅ Video generado: {output_path} ({file_size // 1024}KB)")

        try:
            os.remove(img_path)
        except Exception:
            pass

        return output_path

    def generate_dummy_video(self, deal_data):
        """Fallback: Crea archivo dummy."""
        filename = f"video_{deal_data.get('id', 'temp')}.mp4"
        path = os.path.join(self.temp_dir, filename)
        with open(path, "w") as f:
            f.write("DUMMY VIDEO CONTENT FOR TESTING")
        return path

    def upload_to_tiktok(self, video_path, deal_data):
        """Sube a TikTok usando el navegador automatizado."""
        caption = f"{deal_data.get('marketing_title')} 🔥 Link en bio! #camping #ofertas"
        print(f"   🚀 Iniciando subida a TikTok: {caption}")
        
        success = self.uploader.upload_video(video_path, caption)
        
        if success:
            print("   ✅ Publicado exitosamente (Browser).")
        else:
            print("   ❌ Falló la subida.")

    def close(self):
        self.uploader.close()

if __name__ == "__main__":
    manager = SocialManager()
    manager.process_deal({"title": "Tienda Test", "marketing_title": "Tienda Increíble", "id": "123"})
    manager.close()
