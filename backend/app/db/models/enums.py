import enum


class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    RESCHEDULED = "RESCHEDULED"
    NO_SHOW = "NO_SHOW"


class BookingSource(str, enum.Enum):
    AI_VOICE_AGENT = "AI_VOICE_AGENT"
    WEB_PORTAL = "WEB_PORTAL"
    WALK_IN = "WALK_IN"


class CallStatus(str, enum.Enum):
    RINGING = "RINGING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class SpeakerType(str, enum.Enum):
    PATIENT = "PATIENT"
    AI_ASSISTANT = "AI_ASSISTANT"
    STAFF = "STAFF"


class TriageSeverity(str, enum.Enum):
    LOW = "LOW"
    ROUTINE = "ROUTINE"
    URGENT = "URGENT"
    EMERGENCY_CRITICAL = "EMERGENCY_CRITICAL"


class NotificationChannel(str, enum.Enum):
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"
    VOICE_CALL = "VOICE_CALL"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class DayOfWeek(str, enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
