from fastapi import APIRouter, Depends

from ..core.dependencies import get_current_user
from ..models.user import User
from ..schemas.auth import UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def current_user(user: User = Depends(get_current_user)):
    return user
