"""
Logging estructurado para el bot de TikTok.
Proporciona logs en formato JSON para fácil parsing en producción
y formato legible para desarrollo local.
"""
import os
import sys
import json
import logging
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Formatea logs como JSON para producción/CI."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Añadir campos extra si existen
        if hasattr(record, "extra") and record.extra:
            log_data["extra"] = record.extra

        # Añadir excepción si existe
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Formatea logs con colores para desarrollo local."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Iconos por nivel
        icons = {
            "DEBUG": "🔍",
            "INFO": "📝",
            "WARNING": "⚠️ ",
            "ERROR": "❌",
            "CRITICAL": "🚨",
        }
        icon = icons.get(record.levelname, "")

        message = f"{color}{timestamp}{self.RESET} {icon} {record.getMessage()}"

        # Añadir extra si existe
        if hasattr(record, "extra") and record.extra:
            extra_str = " | ".join(f"{k}={v}" for k, v in record.extra.items())
            message += f" [{extra_str}]"

        return message


class ExtraLoggerAdapter(logging.LoggerAdapter):
    """Adapter que permite pasar campos extra fácilmente."""

    def process(self, msg, kwargs):
        extra = kwargs.pop("extra", {})
        if extra:
            kwargs["extra"] = {"extra": extra}
        return msg, kwargs


def get_logger(name: str = "camper") -> ExtraLoggerAdapter:
    """
    Obtiene un logger configurado.

    Uso:
        from logger import get_logger
        logger = get_logger(__name__)
        logger.info("Mensaje", extra={"deal_id": "123", "price": 29.99})
    """
    logger = logging.getLogger(name)

    # Solo configurar si no está ya configurado
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        # JSON en CI, colores en local
        if os.getenv("CI"):
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(ColoredFormatter())

        logger.addHandler(handler)

        # Evitar propagación duplicada
        logger.propagate = False

    return ExtraLoggerAdapter(logger, {})


# Logger por defecto para importación directa
logger = get_logger("camper")
