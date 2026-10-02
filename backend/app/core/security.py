import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..models.revoked_token import RevokedToken
from ..models.user import User
from .config import ACCESS_TOKEN_MINUTES, JWT_ALGORITHM, JWT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
INVALID_TOKEN_ERROR = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return "scrypt$" + base64.urlsafe_b64encode(salt).decode() + "$" + base64.urlsafe_b64encode(digest).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        _, encoded_salt, encoded_digest = password_hash.split("$", 2)
        salt = base64.urlsafe_b64decode(encoded_salt.encode())
        expected = base64.urlsafe_b64decode(encoded_digest.encode())
        actual = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    token_id = secrets.token_hex(16)
    return jwt.encode({"sub": str(user_id), "jti": token_id, "exp": expires}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub", ""))
        token_id = payload.get("jti")
        if not token_id or database.get(RevokedToken, token_id) is not None:
            raise INVALID_TOKEN_ERROR
    except (JWTError, ValueError):
        raise INVALID_TOKEN_ERROR from None
    user = database.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise INVALID_TOKEN_ERROR
    return user


def revoke_token(token: str, user: User, database: Session) -> None:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    token_id = payload.get("jti")
    expires_at = payload.get("exp")
    if not token_id or not expires_at:
        raise INVALID_TOKEN_ERROR
    database.add(RevokedToken(jti=token_id, user_id=user.id, expires_at=datetime.fromtimestamp(expires_at, timezone.utc)))
    database.commit()
