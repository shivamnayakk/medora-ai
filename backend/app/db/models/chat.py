import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SAEnum,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import SpeakerType

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.voice_call import VoiceCall
    from app.db.models.tool_execution import ToolExecution
    from app.db.models.triage import TriageAssessment


class ChatSession(Base):
    """
    High-level conversation session container.
    Connects phone calls/web chats with message history and AI tool logs.
    """
    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    voice_call_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("voice_calls.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # 🔄 Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="chat_sessions")
    voice_call: Mapped["VoiceCall"] = relationship("VoiceCall", back_populates="chat_sessions")

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )

    tool_executions: Mapped[list["ToolExecution"]] = relationship(
        "ToolExecution",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )

    triage_assessments: Mapped[list["TriageAssessment"]] = relationship(
        "TriageAssessment",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    """
    Individual turn-by-turn dialogue message (Patient speech or AI voice response).
    """
    chat_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    speaker: Mapped[SpeakerType] = mapped_column(
        SAEnum(SpeakerType, name="speaker_type_enum"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # 🔄 Relationships
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="chat_messages")
