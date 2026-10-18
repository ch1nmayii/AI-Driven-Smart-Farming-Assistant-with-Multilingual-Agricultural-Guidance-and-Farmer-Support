import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "AI-Driven Smart Farming Assistant"
    PORT: int = int(os.getenv("PORT", "6000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    # Week 1-2: Sarvam AI (STT, TTS, Translation) - primary Indic AI layer
    SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
    # Week 1-2: OpenAI (Whisper STT fallback)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:6000",
        "http://127.0.0.1:6000",
        "*"
    ]
    DATA_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

settings = Settings()
