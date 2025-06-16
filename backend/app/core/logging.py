import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


def init_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    env = settings.ENVIRONMENT.upper()

    # Try creating the log directory
    file_handler = None
    try:
        LOG_DIR.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_format = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
    except Exception as e:
        print(f"Logging to file disabled: {e}")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        f"[{env}] [%(levelname)s] %(asctime)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # Assemble handlers
    handlers = [console_handler]
    if file_handler:
        handlers.append(file_handler)

    # Global logger config
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )

    # Silence noisy loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
