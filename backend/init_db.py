from backend.database import engine, Base, SessionLocal
from backend.config import settings
from backend.models.user import User
import bcrypt


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin:
            password = settings.ADMIN_PASSWORD or "admin123"
            admin = User(
                username=settings.ADMIN_USERNAME,
                password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
    finally:
        db.close()
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
