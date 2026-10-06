import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import CallStatus

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.appointment import Appointment
    from app.db.models.chat import ChatSession


class VoiceCall(Base):
    """
    Twilio Telephony & Voice Assistant Session Record.
    Tracks incoming calls and their outcomes.
    """
    twilio_call_sid: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    caller_phone: Mapped[str] = mapped_column(
        String(20),
        index=True,
        nullable=False,
    )

    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    booked_appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[CallStatus] = mapped_column(
        SAEnum(CallStatus, name="call_status_enum"),
        default=CallStatus.RINGING,
        nullable=False,
    )

    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recording_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    call_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 🔄 Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="voice_calls")
    booked_appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="voice_calls")

    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        "ChatSession",
        back_populates="voice_call",
        cascade="all, delete-orphan",
    )
