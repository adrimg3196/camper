"""
Generador de diálogos persuasivos para productos usando Gemini AI.
Crea scripts donde el producto "habla" al espectador invitándole a comprar.
"""
import os
import json
import requests
from typing import List, Dict


class DialogueGenerator:
    """Genera diálogos de venta estilo TikTok viral usando Gemini."""

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_AI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def generate_product_dialogue(self, deal_data: dict) -> List[Dict]:
        """
        Genera un script de diálogo donde el producto habla al espectador.

        Returns:
            Lista de segmentos con timestamp y texto:
            [
                {"start": 1.0, "end": 3.0, "text": "..."},
                {"start": 3.0, "end": 6.0, "text": "..."},
                ...
            ]
        """
        title = deal_data.get('marketing_title') or deal_data.get('title', 'Producto')
        price = deal_data.get('price', 0)
        original_price = deal_data.get('original_price')
        discount = deal_data.get('discount', 0)
        category = deal_data.get('category', 'camping')

        if self.api_key:
            return self._generate_with_gemini(title, price, original_price, discount, category)
        else:
            return self._generate_template_dialogue(title, price, discount)

    def _generate_with_gemini(self, title: str, price: float, original_price: float,
                               discount: int, category: str) -> List[Dict]:
        """Genera diálogo usando Gemini AI."""
        prompt = f"""Eres un experto en marketing viral de TikTok. Genera un script corto y persuasivo
donde el PRODUCTO habla directamente al espectador en primera persona, como si tuviera personalidad.

PRODUCTO: {title}
CATEGORIA: {category}
PRECIO: {price}€
{f'PRECIO ORIGINAL: {original_price}€' if original_price else ''}
{f'DESCUENTO: {discount}%' if discount else ''}

REGLAS:
1. El producto habla en PRIMERA PERSONA ("Soy...", "Te ofrezco...")
2. Tono ENERGICO, DIRECTO y URGENTE (estilo TikTok viral)
3. Usa palabras que generen FOMO (escasez, urgencia)
4. MAXIMO 4 frases cortas
5. Cada frase de máximo 10 palabras
6. En español de España (no uses "ustedes", usa "tú")
7. Termina con llamada a la acción clara

FORMATO JSON (solo JSON, sin texto adicional):
{{
  "segments": [
    {{"start": 1.0, "end": 3.5, "text": "Frase de presentación"}},
    {{"start": 3.5, "end": 6.0, "text": "Frase de beneficio"}},
    {{"start": 6.0, "end": 9.0, "text": "Frase de urgencia/precio"}},
    {{"start": 9.0, "end": 12.0, "text": "Llamada a la acción"}}
  ]
}}"""

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.9, "maxOutputTokens": 500}
                },
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']

                # Limpiar JSON
                clean_text = text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text.replace("```json", "").replace("```", "").strip()
                elif clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    clean_text = clean_text.strip()

                data = json.loads(clean_text)
                segments = data.get('segments', [])

                print(f"   🗣️ Diálogo generado por Gemini: {len(segments)} segmentos")
                return segments

            else:
                print(f"   ⚠️ Error Gemini API ({response.status_code}): {response.text[:200]}")
                return self._generate_template_dialogue(title, price, discount)

        except Exception as e:
            print(f"   ⚠️ Error generando diálogo: {e}")
            return self._generate_template_dialogue(title, price, discount)

    def _generate_template_dialogue(self, title: str, price: float, discount: int) -> List[Dict]:
        """Genera diálogo usando plantillas predefinidas (fallback)."""
        # Acortar título si es muy largo
        short_title = title[:30] + "..." if len(title) > 30 else title

        segments = [
            {"start": 1.0, "end": 3.5, "text": f"¡Hola! Soy {short_title}"},
            {"start": 3.5, "end": 6.5, "text": "Perfecto para tus aventuras al aire libre"},
        ]

        if discount and discount > 0:
            segments.append({
                "start": 6.5, "end": 9.5,
                "text": f"Hoy tengo {discount}% de descuento. ¡Solo {price:.0f} euros!"
            })
        else:
            segments.append({
                "start": 6.5, "end": 9.5,
                "text": f"¡Increíble precio! Solo {price:.0f} euros"
            })

        segments.append({
            "start": 9.5, "end": 12.5,
            "text": "¡Corre al link en bio antes de que vuele!"
        })

        print(f"   🗣️ Diálogo generado (template): {len(segments)} segmentos")
        return segments

    def get_full_script(self, segments: List[Dict]) -> str:
        """Combina todos los segmentos en un script completo para TTS."""
        return " ".join(seg['text'] for seg in segments)

    def get_total_duration(self, segments: List[Dict]) -> float:
        """Calcula la duración total del diálogo."""
        if not segments:
            return 0
        return max(seg['end'] for seg in segments)


if __name__ == "__main__":
    # Test
    generator = DialogueGenerator()
    test_deal = {
        "title": "Lixada Hornillo Camping Gas Portátil",
        "marketing_title": "Hornillo PRO para aventureros",
        "price": 14.99,
        "original_price": 19.99,
        "discount": 25,
        "category": "cocina-camping"
    }
    segments = generator.generate_product_dialogue(test_deal)
    for seg in segments:
        print(f"  [{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
    print(f"\nScript completo: {generator.get_full_script(segments)}")
