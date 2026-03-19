import sys
import os
import pytest

backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, os.path.abspath(backend_path))

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(root_path))


@pytest.fixture(scope="function")
def db_session():
    from database import SessionLocal, engine, Base
    from models.user import User
    from models.video import Video
    from models.script import Script
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)
