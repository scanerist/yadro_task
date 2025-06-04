from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.dao.database import Base

class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False) 