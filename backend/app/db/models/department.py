from typing import TYPE_CHECKING
from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.doctor import Doctor
    from app.db.models.triage import TriageAssessment


class Department(Base):
    """
    Hospital clinical departments (e.g. Cardiology, Neurology, Pediatrics, Orthopedics).
    Used by AI Assistant for doctor routing and triage redirection.
    """
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # 🔄 Relationships
    doctors: Mapped[list["Doctor"]] = relationship(
        "Doctor",
        back_populates="department",
    )

    triage_assessments: Mapped[list["TriageAssessment"]] = relationship(
        "TriageAssessment",
        back_populates="recommended_department",
    )
