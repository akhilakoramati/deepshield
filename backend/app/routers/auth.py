from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_user, hash_password, oauth2_scheme, revoke_token, verify_password
from ..database.session import get_db
from ..models.user import User
from ..schemas.auth import ChangePasswordRequest, LoginRequest, TokenResponse, UserCreate, UserResponse
from ..services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, database: Session = Depends(get_db)):
    result = register_user(database, payload.email, payload.full_name, payload.password)
    if result is None:
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user, token = result
    return {"access_token": token, "user": user}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, database: Session = Depends(get_db)):
    result = authenticate_user(database, payload.email, payload.password)
    if result is None:
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    user, token = result
    return {"access_token": token, "user": user}


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: ChangePasswordRequest, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    user.password_hash = hash_password(payload.new_password)
    database.commit()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(oauth2_scheme), user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    revoke_token(token, user, database)
