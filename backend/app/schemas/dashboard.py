from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_analyses: int
    image_analyses: int
    audio_analyses: int
    video_analyses: int
    real_count: int
    fake_count: int
    average_confidence: float | None
