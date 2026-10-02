from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.analysis import AnalysisResult
from ..models.media_file import UploadedFile
from ..models.report import Report
from .analysis_service import get_user_analysis


def create_report(analysis_id: int, user_id: int, title: str, report_format: str, database: Session) -> Report:
    analysis = get_user_analysis(analysis_id, user_id, database)
    report = Report(user_id=user_id, analysis_id=analysis.id, title=title, format=report_format)
    database.add(report)
    database.commit()
    database.refresh(report)
    return report
