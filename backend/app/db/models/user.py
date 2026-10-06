from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import UserRole

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.doctor import Doctor
    from app.db.models.audit_log import AuditLog


class User(Base):
    """
    Central authentication and identity table.
    All actors (Patients, Doctors, Staff, Admins) originate here.
    """
    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
    )

    hashed_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role_enum"),
        default=UserRole.PATIENT,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # 1-to-1: Linked Patient profile (if role == PATIENT)
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # 1-to-1: Linked Doctor profile (if role == DOCTOR)
    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # 1-to-Many: Actions performed by this user in audit trail
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="actor",
    )
