from database.base import Base
from database.engine import engine

# Import model agar terdaftar di metadata
from models.user import User


def init_database():
    Base.metadata.create_all(bind=engine)