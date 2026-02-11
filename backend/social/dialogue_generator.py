"""
Generador de diálogos persuasivos para productos usando Gemini AI.
Crea scripts donde el producto "habla" al espectador invitándole a comprar.
Estilo: viral TikTok con personalidad emocional.
"""
import os
import json
import random
import requests
from typing import List, Dict


# Plantillas de personalidad para diferentes categorías
PERSONALITY_TEMPLATES = {
    "cocina-camping": {
        "intro_hooks": [
            "¡Ey! ¿Sigues comiendo barritas en el monte?",
            "Oye, ¿y si te digo que puedo hacer magia en la montaña?",
            "¿Cansado de comer frío en tus rutas?",
        ],
        "benefits": [
            "Conmigo tendrás platos calientes en minutos",
            "Soy ligero, potente, y no te fallo nunca",
            "Tu estómago me lo agradecerá, créeme",
        ],
        "personality": "práctico y directo",
    },
    "mochilas": {
        "intro_hooks": [
            "¿Tu espalda te odia después de cada ruta?",
            "Mira, sé que has sufrido con mochilas baratas",
            "¡Hola aventurero! ¿Listo para cargar como un pro?",
        ],
        "benefits": [
            "Mi diseño ergonómico cuida tu espalda de verdad",
            "Llévame a donde quieras, aguanto lo que sea",
            "Organización perfecta y comodidad extrema",
        ],
        "personality": "resistente y confiable",
    },
    "dormir": {
        "intro_hooks": [
            "¿Pasando frío por las noches en el camping?",
            "Oye, el sueño es sagrado, ¿no crees?",
            "¿Todavía duermes con ese saco viejo que no calienta?",
        ],
        "benefits": [
            "Conmigo dormirás como en tu cama, lo prometo",
            "Calentito hasta en las noches más frías",
            "Tu descanso es mi prioridad número uno",
        ],
        "personality": "acogedor y protector",
    },
    "iluminacion": {
        "intro_hooks": [
            "¿Aún usas el móvil como linterna? Venga ya...",
            "La oscuridad no tiene por qué ser un problema",
            "¡Ey! ¿Quieres ver de verdad en tus aventuras nocturnas?",
        ],
        "benefits": [
            "Ilumino todo lo que necesites ver, sin fallar",
            "Potente, recargable, y siempre lista",
            "Tus manos libres mientras yo trabajo",
        ],
        "personality": "brillante y confiable",
    },
    "hidratacion": {
        "intro_hooks": [
            "¿Todavía comprando botellitas de plástico?",
            "Tu cuerpo necesita agua, pero de calidad",
            "Oye, ¿cuántas botellas has perdido ya?",
        ],
        "benefits": [
            "Mantengo tu agua fría horas y horas",
            "Sin BPA, sin sabores raros, solo agua pura",
            "Ligera, resistente, tu compañera perfecta",
        ],
        "personality": "refrescante y eco-friendly",
    },
    "camping": {
        "intro_hooks": [
            "¿Listo para tu próxima aventura?",
            "Oye, sé que buscas algo especial para el monte",
            "¡Mira lo que tengo para ti, aventurero!",
        ],
        "benefits": [
            "Soy exactamente lo que necesitas ahí fuera",
            "Diseñado para aguantar lo que le eches",
            "Tu mejor compañero de aventuras, sin duda",
        ],
        "personality": "aventurero y versátil",
    },
}

# CTAs virales
VIRAL_CTAS = [
    "¡Corre al link en bio! ¡Vuela!",
    "Link en bio. ¡Corre que se acaba!",
    "¡No esperes más! Link en la bio.",
    "¿A qué esperas? ¡Link en bio!",
    "¡Dale al link en bio ahora mismo!",
    "Link en bio antes de que desaparezca",
]


