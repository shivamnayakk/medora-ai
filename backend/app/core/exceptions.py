from typing import Any, Dict, Optional


# ── Base Exception ───────────────────────────────────────────


class MedoraException(Exception):
    """
    Base exception class for all custom MEDORA application errors.
    Provides standard JSON serialization contract.
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        error_code: str = "MEDORA_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[BaseException] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.cause = cause
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to standard API error response format."""
        return {
            "error": True,
            "error_code": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "cause": str(self.cause) if self.cause else None,
        }


# ── 400 Bad Request ──────────────────────────────────────────


class MedoraBadRequestException(MedoraException):

    def __init__(
        self,
        message: str = "Bad request",
        error_code: str = "BAD_REQUEST",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details,
        )


class InvalidInputException(MedoraBadRequestException):

    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Invalid input for '{field}': {reason}",
            error_code="INVALID_INPUT",
            details={"field": field, "reason": reason},
        )

class DoctorUnavailable(MedoraBadRequestException):
    def __init__(self , doctor_id : str , doctor_name : str , date : str):
        super().__init__(
            message=f"Doctor {doctor_name} {doctor_id} is not availabale on {date}",
            error_code = "DOCTOR_UNAVILABLE",
            details = {
                "doctor_id": doctor_id,
                "doctor_name": doctor_name,
                "date": date,
            }
        )

class InvalidSlotDurationException(MedoraBadRequestException):

    def __init__(self , duration_minutes : int):
        super().__init__(
            message = f"Invalid Duration of {duration_minutes} minutes , Must be 15 , 30 or 60 minutes.",
            error_code = "INVALID_SLOT_DURATION",
            details = {
                'requested_duration' : duration_minutes

            }

            
            
        )
            

            




# ── 401 Unauthorized ─────────────────────────────────────────


class MedoraUnauthorizedException(MedoraException):

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details,
        )


class InvalidTokenException(MedoraUnauthorizedException):

    def __init__(self, reason: str = "Token is invalid or expired"):
        super().__init__(
            message=reason,
            error_code="INVALID_TOKEN",
            details={"reason": reason},
        )


# ── 403 Forbidden ────────────────────────────────────────────


class MedoraForbiddenException(MedoraException):

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "FORBIDDEN",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403,
            details=details,
        )


# ── 404 Not Found ────────────────────────────────────────────


class MedoraNotFoundException(MedoraException):

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
            details=details,
        )


class DoctorNotFoundException(MedoraNotFoundException):

    def __init__(self, doctor_id: int):
        super().__init__(
            message=f"Doctor with ID {doctor_id} not found",
            error_code="DOCTOR_NOT_FOUND",
            details={"doctor_id": doctor_id},
        )


class PatientNotFoundException(MedoraNotFoundException):

    def __init__(self, patient_id: int):
        super().__init__(
            message=f"Patient with ID {patient_id} not found",
            error_code="PATIENT_NOT_FOUND",
            details={"patient_id": patient_id},
        )


class AppointmentNotFoundException(MedoraNotFoundException):

    def __init__(self, appointment_id: int):
        super().__init__(
            message=f"Appointment with ID {appointment_id} not found",
            error_code="APPOINTMENT_NOT_FOUND",
            details={"appointment_id": appointment_id},
        )


class HospitalNotFoundException(MedoraNotFoundException):

    def __init__(self, hospital_id: int):
        super().__init__(
            message=f"Hospital with ID {hospital_id} not found",
            error_code="HOSPITAL_NOT_FOUND",
            details={"hospital_id": hospital_id},
        )


# ── 409 Conflict ─────────────────────────────────────────────


class MedoraConflictException(MedoraException):

    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=409,
            details=details,
        )


class DuplicateBookingException(MedoraConflictException):

    def __init__(self, doctor_id: int, time_slot: str):
        super().__init__(
            message=f"Time slot {time_slot} is already booked for doctor {doctor_id}",
            error_code="DUPLICATE_BOOKING",
            details={"doctor_id": doctor_id, "time_slot": time_slot},
        )


class UserAlreadyExistsException(MedoraConflictException):

    def __init__(self, email: str):
        super().__init__(
            message="A user with this email already exists",
            error_code="USER_ALREADY_EXISTS",
            details={
                "email_domain": email.split("@")[-1]
                if "@" in email
                else "unknown"
            },
        )


# ── 429 Rate Limit ───────────────────────────────────────────


class MedoraRateLimitException(MedoraException):

    def __init__(self, retry_after_seconds: int = 60):
        super().__init__(
            message=f"Rate limit exceeded. Try again in {retry_after_seconds} seconds.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after_seconds": retry_after_seconds},
        )


# ── 502 External Service Errors ──────────────────────────────


class ExternalServiceException(MedoraException):

    def __init__(
        self,
        service_name: str,
        reason: str = "Service unavailable",
        details: Optional[Dict[str, Any]] = None,
    ):
        error_details = {"service": service_name, "reason": reason}
        if details:
            error_details.update(details)
        super().__init__(
            message=f"External service '{service_name}' failed: {reason}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details=error_details,
        )


class LLMException(ExternalServiceException):

    def __init__(self, provider: str, reason: str):
        super().__init__(service_name=f"LLM/{provider}", reason=reason)
        self.error_code = "LLM_ERROR"


class VectorStoreException(ExternalServiceException):

    def __init__(self, reason: str):
        super().__init__(service_name="Qdrant", reason=reason)
        self.error_code = "VECTOR_STORE_ERROR"


class VoiceServiceException(ExternalServiceException):

    def __init__(self, reason: str):
        super().__init__(service_name="Deepgram", reason=reason)
        self.error_code = "VOICE_SERVICE_ERROR"

# -- 503 Emergemcy 

class EmergencyEscalationException(MedoraException):

    def __init__(self , reason : str , emergency_hotline : str = "112"):
        super().__init__(
            message= f"Medical Emergency detected , Immediate Emergency Action is required",
            status_code= 503,
            error_code ="EMERGENCY_ESCALATION",
            details={
                "reason" : reason,
                "emergency_hotline" : emergency_hotline ,
                "sugesstion" : "Please Contact Emergency Services Immediately"

            }
        )
