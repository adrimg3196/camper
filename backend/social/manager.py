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
        """Genera un video vertical (9:16) a partir de la imagen y datos del producto."""
        print(f"   🔨 Renderizando video real para {deal_data.get('title')}...")
        import requests
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
        
        # Monkeypatch para compatibilidad MoviePy < 2.0 con Pillow >= 10
        if not hasattr(Image, 'ANTIALIAS'):
            Image.ANTIALIAS = Image.LANCZOS

        from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip

        # Datos
        image_url = deal_data.get('image_url')
        title = deal_data.get('marketing_title') or deal_data.get('title')
        price = deal_data.get('price')
        
        if not image_url:
            raise Exception("No hay URL de imagen")

        # Configuración Video TikTok
        W, H = 1080, 1920
        DURATION = 10
        
        # 1. Descargar Imagen (Con headers para evitar bloqueos)
        img_filename = f"temp_{deal_data.get('id')}.jpg"
        img_path = os.path.join(self.temp_dir, img_filename)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        try:
            response = requests.get(image_url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
            else:
                raise Exception(f"Status {response.status_code}")
        except Exception as e:
            raise Exception(f"Error descargando imagen: {e}")

        # 2. Crear Clip de Imagen (Centrado y escalado)
        img_clip = ImageClip(img_path).set_duration(DURATION)
        
        # Escalar imagen para que quepa en el ancho
        img_w, img_h = img_clip.size
        if img_w > 0:
            ratio = W / img_w
            new_h = int(img_h * ratio)
            img_clip = img_clip.resize(width=W)
        
        # Posicionar en el centro
        img_clip = img_clip.set_position(("center", "center"))

        # 3. Fondo (Oscuro para resaltar)
        bg_clip = ColorClip(size=(W, H), color=(20, 20, 20)).set_duration(DURATION)

        # 4. Textos usando PIL (Para evitar ImageMagick)
        overlays = []
        
        def create_text_image(text, fontsize, color, max_width, bg_color=None):
            # Crear imagen transparente
            # Estimación simple de tamaño
            font_size = fontsize
            # Intentar cargar fuente por defecto o sistema. 
            # En Linux/Mac a veces path es complejo, PIL default font es fea.
            # Usaremos default si no hay TTF
            try:
                # Intentar fuente común
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Wrapear texto
            lines = []
            words = text.split()
            current_line = []
            
            # Dummy draw para medir
            dummy_img = Image.new('RGBA', (1, 1))
            draw = ImageDraw.Draw(dummy_img)
            
            for word in words:
                current_line.append(word)
                # Check width
                line_str = " ".join(current_line)
                bbox = draw.textbbox((0, 0), line_str, font=font)
                w = bbox[2] - bbox[0]
                if w > max_width:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            lines.append(" ".join(current_line))
            
            # Altura total
            line_height = fontsize * 1.2
            h_total = int(len(lines) * line_height) + 40
            
            img_text = Image.new('RGBA', (max_width, h_total), (0,0,0,0))
            draw = ImageDraw.Draw(img_text)
            
            y = 0
            for line in lines:
                draw.text((max_width/2, y), line, font=font, fill=color, anchor="ma")
                y += line_height
                
            return np.array(img_text)

        try:
            # Título (Arriba)
            title_img = create_text_image(title, 60, 'white', W-100)
            txt_title = ImageClip(title_img).set_duration(DURATION).set_position(('center', 200))
            overlays.append(txt_title)

            # Precio (Abajo)
            if price:
                price_str = f"Oferta: {price}EUR"
                price_img = create_text_image(price_str, 90, 'yellow', W-100)
                txt_price = ImageClip(price_img).set_duration(DURATION).set_position(('center', 1400))
                overlays.append(txt_price)
                
        except Exception as e:
            print(f"   ⚠️ Falló generación de texto PIL: {e}")

        # 5. Composición Final
        final_clip = CompositeVideoClip([bg_clip, img_clip] + overlays, size=(W, H))
        
        output_filename = f"video_{deal_data.get('id')}.mp4"
        output_path = os.path.join(self.temp_dir, output_filename)
        
        # Logger=None silencia la salida de ffmpeg
        final_clip.write_videofile(output_path, fps=24, codec='libx264', audio=False, logger=None)
        print(f"   ✅ Video generado: {output_path}")

        # Limpiar imagen temp
        try: os.remove(img_path)
        except: pass
        
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
