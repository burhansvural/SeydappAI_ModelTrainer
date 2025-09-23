"""
📝 Centralized Logging System
Merkezi logging sistemi - file ve console output
"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "SeydappAI", log_dir: str = "logs") -> logging.Logger:
    """Merkezi logger setup'ı"""

    # Log dizinini oluştur
    Path(log_dir).mkdir(exist_ok=True)

    # Logger oluştur
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Eğer handler'lar zaten eklenmiş ise duplicate etme
    if logger.handlers:
        return logger

    # File handler - rotating logs
    log_file = Path(log_dir) / f"training_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Handler'ları ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
