from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.analysis import AnalysisResult
from ..models.media_file import UploadedFile
from ..models.user import User
from ..schemas.dashboard import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def stats(user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    query = select(
        func.count(AnalysisResult.id),
        func.sum(case((UploadedFile.media_type == "image", 1), else_=0)),
        func.sum(case((UploadedFile.media_type == "audio", 1), else_=0)),
        func.sum(case((UploadedFile.media_type == "video", 1), else_=0)),
        func.sum(case((AnalysisResult.label == "REAL", 1), else_=0)),
        func.sum(case((AnalysisResult.label == "FAKE", 1), else_=0)),
        func.avg(AnalysisResult.confidence),
    ).join(UploadedFile).where(UploadedFile.user_id == user.id)
    total, images, audio, video, real, fake, average_confidence = database.execute(query).one()
    return DashboardStats(total_analyses=total or 0, image_analyses=images or 0, audio_analyses=audio or 0, video_analyses=video or 0, real_count=real or 0, fake_count=fake or 0, average_confidence=round(float(average_confidence), 2) if average_confidence is not None else None)
