from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.security import create_access_token, hash_password, verify_password
from ..models.user import User


def register_user(database: Session, email: str, full_name: str, password: str) -> tuple[User, str] | None:
    if database.scalar(select(User).where(User.email == email.lower())):
        return None
    user = User(email=email.lower(), full_name=full_name, password_hash=hash_password(password))
    database.add(user)
    database.commit()
    database.refresh(user)
    return user, create_access_token(user.id)


def authenticate_user(database: Session, email: str, password: str) -> tuple[User, str] | None:
    user = database.scalar(select(User).where(User.email == email.lower()))
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user, create_access_token(user.id)
