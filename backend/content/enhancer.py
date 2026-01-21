import os
import random
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class ContentEnhancer:
    def __init__(self):
        self.api_key = os.environ.get("HUGGINGFACE_API_KEY")
        self.model = os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        self.api_url = f"https://router.huggingface.co/models/{self.model}"

    def enhance_product(self, product_data: dict) -> dict:
        """Enriquece los datos del producto usando modelos Open Source gratuitos."""
        
        print(f"🧠 Mejorando contenido para: {product_data.get('title')}...")

        if self.api_key and not self.api_key.startswith("hf_placeholder"):
            return self._enhance_with_huggingface(product_data)
        else:
            print("⚠️ No HUGGINGFACE_API_KEY found. Using templates.")
            return self._enhance_with_templates(product_data)

    def _enhance_with_huggingface(self, product_data):
        """Usa HuggingFace Inference API (Gratis)."""
        try:
            # Mistral/Gemma prompt format
            prompt = f"""<s>[INST] Actúa como un experto en marketing de aventuras.
            Producto: "{product_data['title']}" ({product_data['category']}).
            Precio: {product_data['price']}€.
            
            Escribe un JSON con estos campos:
            - marketing_title: Título corto y emocionante (max 50 letras).
            - marketing_description: Una frase persuasiva que destaque beneficios.
            - tags: Lista de 5 hashtags.
            
            Solo responde con el JSON. [/INST]"""
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 250, "return_full_text": False, "temperature": 0.7}
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', '')
                
                print("✨ IA (HuggingFace) ha generado contenido.")
                
                # Intentar limpiar el JSON si el modelo es "charlatán"
                clean_text = generated_text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text.replace("```json", "").replace("```", "")
                
                try:
                    data = json.loads(clean_text)
                    product_data['marketing_title'] = data.get('marketing_title', product_data['title'])
                    product_data['marketing_description'] = data.get('marketing_description', "")
                except:
                    # Fallback si el JSON no es válido, usamos el texto crudo con cuidado
                    product_data['marketing_title'] = f"¡OFERTA! {product_data['title'][:30]}..."
                    product_data['marketing_description'] = clean_text[:200]
                
                return product_data
            else:
                print(f"⚠️ Error HuggingFace API: {response.text}")
                return self._enhance_with_templates(product_data)
            
        except Exception as e:
            print(f"⚠️ Error conexión IA: {e}. Usando template fallback.")
            return self._enhance_with_templates(product_data)

    def _enhance_with_templates(self, product_data):
        """Genera contenido basado en reglas simples (Modo Gratis/Sin Key)."""
        
        adjectives = ["Increíble", "Indestructible", "Esencial", "El mejor", "Top ventas"]
        emojis = ["🔥", "🌲", "⚡️", "⛺️", "⛰️"]
        
        adj = random.choice(adjectives)
        emoji = random.choice(emojis)
        
        product_data['marketing_title'] = f"{emoji} {adj}: {product_data['title']}"
        
        cat = product_data.get('category', '').lower()
        if 'camping' in cat or 'tienda' in cat:
            desc = "Prepárate para dormir bajo las estrellas con total comodidad. Resistente, ligero y diseñado para aventureros de verdad."
        elif 'trekking' in cat or 'saco' in cat:
            desc = "No dejes que el frío arruine tu ruta. Este equipo te mantiene caliente y ligero para llegar a la cima."
        else:
            desc = f"La mejor oferta del día para tu próxima escapada. Aprovecha este descuento del {product_data.get('discount')}% antes de que vuele."
            
        product_data['marketing_description'] = desc
        
        print("🤖 Contenido mejorado (Modo Template).")
        return product_data
