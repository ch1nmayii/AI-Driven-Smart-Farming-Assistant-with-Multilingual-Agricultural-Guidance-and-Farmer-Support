from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

LanguageCode = Literal["hi", "kn", "en"]

class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or transcribed text")
    language: LanguageCode = Field(default="hi", description="ISO code: 'hi' for Hindi, 'kn' for Kannada, 'en' for English")
    session_id: Optional[str] = Field(default="farmer-session-default", description="Conversation session ID")
    location: Optional[str] = Field(default="Uttar Pradesh", description="Farmer state / district for weather and mandi price context")
    crop_context: Optional[str] = Field(default=None, description="Optional crop being queried (e.g., wheat, rice, tomato)")

class ChatResponse(BaseModel):
    response_text: str = Field(..., description="Multilingual response text in farmer's selected language")
    audio_base64: Optional[str] = Field(default=None, description="Base64 encoded synthesized speech audio for instant playback")
    audio_url: Optional[str] = Field(default=None, description="Direct URL or data URI for TTS audio playback")
    language: str
    intent: str
    confidence_score: float = Field(default=0.92, description="RAG and answer quality confidence score (0.0 to 1.0)")
    flagged_for_review: bool = Field(default=False, description="Whether flagged for agricultural extension worker review")
    sources: List[str] = Field(default_factory=list, description="Grounding sources (e.g. ICAR, Kisan Call Center)")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class AudioSTTResponse(BaseModel):
    transcription: str
    detected_language: str
    confidence: float

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
    category: str  # crops, pests, soil, schemes, market
    title: str
    content_en: str
    content_hi: str
    content_kn: str
    source: str
