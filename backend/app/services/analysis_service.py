from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.config import UPLOAD_DIR
from ..models.analysis import AnalysisResult
from ..models.media_file import UploadedFile
from .ai.registry import get_detector


def create_analysis(file_id: int, user_id: int, database: Session) -> AnalysisResult:
    uploaded = database.scalar(select(UploadedFile).where(UploadedFile.id == file_id, UploadedFile.user_id == user_id))
    if uploaded is None:
        raise HTTPException(status_code=404, detail="File not found")
    detector = get_detector(uploaded.media_type)
    detector_result = detector(str(UPLOAD_DIR / uploaded.stored_name))
    result = AnalysisResult(
        file_id=file_id,
        status=detector_result.status,
        label=detector_result.prediction,
        confidence=round(detector_result.confidence),
        details=detector_result.summary,
    )
    database.add(result)
    database.commit()
    database.refresh(result)
    return result


def get_user_analysis(analysis_id: int, user_id: int, database: Session) -> AnalysisResult:
    result = database.scalar(select(AnalysisResult).join(UploadedFile).where(AnalysisResult.id == analysis_id, UploadedFile.user_id == user_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result
