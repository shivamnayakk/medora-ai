import uuid
from datetime import time
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import DayOfWeek

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.department import Department
    from app.db.models.appointment import Appointment


class Doctor(Base):
    """
    Doctor professional credentials, department, and consultation details.
    """
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    specialization: Mapped[str] = mapped_column(String(150), nullable=False)
    license_number: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    consultation_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("500.00"), nullable=False)
    room_number: Mapped[str | None] = mapped_column(String(20), nullable=True)

    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 🔄 Relationships
    user: Mapped["User"] = relationship("User", back_populates="doctor")
    department: Mapped["Department"] = relationship("Department", back_populates="doctors")

    availabilities: Mapped[list["DoctorAvailability"]] = relationship(
        "DoctorAvailability",
        back_populates="doctor",
        cascade="all, delete-orphan",
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan",
    )


class DoctorAvailability(Base):
    """
    OPD Schedule slots for each doctor.
    Used by AI Assistant to determine available booking slots.
    """
    __tablename__ = "doctor_availabilities"

    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[DayOfWeek] = mapped_column(
        SAEnum(DayOfWeek, name="day_of_week_enum"),
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 🔄 Relationships
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="availabilities")
