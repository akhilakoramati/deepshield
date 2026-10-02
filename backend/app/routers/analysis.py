from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.analysis import AnalysisResult
from ..models.media_file import UploadedFile
from ..models.user import User
from ..schemas.analysis import AnalysisCreate, AnalysisDetail, AnalysisHistoryPage
from ..services.analysis_service import create_analysis, get_user_analysis

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


def to_detail(result: AnalysisResult) -> AnalysisDetail:
    return AnalysisDetail(
        id=result.id,
        file_id=result.file_id,
        analysis_id=result.id,
        media_id=result.file_id,
        status=result.status,
        label=result.label,
        confidence=result.confidence,
        details=result.details,
        created_at=result.created_at,
        media_name=result.file.original_name,
        media_type=result.file.media_type,
        media_size_bytes=result.file.size_bytes,
    )


@router.post("", response_model=AnalysisDetail, status_code=status.HTTP_201_CREATED)
def run_analysis(payload: AnalysisCreate, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return to_detail(create_analysis(payload.media_id, user.id, database))


def build_history_page(user_id: int, database: Session, page: int, page_size: int, media_type: str | None, verdict: str | None, risk_level: str | None, search: str | None, start_date: datetime | None, end_date: datetime | None) -> AnalysisHistoryPage:
    filters = [UploadedFile.user_id == user_id]
    if media_type:
        filters.append(UploadedFile.media_type == media_type)
    if verdict:
        filters.append(AnalysisResult.label == verdict.upper())
    if risk_level == "elevated":
        filters.append(AnalysisResult.label == "FAKE")
    elif risk_level == "low":
        filters.append(AnalysisResult.label == "REAL")
    elif risk_level == "moderate":
        filters.append(or_(AnalysisResult.label.is_(None), AnalysisResult.label == "INCONCLUSIVE"))
    if search:
        filters.append(func.lower(UploadedFile.original_name).contains(search.lower()))
    if start_date:
        filters.append(AnalysisResult.created_at >= start_date)
    if end_date:
        filters.append(AnalysisResult.created_at <= end_date)
    total = database.scalar(select(func.count(AnalysisResult.id)).join(UploadedFile).where(*filters)) or 0
    query = select(AnalysisResult).join(UploadedFile).where(*filters).order_by(AnalysisResult.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    items = [to_detail(result) for result in database.scalars(query)]
    return AnalysisHistoryPage(items=items, page=page, page_size=page_size, total=total, total_pages=(total + page_size - 1) // page_size)


@router.get("/history", response_model=AnalysisHistoryPage)
def analysis_history(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), media_type: str | None = None, verdict: str | None = None, risk_level: str | None = None, search: str | None = None, start_date: datetime | None = None, end_date: datetime | None = None, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return build_history_page(user.id, database, page, page_size, media_type, verdict, risk_level, search, start_date, end_date)


@router.get("/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return to_detail(get_user_analysis(analysis_id, user.id, database))


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(analysis_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    result = get_user_analysis(analysis_id, user.id, database)
    database.delete(result)
    database.commit()
