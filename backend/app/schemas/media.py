from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_name: str
    media_type: str
    size_bytes: int
    created_at: datetime
