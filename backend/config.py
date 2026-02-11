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


# Instancias singleton para importar directamente
video_config = VideoConfig()
schedule_config = ScheduleConfig()
amazon_config = AmazonConfig()
ai_config = AIConfig()
