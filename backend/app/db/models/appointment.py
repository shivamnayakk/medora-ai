import uuid
from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    Enum as SAEnum,
    ForeignKey,
    Index,
    String,
    Text,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import AppointmentStatus, BookingSource

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.doctor import Doctor
    from app.db.models.notification import Notification
    from app.db.models.payment import Payment
    from app.db.models.voice_call import VoiceCall


class Appointment(Base):
    """
    Central Appointment Booking Model.
    Includes database-level double-booking protection.
    """
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    appointment_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    status: Mapped[AppointmentStatus] = mapped_column(
        SAEnum(AppointmentStatus, name="appointment_status_enum"),
        default=AppointmentStatus.PENDING,
        nullable=False,
        index=True,
    )

    booking_source: Mapped[BookingSource] = mapped_column(
        SAEnum(BookingSource, name="booking_source_enum"),
        default=BookingSource.AI_VOICE_AGENT,
        nullable=False,
    )

    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 🔄 Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="appointments")

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="appointment",
        cascade="all, delete-orphan",
    )

    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="appointment",
        cascade="all, delete-orphan",
    )

    voice_calls: Mapped[list["VoiceCall"]] = relationship(
        "VoiceCall",
        back_populates="booked_appointment",
    )

    # 🛡️ Double-booking prevention: Composite Index on Doctor + Date + Start Time
    __table_args__ = (
        Index(
            "ix_doctor_date_time_booking",
            "doctor_id",
            "appointment_date",
            "start_time",
        ),
    )
