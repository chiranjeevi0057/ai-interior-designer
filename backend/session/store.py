# session/store.py
# Manages active design sessions in server memory.
# Think of this as a temporary holding area for each user's
# In Tier 2: we swap this to PostgreSQL (persistent across restarts)
# The rest of the app never knows the difference — it always calls the same functions regardless of what's underneath.

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict
from models.intake import IntakePayload
from models.design_plan import DesignPlan
from config import settings


class Session:
    """
    Represents one user's complete design session.
    Everything about their current design lives here.
    """

    def __init__(self, session_id: str, intake: IntakePayload):
        self.session_id = session_id
        self.intake = intake

        # Conversation history — grows with each refinement turn
        # Format: [{"role": "user", "content": "..."}, 
        #          {"role": "assistant", "content": "..."}]
        self.conversation_history = []

        # The current design plan (None until AI generates it)
        self.current_plan: Optional[DesignPlan] = None

        # Image generation tracking
        self.image_job_id: Optional[str] = None
        self.image_url: Optional[str] = None
        self.image_status: str = "pending"
        self.image_prompt: Optional[str] = None

        # Session state machine
        # idle → planning → plan_ready → image_generating → complete
        self.session_state: str = "idle"

        # Timestamps
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(
            minutes=settings.session_expiry_minutes
        )

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def touch(self):
        """Reset the expiry timer — call this on every user interaction."""
        self.updated_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(
            minutes=settings.session_expiry_minutes
        )

    def add_conversation_turn(self, role: str, content: str):
        """Add one message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.touch()

    def to_dict(self) -> dict:
        """Convert session to a dictionary for API responses."""
        return {
            "session_id": self.session_id,
            "session_state": self.session_state,
            "image_status": self.image_status,
            "image_url": self.image_url,
            "plan_version": self.current_plan.version if self.current_plan else 0,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
        }


class SessionStore:
    """
    In-memory store for all active sessions.
    One instance of this runs for the lifetime of the server.
    """

    def __init__(self):
        # The main storage — session_id → Session object
        self._sessions: Dict[str, Session] = {}

    def create(self, intake: IntakePayload) -> Session:
        """Create a new session and store it."""
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id, intake=intake)
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        """Get a session by ID. Returns None if not found or expired."""
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.is_expired():
            self.delete(session_id)
            return None
        return session

    def delete(self, session_id: str):
        """Remove a session from memory."""
        self._sessions.pop(session_id, None)

    def cleanup_expired(self):
        """Remove all expired sessions — called periodically."""
        expired = [
            sid for sid, session in self._sessions.items()
            if session.is_expired()
        ]
        for sid in expired:
            del self._sessions[sid]

    def count(self) -> int:
        """How many active sessions exist."""
        return len(self._sessions)


# Create ONE global instance used throughout the entire app
# Every router imports this same object
session_store = SessionStore()