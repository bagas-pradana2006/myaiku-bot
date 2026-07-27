"""
Application Settings
--------------------
Memuat seluruh konfigurasi aplikasi dari environment (.env).
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ==========================================================
# Application
# ==========================================================

APP_NAME = "MyAiku Bot"
APP_VERSION = "3.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta")


# ==========================================================
# Telegram
# ==========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", APP_NAME)

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN belum diisi. Silakan isi file .env terlebih dahulu."
    )


# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# ==========================================================
# PostgreSQL
# ==========================================================

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "homeserver")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


# ==========================================================
# Redis
# ==========================================================

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


# ==========================================================
# HTTP Client
# ==========================================================

HTTP_CONNECT_TIMEOUT = 30
HTTP_READ_TIMEOUT = 30
HTTP_WRITE_TIMEOUT = 30
HTTP_POOL_TIMEOUT = 30
HTTP_CONNECTION_POOL_SIZE = 8