import bcrypt
from sqlalchemy.orm import Session
from pydantic import SecretStr
from models.user import User


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def _get_password_value(password: SecretStr | str) -> str:
    return password.get_secret_value() if isinstance(password, SecretStr) else password


def authenticate_user(db: Session, username: str, password: SecretStr | str) -> User | None:
    if not username or not password:
        return None
    password_value = _get_password_value(password)
    if len(username) > 100 or len(password_value) > 100:
        return None
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password_value, user.password_hash):
        return None
    return user
