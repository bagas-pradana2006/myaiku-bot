from database.init_db import init_database


def startup():
    """Inisialisasi semua komponen aplikasi."""

    print("Initializing database...")

    init_database()

    print("Database ready.")