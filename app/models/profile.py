import uuid
from datetime import date

from sqlalchemy import DATE, INT, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.databases import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(INT, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )

    birthdate: Mapped[date] = mapped_column(DATE, nullable=True)
    address: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    job: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    thumbnail: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return self.job
