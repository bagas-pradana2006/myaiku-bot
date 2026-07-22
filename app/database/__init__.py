from database.base import Base
from database.engine import engine

# Import semua model agar terdaftar di metadata
from models import *  # noqa: F401,F403

def init_database():
    Base.metadata.create_all(bind=engine)