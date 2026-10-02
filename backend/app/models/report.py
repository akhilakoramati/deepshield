from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis_results.id"))
    title: Mapped[str] = mapped_column(String(255))
    format: Mapped[str] = mapped_column(String(10), default="json")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