class DialogueGenerator:
    """Genera diálogos de venta estilo TikTok viral usando Gemini."""

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_AI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def generate_product_dialogue(self, deal_data: dict) -> List[Dict]:
        """
        Genera un script de diálogo donde el producto habla al espectador.
        """
        title = deal_data.get('marketing_title') or deal_data.get('title', 'Producto')
        price = deal_data.get('price', 0)
        original_price = deal_data.get('original_price')
        discount = deal_data.get('discount', 0)
        category = deal_data.get('category', 'camping')

        if self.api_key:
            return self._generate_with_gemini(title, price, original_price, discount, category)
        else:
            return self._generate_emotional_template(title, price, discount, category)

    def _generate_with_gemini(self, title: str, price: float, original_price: float,
                               discount: int, category: str) -> List[Dict]:
        """Genera diálogo emocional usando Gemini AI."""

        # Obtener personalidad según categoría
        personality = PERSONALITY_TEMPLATES.get(category, PERSONALITY_TEMPLATES['camping'])

        prompt = f"""Eres un copywriter experto en TikTok viral. Genera un script EMOCIONAL y PERSUASIVO
donde el PRODUCTO habla DIRECTAMENTE al espectador, como si fuera su amigo dándole un consejo.

PRODUCTO: {title}
CATEGORIA: {category}
PRECIO ACTUAL: {price}€
{f'PRECIO ORIGINAL: {original_price}€ (AHORRO de {original_price - price:.0f}€!)' if original_price else ''}
{f'DESCUENTO: {discount}% OFF' if discount else ''}
PERSONALIDAD DEL PRODUCTO: {personality['personality']}

ESTILO VIRAL (MUY IMPORTANTE):
1. EMPIEZA con una PREGUNTA que conecte emocionalmente
2. El producto habla en PRIMERA PERSONA como un amigo
3. Usa lenguaje COLOQUIAL español (tío, mola, flipar, currar)
4. Genera FOMO real (escasez, urgencia, "no seas el último")
5. MÁXIMO 4 frases MUY CORTAS (8-10 palabras cada una)
6. Termina con CTA urgente hacia "link en bio"

EJEMPLOS DE TONO:
- "¿Sigues pasando frío? Venga ya, tío..."
- "Mira, sé que has buscado esto mil veces"
- "¿A que mola? Pues espera a ver el precio..."

FORMATO JSON (solo JSON, nada más):
{{
  "segments": [
    {{"start": 0.5, "end": 2.5, "text": "Pregunta gancho emocional"}},
    {{"start": 2.5, "end": 5.0, "text": "Presentación con personalidad"}},
    {{"start": 5.0, "end": 8.0, "text": "Beneficio + precio/descuento"}},
    {{"start": 8.0, "end": 11.0, "text": "CTA urgente link en bio"}}
  ]
}}"""

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 1.0, "maxOutputTokens": 500}
                },
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']

                # Limpiar JSON
                clean_text = text.strip()
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()

                data = json.loads(clean_text)
                segments = data.get('segments', [])

                print(f"   🗣️ Diálogo generado por Gemini: {len(segments)} segmentos")
                for seg in segments:
                    print(f"      [{seg['start']:.1f}s] {seg['text']}")
                return segments

            else:
                print(f"   ⚠️ Error Gemini API ({response.status_code})")
                return self._generate_emotional_template(title, price, discount, category)

        except Exception as e:
            print(f"   ⚠️ Error generando diálogo: {e}")
            return self._generate_emotional_template(title, price, discount, category)

    def _generate_emotional_template(self, title: str, price: float, discount: int, category: str) -> List[Dict]:
        """Genera diálogo emocional usando plantillas predefinidas (fallback)."""

        # Obtener plantillas de personalidad
        personality = PERSONALITY_TEMPLATES.get(category, PERSONALITY_TEMPLATES['camping'])

        # Acortar título
        short_title = title.split()[0:4]  # Primeras 4 palabras
        short_title = " ".join(short_title)
        if len(short_title) > 25:
            short_title = short_title[:25] + "..."

        # Construir diálogo emocional
        intro = random.choice(personality['intro_hooks'])
        benefit = random.choice(personality['benefits'])
        cta = random.choice(VIRAL_CTAS)

        segments = [
            {"start": 0.5, "end": 2.5, "text": intro},
            {"start": 2.5, "end": 5.0, "text": f"Soy {short_title}, y vengo a salvarte"},
        ]

        # Frase de precio/descuento
        if discount and discount > 0:
            price_text = f"¡{discount}% OFF! Solo {price:.0f} euros, date prisa"
        else:
            price_text = f"Por solo {price:.0f} euros, ¿lo vas a dejar pasar?"

        segments.append({"start": 5.0, "end": 8.0, "text": price_text})
        segments.append({"start": 8.0, "end": 11.0, "text": cta})

        print(f"   🗣️ Diálogo generado (template emocional): {len(segments)} segmentos")
        for seg in segments:
            print(f"      [{seg['start']:.1f}s] {seg['text']}")
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

    test_deals = [
        {
            "title": "Lixada Hornillo Camping Gas Portátil",
            "price": 14.99,
            "discount": 25,
            "category": "cocina-camping"
        },
        {
            "title": "QEZER Saco Dormir Plumón -28°C",
            "price": 89.99,
            "discount": 31,
            "category": "dormir"
        },
    ]

    for deal in test_deals:
        print(f"\n{'='*50}")
        print(f"Producto: {deal['title']}")
        segments = generator.generate_product_dialogue(deal)
        print(f"\nScript completo: {generator.get_full_script(segments)}")
