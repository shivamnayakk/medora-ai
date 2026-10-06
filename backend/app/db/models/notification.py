import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import NotificationChannel

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.appointment import Appointment


class Notification(Base):
    """
    Patient reminders, booking confirmations, and SMS/WhatsApp alerts.
    """
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    channel: Mapped[NotificationChannel] = mapped_column(
        SAEnum(NotificationChannel, name="notification_channel_enum"),
        default=NotificationChannel.SMS,
        nullable=False,
    )

    recipient: Mapped[str] = mapped_column(String(100), nullable=False)
    message_content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="QUEUED", nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # 🔄 Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="notifications")
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="notifications")
