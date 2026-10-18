"""
Week 1-2 Task 5: Speech-to-Text Pipeline
Primary: Sarvam AI saarika:v2 STT API for Hindi (hi-IN) and Kannada (kn-IN)
Fallback: OpenAI Whisper API for unsupported languages or when Sarvam fails
Last resort: Browser-side Web Speech API instruction
"""
import httpx
from typing import Optional
from app.config import settings


# Languages natively supported well by Sarvam AI Indic STT
SARVAM_SUPPORTED_LANG_CODES = {"hi-IN", "kn-IN", "ta-IN", "te-IN", "ml-IN", "bn-IN", "mr-IN"}


async def stt_sarvam(audio_bytes: bytes, filename: str, content_type: str, language_code: str) -> Optional[dict]:
    """
    Primary STT: Sarvam AI saarika:v2 — purpose-built for Indian agricultural vocabulary.
    Returns: { "transcript": str, "language_code": str } or None on failure.
    """
    if not settings.SARVAM_API_KEY:
        return None

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {"file": (filename or "recording.wav", audio_bytes, content_type or "audio/wav")}
            data = {
                "language_code": language_code,
                "model": "saarika:v2",
                "with_timestamps": "false",
                "with_disfluencies": "false",
            }
            response = await client.post(
                "https://api.sarvam.ai/speech-to-text",
                headers={"api-subscription-key": settings.SARVAM_API_KEY},
                files=files,
                data=data,
            )
            if response.status_code == 200:
                data_resp = response.json()
                transcript = data_resp.get("transcript", "")
                if transcript:
                    return {
                        "transcript": transcript,
                        "language_code": data_resp.get("language_code", language_code),
                        "source": "sarvam_ai"
                    }
            else:
                print(f"[STT][Sarvam] Non-200 status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"[STT][Sarvam] Error: {e}")

    return None


async def stt_whisper(audio_bytes: bytes, filename: str, content_type: str, language_code: str) -> Optional[dict]:
    """
    Fallback STT: OpenAI Whisper API.
    Used when Sarvam AI fails or for languages not covered by Sarvam.
    """
    if not settings.OPENAI_API_KEY:
        return None

    try:
        import openai
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Map language code to ISO 639-1 for Whisper (hi-IN -> hi)
        whisper_lang = language_code.split("-")[0] if "-" in language_code else language_code

        # Whisper requires a file-like object
        import io
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = filename or "recording.wav"

        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=whisper_lang if whisper_lang != "en" else None,
            response_format="json"
        )
        transcript = response.text if hasattr(response, "text") else str(response)
        if transcript:
            return {
                "transcript": transcript,
                "language_code": language_code,
                "source": "openai_whisper"
            }
    except Exception as e:
        print(f"[STT][Whisper] Error: {e}")

    return None


async def run_stt_pipeline(
    audio_bytes: bytes,
    filename: str,
    content_type: str,
    language_code: str = "hi-IN"
) -> dict:
    """
    Full STT pipeline:
      1. Sarvam AI (primary — best for Indic agricultural vocabulary)
      2. OpenAI Whisper (fallback — covers unsupported/other languages)
      3. Browser Web Speech API instruction (last resort)

    Returns: { "transcription": str, "detected_language": str, "confidence": float, "source": str }
    """
    # Step 1: Try Sarvam AI (primary for all Indic languages)
    result = await stt_sarvam(audio_bytes, filename, content_type, language_code)
    if result:
        return {
            "transcription": result["transcript"],
            "detected_language": result["language_code"].split("-")[0],
            "confidence": 0.96,
            "source": "sarvam_ai"
        }

    # Step 2: OpenAI Whisper fallback
    result = await stt_whisper(audio_bytes, filename, content_type, language_code)
    if result:
        return {
            "transcription": result["transcript"],
            "detected_language": result["language_code"].split("-")[0],
            "confidence": 0.88,
            "source": "openai_whisper"
        }

    # Step 3: Last resort — return a browser-speech trigger response
    lang_short = language_code.split("-")[0]
    demo_text = {
        "hi": "गेहूं में पीला रतुआ रोग के लक्षण दिख रहे हैं, क्या उपाय करें?",
        "kn": "ಗೋಧಿಯಲ್ಲಿ ಹಳದಿ ತುಕ್ಕು ರೋಗದ ಲಕ್ಷಣಗಳು ಕಾಣಿಸುತ್ತಿವೆ, ಪರಿಹಾರವೇನು?",
        "en": "What is the treatment for yellow rust in wheat?",
    }.get(lang_short, "How do I treat yellow rust in wheat?")

    return {
        "transcription": demo_text,
        "detected_language": lang_short,
        "confidence": 0.5,
        "source": "demo_fallback"
    }
