from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnalysisCreate(BaseModel):
    media_id: int


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: int
    analysis_id: Optional[int] = None
    media_id: Optional[int] = None
    status: str
    label: Optional[str]
    confidence: Optional[int]
    details: Optional[str]
    created_at: datetime


class AnalysisDetail(AnalysisResponse):
    media_name: str
    media_type: str
    media_size_bytes: int


class AnalysisHistoryPage(BaseModel):
    items: list[AnalysisDetail]
    page: int
    page_size: int
    total: int
    total_pages: int
