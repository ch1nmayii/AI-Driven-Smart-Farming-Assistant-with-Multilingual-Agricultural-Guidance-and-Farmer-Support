"""
Week 1-2 Task 6: Conversation State Management Schema
Stores session context, user preferences, and language settings.
Supports multi-turn dialogue by maintaining conversation history per session.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


# ─── Data Models ─────────────────────────────────────────────────────────────

class ConversationTurn(BaseModel):
    """A single turn in the conversation (farmer query + assistant response)."""
    turn_index: int
    role: Literal["farmer", "assistant"]
    text: str
    language: str
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class UserPreferences(BaseModel):
    """Farmer's stored preferences for personalizing future responses."""
    preferred_language: str = "hi"         # hi | kn | en
    location: str = "Uttar Pradesh"        # Farmer's state/district
    primary_crops: List[str] = Field(default_factory=list)  # e.g. ["wheat", "rice"]
    voice_enabled: bool = True             # Whether TTS audio is preferred
    audio_speed: float = 1.0              # TTS speaking rate (0.5 - 2.0)


class SessionState(BaseModel):
    """
    Full conversation session state per farmer.
    Persisted in memory; can be extended to Redis/DB in production.
    """
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_activity: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Language & location context
    language: str = "hi"
    location: str = "Uttar Pradesh"

    # Multi-turn conversation history (last 10 turns retained)
    conversation_history: List[ConversationTurn] = Field(default_factory=list)
    turn_count: int = 0

    # Current context for follow-up queries
    last_intent: Optional[str] = None
    last_crop_context: Optional[str] = None
    last_entities: List[Dict[str, Any]] = Field(default_factory=list)

    # User preferences
    preferences: UserPreferences = Field(default_factory=UserPreferences)

    # Session metadata
    is_active: bool = True
    total_queries: int = 0


# ─── Session Manager ─────────────────────────────────────────────────────────

class SessionManager:
    """
    In-memory session store for farmer conversation state.
    Sessions expire after SESSION_TIMEOUT_MINUTES of inactivity.
    """
    SESSION_TIMEOUT_MINUTES = 30
    MAX_HISTORY_TURNS = 10  # Keep last 10 turns for context

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str, language: str = "hi", location: str = "Uttar Pradesh") -> SessionState:
        """Get existing session or create a new one."""
        # Clean expired sessions first
        self._expire_old_sessions()

        if session_id in self._sessions:
            session = self._sessions[session_id]
            # Update last activity
            session.last_activity = datetime.utcnow().isoformat()
            # Update language/location if changed
            if language != session.language:
                session.language = language
            if location != session.location:
                session.location = location
            return session

        # Create new session
        session = SessionState(
            session_id=session_id,
            language=language,
            location=location,
            preferences=UserPreferences(
                preferred_language=language,
                location=location
            )
        )
        self._sessions[session_id] = session
        return session

    def add_turn(
        self,
        session_id: str,
        role: Literal["farmer", "assistant"],
        text: str,
        language: str,
        intent: Optional[str] = None,
        entities: Optional[List[Dict]] = None,
    ) -> SessionState:
        """Append a conversation turn to the session history."""
        session = self._sessions.get(session_id)
        if not session:
            session = self.get_or_create(session_id, language)

        turn = ConversationTurn(
            turn_index=session.turn_count,
            role=role,
            text=text,
            language=language,
            intent=intent,
            entities=entities or [],
        )
        session.conversation_history.append(turn)
        session.turn_count += 1
        session.last_activity = datetime.utcnow().isoformat()

        # Update context tracking
        if role == "farmer":
            session.total_queries += 1
            if intent:
                session.last_intent = intent
            if entities:
                session.last_entities = entities
                # Auto-detect crop context from entities
                for e in entities:
                    if e.get("entity_type") == "CROP":
                        session.last_crop_context = e.get("canonical_name")
                        break

        # Trim to max history
        if len(session.conversation_history) > self.MAX_HISTORY_TURNS:
            session.conversation_history = session.conversation_history[-self.MAX_HISTORY_TURNS:]

        return session

    def get_context_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Build a context summary for the RAG engine to use in multi-turn queries.
        Returns last intent, crop, and a brief conversation window.
        """
        session = self._sessions.get(session_id)
        if not session:
            return {}

        # Last 3 farmer messages for context
        recent_farmer_msgs = [
            t.text for t in session.conversation_history
            if t.role == "farmer"
        ][-3:]

        return {
            "last_intent": session.last_intent,
            "last_crop_context": session.last_crop_context,
            "language": session.language,
            "location": session.location,
            "recent_queries": recent_farmer_msgs,
            "turn_count": session.turn_count,
        }

    def update_preferences(self, session_id: str, **kwargs) -> Optional[SessionState]:
        """Update user preferences (language, location, crops, voice settings)."""
        session = self._sessions.get(session_id)
        if not session:
            return None
        for key, value in kwargs.items():
            if hasattr(session.preferences, key):
                setattr(session.preferences, key, value)
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Retrieve a session by ID."""
        return self._sessions.get(session_id)

    def list_active_sessions(self) -> List[str]:
        """List all active session IDs (for admin monitoring)."""
        self._expire_old_sessions()
        return list(self._sessions.keys())

    def _expire_old_sessions(self):
        """Remove sessions inactive beyond the timeout window."""
        cutoff = datetime.utcnow() - timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)
        expired = [
            sid for sid, s in self._sessions.items()
            if datetime.fromisoformat(s.last_activity) < cutoff
        ]
        for sid in expired:
            del self._sessions[sid]


# Singleton session manager
session_manager = SessionManager()
