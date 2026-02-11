"""
Servicio de Text-to-Speech para generar audio de voz para videos.
Soporta múltiples backends: Edge TTS (alta calidad) y gTTS (fallback gratuito).
"""
import os
import asyncio


class TTSService:
    """Genera audio de voz con múltiples backends TTS."""

    # Voces españolas disponibles en Edge TTS (Neural) - solo para referencia
    EDGE_VOICES = {
        "es-ES-AlvaroNeural": "Masculina España (Álvaro)",
        "es-ES-ElviraNeural": "Femenina España (Elvira)",
        "es-MX-DaliaNeural": "Femenina México (Dalia)",
        "es-MX-JorgeNeural": "Masculino México (Jorge)",
    }

    def __init__(self, voice: str = "es-ES-ElviraNeural", backend: str = "auto"):
        """
        Inicializa el servicio TTS.

        Args:
            voice: Nombre de la voz a usar (para Edge TTS)
            backend: "edge", "gtts", o "auto" (intenta edge, fallback a gtts)
        """
        self.voice = voice
        self.backend = backend
        self.rate = "+10%"
        self.pitch = "+0Hz"

    async def _synthesize_edge(self, text: str, output_path: str) -> dict:
        """Genera audio usando Edge TTS (alta calidad, voces neurales)."""
        import edge_tts

        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch)
        await communicate.save(output_path)

        if not os.path.exists(output_path):
            raise Exception("El archivo de audio no se creó")

        file_size = os.path.getsize(output_path)
        if file_size < 1000:
            raise Exception(f"Archivo de audio muy pequeño ({file_size} bytes)")

        return {
            "file_path": output_path,
            "file_size": file_size,
            "duration_seconds": self._estimate_duration(text),
            "voice": self.voice,
            "backend": "edge-tts",
            "text": text,
        }

    def _synthesize_gtts(self, text: str, output_path: str) -> dict:
        """Genera audio usando gTTS (Google TTS gratuito, funciona en CI)."""
        from gtts import gTTS

        # Determinar idioma basado en la voz configurada
        lang = "es"
        tld = "es"  # Acento español de España
        if "MX" in self.voice:
            tld = "com.mx"  # Acento mexicano
        elif "AR" in self.voice:
            tld = "com.ar"  # Acento argentino

        tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
        tts.save(output_path)

        if not os.path.exists(output_path):
            raise Exception("El archivo de audio no se creó")

        file_size = os.path.getsize(output_path)
        if file_size < 1000:
            raise Exception(f"Archivo de audio muy pequeño ({file_size} bytes)")

        return {
            "file_path": output_path,
            "file_size": file_size,
            "duration_seconds": self._estimate_duration(text),
            "voice": f"gtts-{lang}-{tld}",
            "backend": "gtts",
            "text": text,
        }

    def synthesize(self, text: str, output_path: str, rate: str = None, pitch: str = None) -> dict:
        """
        Genera archivo de audio MP3 a partir de texto.

        Args:
            text: Texto a convertir en voz
            output_path: Ruta donde guardar el archivo MP3
            rate: Velocidad (solo para Edge TTS)
            pitch: Tono (solo para Edge TTS)

        Returns:
            dict con información del audio generado
        """
        if rate:
            self.rate = rate
        if pitch:
            self.pitch = pitch

        # Estrategia según backend configurado
        if self.backend == "gtts":
            return self._try_gtts(text, output_path)
        elif self.backend == "edge":
            return self._try_edge(text, output_path)
        else:  # auto
            return self._try_auto(text, output_path)

    def _try_edge(self, text: str, output_path: str) -> dict:
        """Intenta usar Edge TTS."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._synthesize_edge(text, output_path))
        finally:
            loop.close()

    def _try_gtts(self, text: str, output_path: str) -> dict:
        """Intenta usar gTTS."""
        result = self._synthesize_gtts(text, output_path)
        print(f"   🔊 Audio TTS generado (gTTS): {output_path} ({result['file_size'] // 1024}KB)")
        return result

    def _try_auto(self, text: str, output_path: str) -> dict:
        """Intenta Edge TTS primero, fallback a gTTS si falla."""
        try:
            result = self._try_edge(text, output_path)
            print(f"   🔊 Audio TTS generado (Edge): {output_path} ({result['file_size'] // 1024}KB)")
            return result
        except Exception as e:
            print(f"   ⚠️ Edge TTS falló ({e}), usando gTTS como fallback...")
            return self._try_gtts(text, output_path)

    def _estimate_duration(self, text: str) -> float:
        """
        Estima la duración del audio basándose en el texto.
        Aproximación: ~150 palabras por minuto en español.
        """
        words = len(text.split())
        rate_modifier = 1.0
        if self.rate and self.rate.startswith("+"):
            try:
                percent = int(self.rate.replace("+", "").replace("%", ""))
                rate_modifier = 1 - (percent / 100)
            except ValueError:
                pass
        elif self.rate and self.rate.startswith("-"):
            try:
                percent = int(self.rate.replace("-", "").replace("%", ""))
                rate_modifier = 1 + (percent / 100)
            except ValueError:
                pass

        base_duration = (words / 150) * 60
        return base_duration * rate_modifier

    def synthesize_full_script(self, text: str, output_path: str) -> dict:
        """Alias para synthesize."""
        return self.synthesize(text, output_path)


# Presets de configuración
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
    tts = TTSService(voice="es-ES-ElviraNeural", backend="auto")
    test_text = "¡Hola! Soy tu nuevo hornillo de camping. Perfecto para aventuras. ¡Corre al link en bio!"
    output = tts.synthesize(test_text, "/tmp/test_tts.mp3")
    print(f"\nResultado: {output}")
