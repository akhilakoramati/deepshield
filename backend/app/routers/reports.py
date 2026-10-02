from fastapi import APIRouter, Depends, HTTPException
from io import BytesIO
import json
from fastapi.responses import JSONResponse, Response
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.security import get_current_user
from ..database.session import get_db
from ..models.analysis import AnalysisResult
from ..models.report import Report
from ..models.user import User
from ..schemas.report import ReportRequest
from ..services.analysis_service import get_user_analysis
from ..services.report_service import create_report as create_report_record

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("")
def create_report(payload: ReportRequest, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    report = create_report_record(payload.analysis_id, user.id, payload.title, payload.format, database)
    return {"id": report.id, "title": report.title, "format": report.format, "status": "created"}


@router.get("")
def list_reports(user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    reports = database.scalars(select(Report).where(Report.user_id == user.id).order_by(Report.created_at.desc()))
    return [{"id": report.id, "analysis_id": report.analysis_id, "title": report.title, "format": report.format, "created_at": report.created_at} for report in reports]


@router.get("/{report_id}")
def get_report(report_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    report = database.scalar(select(Report).where(Report.id == report_id, Report.user_id == user.id))
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    analysis = get_user_analysis(report.analysis_id, user.id, database)
    return JSONResponse({"id": report.id, "title": report.title, "format": report.format, "created_at": report.created_at.isoformat(), "analysis": {"id": analysis.id, "status": analysis.status, "label": analysis.label, "confidence": analysis.confidence, "details": analysis.details, "media_name": analysis.file.original_name, "media_type": analysis.file.media_type, "media_size_bytes": analysis.file.size_bytes, "created_at": analysis.created_at.isoformat()}})


@router.get("/{report_id}/download")
def download_report(report_id: int, user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    report = database.scalar(select(Report).where(Report.id == report_id, Report.user_id == user.id))
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    analysis = get_user_analysis(report.analysis_id, user.id, database)
    if report.format != "pdf":
        payload = {"product": "DeepShield", "report_id": report.id, "title": report.title, "analysis": {"id": analysis.id, "media_id": analysis.file_id, "status": analysis.status, "prediction": analysis.label, "confidence": analysis.confidence, "summary": analysis.details, "created_at": analysis.created_at.isoformat()}}
        return Response(content=json.dumps(payload, indent=2), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="deepshield-report-{analysis.id}.json"'})
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    heading = styles["Heading2"]
    story = [Paragraph("DeepShield", styles["Title"]), Paragraph("AI-Powered Media Authenticity Analysis", body), Spacer(1, 0.25 * inch)]
    case_data = [["Analysis ID", str(analysis.id)], ["User reference", f"User {user.id}"], ["Analysis date", analysis.created_at.isoformat()], ["File name", analysis.file.original_name], ["File type", analysis.file.media_type], ["File size", f"{analysis.file.size_bytes} bytes"]]
    story.extend([Paragraph("Case Information", heading), Table(case_data, colWidths=[1.5 * inch, 5 * inch], style=TableStyle([("GRID", (0, 0), (-1, -1), .5, "#B8C4CC"), ("BACKGROUND", (0, 0), (0, -1), "#EAF1F4"), ("VALIGN", (0, 0), (-1, -1), "TOP")])) , Spacer(1, 0.2 * inch)])
    verdict = analysis.label or "Inconclusive"
    risk = "Elevated" if verdict == "FAKE" else "Low" if verdict == "REAL" else "Moderate"
    result_data = [["Final verdict", verdict], ["Confidence", f"{analysis.confidence}%" if analysis.confidence is not None else "Not available"], ["Risk level", risk], ["Model used", "Configured DeepShield detector"], ["Processing time", "Not recorded by the detector"]]
    story.extend([Paragraph("Detection Result", heading), Table(result_data, colWidths=[1.5 * inch, 5 * inch], style=TableStyle([("GRID", (0, 0), (-1, -1), .5, "#B8C4CC"), ("BACKGROUND", (0, 0), (0, -1), "#EAF1F4"), ("VALIGN", (0, 0), (-1, -1), "TOP")])) , Spacer(1, 0.2 * inch)])
    details = analysis.details or "No analysis details were recorded."
    story.extend([Paragraph("Analysis Details", heading), Paragraph(details, body), Spacer(1, 0.2 * inch), Paragraph("Report Summary", heading), Paragraph(f"DeepShield classified this {analysis.file.media_type} as {verdict} with the recorded confidence shown above.", body), Spacer(1, 0.2 * inch), Paragraph("Disclaimer", heading), Paragraph("Automated AI detection is probabilistic and should not automatically be treated as definitive proof. Review the source media and relevant evidence before making consequential decisions.", body)])
    output = BytesIO()
    SimpleDocTemplate(output, pagesize=LETTER, rightMargin=.65 * inch, leftMargin=.65 * inch, topMargin=.65 * inch, bottomMargin=.65 * inch).build(story)
    return Response(content=output.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="deepshield_report_{analysis.id}.pdf"'})
