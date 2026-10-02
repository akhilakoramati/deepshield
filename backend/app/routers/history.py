from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.user import User
from .analysis import build_history_page
from ..schemas.analysis import AnalysisHistoryPage

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=AnalysisHistoryPage)
def history(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), media_type: str | None = None, verdict: str | None = None, risk_level: str | None = None, search: str | None = None, start_date: datetime | None = None, end_date: datetime | None = None, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return build_history_page(user.id, database, page, page_size, media_type, verdict, risk_level, search, start_date, end_date)
