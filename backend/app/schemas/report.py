from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    analysis_id: int
    title: str = Field(min_length=1, max_length=255)
    format: str = Field(default="pdf", pattern="^(pdf|json|txt)$")
