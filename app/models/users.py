from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.core.db import Base


class User(Base):
    name: Mapped[str] = mapped_column(
        String(length=settings.max_length_string),
        nullable=False
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
