from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.analysis import AnalysisResult
from ..models.media_file import UploadedFile
from ..models.user import User
from ..schemas.analysis import AnalysisResponse
from ..schemas.media import FileResponse
from ..services.analysis_service import create_analysis as create_analysis_record
from ..services.media_service import store_upload

router = APIRouter(prefix="/api/files", tags=["uploads"])
ALLOWED_TYPES = {"image", "audio", "video"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".mp4", ".mov", ".webm"}


@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return await store_upload(file, user.id, database)


@router.get("", response_model=list[FileResponse])
def list_files(user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return list(database.scalars(select(UploadedFile).where(UploadedFile.user_id == user.id).order_by(UploadedFile.created_at.desc())))


@router.post("/{file_id}/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(file_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return create_analysis_record(file_id, user.id, database)
