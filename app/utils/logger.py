"""
Application Logger
------------------
Menyediakan logger utama yang digunakan oleh seluruh aplikasi MyAiku.
"""

import logging
from pathlib import Path

from config.settings import LOG_LEVEL

# ==========================================================
# Paths
# ==========================================================

# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Log directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("myaiku")
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger.propagate = False

# Hindari duplicate handler saat module di-import berkali-kali
if not logger.handlers:

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)