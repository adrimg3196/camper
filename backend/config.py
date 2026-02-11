"""
Configuración centralizada para el bot de TikTok.
Todos los valores pueden ser sobrescritos con variables de entorno.
"""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class VideoConfig:
    """Configuración de generación y subida de video."""
    CHUNK_SIZE: int = int(os.getenv("VIDEO_CHUNK_SIZE", "5242880"))  # 5MB
    AWS_REGION: str = os.getenv("TIKTOK_REGION", "ap-singapore-1")
    UPLOAD_TIMEOUT: int = int(os.getenv("UPLOAD_TIMEOUT", "300"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    REMOTION_CONCURRENCY: int = int(os.getenv("REMOTION_CONCURRENCY", "2"))
    REMOTION_TIMEOUT: int = int(os.getenv("REMOTION_TIMEOUT", "300"))


@dataclass(frozen=True)
class ScheduleConfig:
    """Configuración de programación y ejecución."""
    RUN_INTERVAL_HOURS: int = int(os.getenv("RUN_INTERVAL_HOURS", "6"))
    PRODUCTS_PER_RUN: int = int(os.getenv("PRODUCTS_PER_RUN", "2"))


@dataclass(frozen=True)
class AmazonConfig:
    """Configuración de Amazon affiliates."""
    BASE_URL: str = os.getenv("AMAZON_BASE_URL", "https://www.amazon.es")
    PARTNER_TAG: str = os.getenv("AMAZON_PARTNER_TAG", "camperdeals-21")


@dataclass(frozen=True)
class AIConfig:
    """Configuración de servicios de IA."""
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_AI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
    # Veo 3.1 video generation (requiere API key con acceso a Veo)
    ENABLE_VEO: bool = os.getenv("ENABLE_VEO", "false").lower() == "true"
    # Runway ML video generation (Gen-4 Turbo)
    RUNWAY_API_KEY: str = os.getenv("RUNWAY_API_KEY", "")
    ENABLE_RUNWAY: bool = os.getenv("ENABLE_RUNWAY", "false").lower() == "true"


# Instancias singleton para importar directamente
video_config = VideoConfig()
schedule_config = ScheduleConfig()
amazon_config = AmazonConfig()
ai_config = AIConfig()


def is_veo_enabled() -> bool:
    """Verifica si Veo está habilitado y configurado."""
    return ai_config.ENABLE_VEO and bool(ai_config.GOOGLE_API_KEY)


def is_runway_enabled() -> bool:
    """Verifica si Runway está habilitado y configurado."""
    return ai_config.ENABLE_RUNWAY and bool(ai_config.RUNWAY_API_KEY)


def get_google_ai_key() -> str:
    """Obtiene la API key de Google AI."""
    return ai_config.GOOGLE_API_KEY
