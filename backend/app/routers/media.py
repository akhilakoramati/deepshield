from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.user import User
from ..models.media_file import UploadedFile
from ..schemas.media import FileResponse
from ..services.media_service import store_upload

router = APIRouter(prefix="/api/media", tags=["media"])


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(file: UploadFile = File(...), user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return await store_upload(file, user.id, database)


@router.get("/{media_id}", response_model=FileResponse)
def get_media(media_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    media = database.scalar(select(UploadedFile).where(UploadedFile.id == media_id, UploadedFile.user_id == user.id))
    if media is None:
        raise HTTPException(status_code=404, detail="Media file not found")
    return media
