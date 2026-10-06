import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import Gender

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.appointment import Appointment
    from app.db.models.voice_call import VoiceCall
    from app.db.models.chat import ChatSession
    from app.db.models.triage import TriageAssessment
    from app.db.models.notification import Notification


class Patient(Base):
    """
    Patient demographic and medical profile.
    Tied 1-to-1 to a User record.
    """
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)

    gender: Mapped[Gender] = mapped_column(
        SAEnum(Gender, name="gender_enum"),
        default=Gender.OTHER,
        nullable=False,
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    medical_history_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # 🔄 Relationships
    user: Mapped["User"] = relationship("User", back_populates="patient")

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan",
    )

    voice_calls: Mapped[list["VoiceCall"]] = relationship(
        "VoiceCall",
        back_populates="patient",
    )

    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        "ChatSession",
        back_populates="patient",
    )

    triage_assessments: Mapped[list["TriageAssessment"]] = relationship(
        "TriageAssessment",
        back_populates="patient",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="patient",
    )
