import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.chat import ChatSession


class ToolExecution(Base):
    """
    Audit log for LangGraph/AI Agent function calling & tool executions.
    Guarantees observability and debugging of agent decisions.
    """
    chat_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tool_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input_arguments: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    output_response: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    execution_status: Mapped[str] = mapped_column(String(20), default="SUCCESS", nullable=False)
    execution_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 🔄 Relationships
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="tool_executions")
