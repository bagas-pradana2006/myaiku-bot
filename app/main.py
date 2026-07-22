from telegram.request import HTTPXRequest
from telegram.ext import Application, CommandHandler

from config.settings import BOT_TOKEN
from handlers.start import start, help_command
from handlers.status import status
from startup import startup
from utils.error_handler import error_handler
from utils.logger import logger


def build_application() -> Application:
    """Membangun instance Telegram Application."""

    request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))

    # Global error handler
    app.add_error_handler(error_handler)

    return app


def main():
    """Entry point aplikasi."""

    logger.info("Initializing MyAiku Bot...")

    # Startup aplikasi
    startup()

    # Build Telegram Application
    app = build_application()

    logger.info("🚀 MyAiku Bot v3 started...")

    # Jalankan bot
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()