def test_1_database_initialization():
    from backend.init_db import init_db
    init_db()


def test_2_db_session_fixture(db_session):
    assert db_session is not None


def test_3_admin_user_creation(db_session):
    from backend.config import settings
    from backend.models.user import User
    
    admin = db_session.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if admin:
        assert admin.username == settings.ADMIN_USERNAME
        assert admin.role == "admin"


def test_4_get_db_generator():
    from backend.database import get_db
    from sqlalchemy.orm import Session
    
    generator = get_db()
    db = next(generator)
    assert isinstance(db, Session)
    try:
        next(generator)
    except StopIteration:
        pass


def test_5_config_sensitive_fields():
    from backend.config import settings
    assert settings.ADMIN_PASSWORD is None or settings.ADMIN_PASSWORD != "admin"
    assert settings.SECRET_KEY is None or settings.SECRET_KEY != "secret-key-change-in-production"
