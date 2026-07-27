from database.init_db import init_database
from utils.logger import logger


def startup():
    """Initialize all application components."""

    logger.info("Initializing database...")

    try:
        init_database()
        logger.info("Database ready.")
    except Exception:
        logger.exception("Database initialization failed.")
        raise