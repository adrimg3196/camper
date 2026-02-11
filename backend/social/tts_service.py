"""
Servicio de Text-to-Speech para generar audio de voz para videos.
Usa Edge TTS (Microsoft) que es gratuito y tiene voces españolas de alta calidad.
"""
import os
import asyncio
import subprocess
from typing import Optional


class TTSService:
    """Genera audio de voz usando Edge TTS (gratuito, voces neurales)."""

    # Voces españolas disponibles en Edge TTS (Neural)
    VOICES = {
        "es-ES-AlvaroNeural": "Masculina España (Álvaro)",
        "es-ES-ElviraNeural": "Femenina España (Elvira)",
        "es-MX-DaliaNeural": "Femenina México (Dalia)",
        "es-MX-JorgeNeural": "Masculino México (Jorge)",
        "es-AR-ElenaNeural": "Femenina Argentina (Elena)",
        "es-CO-GonzaloNeural": "Masculino Colombia (Gonzalo)",
    }

    def __init__(self, voice: str = "es-ES-ElviraNeural"):
        """
        Inicializa el servicio TTS.

        Args:
            voice: Nombre de la voz a usar (por defecto Elvira, femenina española)
        """
        self.voice = voice
        self.rate = "+10%"  # Velocidad ligeramente más rápida para TikTok
        self.pitch = "+0Hz"  # Tono normal

    def set_voice(self, voice: str):
        """Cambia la voz a usar."""
        if voice in self.VOICES:
            self.voice = voice
        else:
            print(f"   ⚠️ Voz '{voice}' no disponible. Usando {self.voice}")

    def synthesize(self, text: str, output_path: str, rate: str = None, pitch: str = None) -> dict:
        """
        Genera archivo de audio MP3 a partir de texto.

        Args:
            text: Texto a convertir en voz
            output_path: Ruta donde guardar el archivo MP3
            rate: Velocidad (ej: "+20%", "-10%", "default")
            pitch: Tono (ej: "+5Hz", "-5Hz", "default")

        Returns:
            dict con información del audio generado
        """
        rate = rate or self.rate
        pitch = pitch or self.pitch

        # Usar edge-tts via subprocess (más confiable que async en algunos entornos)
        cmd = [
            "edge-tts",
            "--voice", self.voice,
            "--rate", rate,
            "--pitch", pitch,
            "--text", text,
            "--write-media", output_path,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                raise Exception(f"edge-tts falló: {result.stderr}")

            # Verificar que el archivo se creó
            if not os.path.exists(output_path):
                raise Exception("El archivo de audio no se creó")

            file_size = os.path.getsize(output_path)
            if file_size < 1000:
                raise Exception(f"Archivo de audio muy pequeño ({file_size} bytes)")

            # Calcular duración aproximada
            duration = self._estimate_duration(text)

            print(f"   🔊 Audio TTS generado: {output_path} ({file_size // 1024}KB, ~{duration:.1f}s)")

            return {
                "file_path": output_path,
                "file_size": file_size,
                "duration_seconds": duration,
                "voice": self.voice,
                "text": text,
            }

        except FileNotFoundError:
            raise Exception("edge-tts no está instalado. Ejecuta: pip install edge-tts")
        except subprocess.TimeoutExpired:
            raise Exception("Timeout generando audio TTS")

    def _estimate_duration(self, text: str) -> float:
        """
        Estima la duración del audio basándose en el texto.
        Aproximación: ~150 palabras por minuto en español.
        """
        words = len(text.split())
        # Ajustar por la velocidad configurada
        rate_modifier = 1.0
        if self.rate.startswith("+"):
            try:
                percent = int(self.rate.replace("+", "").replace("%", ""))
                rate_modifier = 1 - (percent / 100)
            except ValueError:
                pass
        elif self.rate.startswith("-"):
            try:
                percent = int(self.rate.replace("-", "").replace("%", ""))
                rate_modifier = 1 + (percent / 100)
            except ValueError:
                pass

        base_duration = (words / 150) * 60  # segundos
        return base_duration * rate_modifier

    def synthesize_segments(self, segments: list, output_dir: str) -> list:
        """
        Genera audio para múltiples segmentos de diálogo.

        Args:
            segments: Lista de {"start": float, "end": float, "text": str}
            output_dir: Directorio donde guardar los archivos

        Returns:
            Lista de segmentos con info de audio añadida
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []

        for i, segment in enumerate(segments):
            output_path = os.path.join(output_dir, f"segment_{i:02d}.mp3")
            try:
                audio_info = self.synthesize(segment['text'], output_path)
                segment_with_audio = {
                    **segment,
                    "audio_path": output_path,
                    "audio_duration": audio_info['duration_seconds'],
                }
                results.append(segment_with_audio)
            except Exception as e:
                print(f"   ⚠️ Error en segmento {i}: {e}")
                results.append({**segment, "audio_path": None, "error": str(e)})

        return results

    def synthesize_full_script(self, text: str, output_path: str) -> dict:
        """
        Genera un único archivo de audio para el script completo.
        Esto es más fluido que concatenar segmentos individuales.
        """
        return self.synthesize(text, output_path)


# Voces recomendadas para diferentes estilos
VOICE_PRESETS = {
    "energetic_female": {
        "voice": "es-ES-ElviraNeural",
        "rate": "+15%",
        "pitch": "+2Hz",
    },
    "calm_male": {
        "voice": "es-ES-AlvaroNeural",
        "rate": "+5%",
        "pitch": "-2Hz",
    },
    "friendly_female": {
        "voice": "es-MX-DaliaNeural",
        "rate": "+10%",
        "pitch": "+0Hz",
    },
}


if __name__ == "__main__":
    # Test
    tts = TTSService(voice="es-ES-ElviraNeural")

    test_text = "¡Hola! Soy tu nuevo hornillo de camping. Perfecto para aventuras. ¡Corre al link en bio!"

    output = tts.synthesize(test_text, "/tmp/test_tts.mp3")
    print(f"\nResultado: {output}")
