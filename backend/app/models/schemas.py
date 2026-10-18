from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

LanguageCode = Literal["hi", "kn", "en"]

# ─── Chat ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or transcribed text")
    language: LanguageCode = Field(default="hi", description="hi=Hindi, kn=Kannada, en=English")
    session_id: Optional[str] = Field(default="farmer-session-default")
    location: Optional[str] = Field(default="Uttar Pradesh")
    crop_context: Optional[str] = Field(default=None)

class ChatResponse(BaseModel):
    response_text: str
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None
    language: str
    intent: str
    intent_confidence: float = 0.92
    confidence_score: float = 0.92
    flagged_for_review: bool = False
    sources: List[str] = Field(default_factory=list)
    entities: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# ─── Audio / STT / TTS ───────────────────────────────────────────────────────

class AudioSTTResponse(BaseModel):
    transcription: str
    detected_language: str
    confidence: float
    stt_source: str = "unknown"   # sarvam_ai | openai_whisper | demo_fallback

# ─── Translation ─────────────────────────────────────────────────────────────

class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    source_language: LanguageCode = Field(..., description="Source language code")
    target_language: LanguageCode = Field(..., description="Target language code")

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    translation_source: str = "sarvam_ai"

# ─── Advisory ────────────────────────────────────────────────────────────────

class MandiPriceItem(BaseModel):
    crop: str
    market: str
    state: str
    min_price: float
    max_price: float
    modal_price: float
    unit: str = "₹/Quintal"
    updated_at: str

class WeatherSummary(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: int
    rainfall_probability: int
    advisory: str

# ─── Admin / Review ──────────────────────────────────────────────────────────

class FlaggedQueryItem(BaseModel):
    id: str
    query: str
    response: str
    language: str
    confidence: float
    timestamp: str
    status: Literal["pending", "reviewed", "resolved"]
    reviewer_notes: Optional[str] = None

class KnowledgeBaseEntry(BaseModel):
    id: str
    category: str
    title: str
    content_en: str
    content_hi: str
    content_kn: str
    source: str

# ─── NER ─────────────────────────────────────────────────────────────────────

class NERResult(BaseModel):
    entity_type: str    # CROP | PEST | DISEASE | CHEMICAL | SCHEME | QUANTITY | LOCATION
    entity_value: str
    canonical_name: str
    hf_score: Optional[float] = None

# ─── Session State (for API exposure if needed) ───────────────────────────────

class SessionSummary(BaseModel):
    session_id: str
    language: str
    location: str
    turn_count: int
    last_intent: Optional[str] = None
    last_crop_context: Optional[str] = None
    is_active: bool = True
