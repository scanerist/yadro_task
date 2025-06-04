from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey

from datetime import datetime

from app.dao.database import Base

class Link(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    orig_url: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    click_count: Mapped[int] = mapped_column(Integer, default=0)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)