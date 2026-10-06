import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum as SAEnum,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import TriageSeverity

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.chat import ChatSession
    from app.db.models.department import Department


class TriageAssessment(Base):
    """
    AI Clinical Triage & Symptom Evaluation.
    Detects critical/emergency conditions and routes patients to appropriate departments.
    """
    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    chat_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    recommended_department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    symptoms_summary: Mapped[str] = mapped_column(Text, nullable=False)

    severity: Mapped[TriageSeverity] = mapped_column(
        SAEnum(TriageSeverity, name="triage_severity_enum"),
        default=TriageSeverity.ROUTINE,
        nullable=False,
    )

    is_emergency_escalated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 🔄 Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="triage_assessments")
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="triage_assessments")
    recommended_department: Mapped["Department"] = relationship("Department", back_populates="triage_assessments")
