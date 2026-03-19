from backend.database import engine, Base
from backend.config import settings
from passlib.hash import bcrypt


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
