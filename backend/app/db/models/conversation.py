# Alias file redirecting to chat.py
from app.db.models.chat import ChatMessage, ChatSession

__all__ = ["ChatSession", "ChatMessage"]
