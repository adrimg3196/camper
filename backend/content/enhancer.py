import os
import random
import requests
import json
from dotenv import load_dotenv
from content.langextract_adapter import extract_product_signals

load_dotenv()

class ContentEnhancer:
    def __init__(self):
        self.google_api_key = os.environ.get("GOOGLE_AI_API_KEY")
        self.hf_api_key = os.environ.get("HUGGINGFACE_API_KEY")
        self.hf_model = os.environ.get("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        self.hf_api_url = f"https://router.huggingface.co/models/{self.hf_model}"
        self.enable_langextract = os.environ.get("ENABLE_LANGEXTRACT", "false").lower() in {"1", "true", "yes", "on"}
        self.langextract_model = os.environ.get("LANGEXTRACT_MODEL_ID", "gemini-2.5-flash")
        self.langextract_api_key = os.environ.get("LANGEXTRACT_API_KEY") or self.google_api_key

    def enhance_product(self, product_data: dict) -> dict:
        """Enriquece los datos del producto usando IA."""

        product_data = dict(product_data)
        print(f"🧠 Mejorando contenido para: {product_data.get('title')}...")
        product_data = self._enrich_with_langextract(product_data)

        if self.google_api_key:
            return self._enhance_with_google_ai(product_data)
        elif self.hf_api_key and not self.hf_api_key.startswith("hf_placeholder"):
            return self._enhance_with_huggingface(product_data)
        else:
            print("⚠️ No AI API key found. Using templates.")
            return self._enhance_with_templates(product_data)

    def _enrich_with_langextract(self, product_data: dict) -> dict:
        """Añade señales estructuradas opcionales con LangExtract."""
        if not self.enable_langextract:
            return product_data

        try:
            signals = extract_product_signals(
                product_data=product_data,
                model_id=self.langextract_model,
                api_key=self.langextract_api_key,
            )

            if not signals:
                return product_data

            product_data["langextract_summary"] = signals.get("summary", "")
            product_data["semantic_tags"] = signals.get("keywords", [])
            product_data["extracted_entities"] = signals.get("entities", [])
            print("🧩 LangExtract añadió contexto estructurado.")
        except Exception as e:
            print(f"⚠️ LangExtract falló: {e}. Continuando sin contexto extra.")

        return product_data

    def _build_langextract_context_hint(self, product_data: dict) -> str:
        summary = str(product_data.get("langextract_summary", "")).strip()
        tags = product_data.get("semantic_tags", [])
        tags = [str(tag).strip() for tag in tags if str(tag).strip()]

        if not summary and not tags:
            return ""

        hint_lines = ["", "Contexto estructurado detectado por LangExtract:"]
        if summary:
            hint_lines.append(f"- Resumen: {summary}")
        if tags:
            hint_lines.append(f"- Keywords: {', '.join(tags[:10])}")

        return "\n".join(hint_lines)

    def _enhance_with_google_ai(self, product_data):
        """Usa Google AI Studio (Gemini) API."""
        try:
            context_hint = self._build_langextract_context_hint(product_data)
            prompt = f"""Actúa como un experto en marketing de aventuras y camping.
Producto: "{product_data['title']}" ({product_data.get('category', 'camping')}).
Precio: {product_data.get('price', 'N/A')}€.
{context_hint}

Escribe un JSON con estos campos:
- marketing_title: Título corto y emocionante (max 50 letras).
- marketing_description: Una frase persuasiva que destaque beneficios.
- tags: Lista de 5 hashtags relevantes.

Solo responde con el JSON, sin texto adicional."""

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.google_api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
            }

            response = requests.post(url, json=payload, timeout=15)

            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                clean_text = text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text.replace("```json", "").replace("```", "").strip()
                elif clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    clean_text = clean_text.strip()

                try:
                    data = json.loads(clean_text)
                    product_data['marketing_title'] = data.get('marketing_title', product_data['title'])
                    product_data['marketing_description'] = data.get('marketing_description', "")
                    print("✨ IA (Google Gemini) ha generado contenido.")
                except json.JSONDecodeError:
                    product_data['marketing_title'] = f"¡OFERTA! {product_data['title'][:30]}..."
                    product_data['marketing_description'] = clean_text[:200]
                    print("✨ IA (Google Gemini) contenido generado (texto plano).")

                return product_data
            else:
                print(f"⚠️ Error Google AI API ({response.status_code}): {response.text[:200]}")
                return self._enhance_with_templates(product_data)

        except Exception as e:
            print(f"⚠️ Error conexión Google AI: {e}. Usando template fallback.")
            return self._enhance_with_templates(product_data)

    def _enhance_with_huggingface(self, product_data):
        """Usa HuggingFace Inference API (Gratis)."""
        try:
            context_hint = self._build_langextract_context_hint(product_data)
            # Mistral/Gemma prompt format
            prompt = f"""<s>[INST] Actúa como un experto en marketing de aventuras.
            Producto: "{product_data['title']}" ({product_data['category']}).
            Precio: {product_data['price']}€.
            {context_hint}
            
            Escribe un JSON con estos campos:
            - marketing_title: Título corto y emocionante (max 50 letras).
            - marketing_description: Una frase persuasiva que destaque beneficios.
            - tags: Lista de 5 hashtags.
            
            Solo responde con el JSON. [/INST]"""
            
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 250, "return_full_text": False, "temperature": 0.7}
            }

            response = requests.post(self.hf_api_url, headers=headers, json=payload)
            
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

        tags = product_data.get("semantic_tags", [])
        tags = [str(tag).strip() for tag in tags if str(tag).strip()]
        if tags:
            desc = f"{desc} Ideal para: {', '.join(tags[:3])}."
            
        product_data['marketing_description'] = desc
        
        print("🤖 Contenido mejorado (Modo Template).")
        return product_data
