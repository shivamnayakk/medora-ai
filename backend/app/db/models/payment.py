import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SAEnum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import PaymentStatus

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment


class Payment(Base):
    """
    Financial billing records for appointments and consultation fees.
    """
    appointment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)

    status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True,
    )

    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transaction_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)

    # 🔄 Relationships
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="payments")
