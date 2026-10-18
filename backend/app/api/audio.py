"""
Week 1-2: Updated Audio API
- STT: Uses STTPipeline (Sarvam AI primary → OpenAI Whisper fallback)
- TTS: Sarvam AI bulbul:v1 with per-language speaker selection
- Translation: Sarvam AI Translate endpoint
"""
import httpx
from fastapi import APIRouter, UploadFile, File, Form
from app.models.schemas import AudioSTTResponse, TranslationRequest, TranslationResponse
from app.config import settings
from app.core.stt_pipeline import run_stt_pipeline
from app.core.language_pipeline import translate_to_english, translate_from_english

router = APIRouter(prefix="/api/audio", tags=["Audio & Speech"])


@router.post("/stt", response_model=AudioSTTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language_code: str = Form("hi-IN")
):
    """
    Speech-to-Text endpoint.
    Primary: Sarvam AI saarika:v2 (Indic-optimised for Hindi, Kannada agricultural vocabulary)
    Fallback: OpenAI Whisper-1 (for unsupported languages or when Sarvam AI is unavailable)
    """
    audio_bytes = await audio.read()
    result = await run_stt_pipeline(
        audio_bytes=audio_bytes,
        filename=audio.filename or "recording.wav",
        content_type=audio.content_type or "audio/wav",
        language_code=language_code
    )
    return AudioSTTResponse(
        transcription=result["transcription"],
        detected_language=result["detected_language"],
        confidence=result["confidence"],
        stt_source=result["source"]
    )


@router.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    language_code: str = Form("hi-IN")
):
    """
    Text-to-Speech endpoint.
    Primary: Sarvam AI bulbul:v1 with gender/language-specific speaker selection.
    Fallback: Browser Web Speech Synthesis API instruction.
    """
    # Select speaker voice per language for natural Indic output
    speaker_map = {
        "hi-IN": "meera",   # Female Hindi speaker
        "kn-IN": "amol",    # Male Kannada speaker
        "en-IN": "arjun",   # Male English speaker
    }
    speaker = speaker_map.get(language_code, "meera")

    if settings.SARVAM_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "inputs": [text[:500]],
                    "target_language_code": language_code,
                    "speaker": speaker,
                    "pitch": 0,
                    "pace": 0.95,       # Slightly slower for rural clarity
                    "loudness": 1.5,
                    "speech_sample_rate": 22050,
                    "enable_preprocessing": True,
                    "model": "bulbul:v1"
                }
                response = await client.post(
                    "https://api.sarvam.ai/text-to-speech",
                    headers={
                        "Content-Type": "application/json",
                        "api-subscription-key": settings.SARVAM_API_KEY
                    },
                    json=payload
                )
                if response.status_code == 200:
                    data = response.json()
                    audios = data.get("audios", [])
                    if audios:
                        return {"audio_base64": audios[0], "format": "wav", "source": "sarvam_ai"}
        except Exception as e:
            print(f"[TTS][Sarvam] Error: {e}")

    return {
        "audio_base64": None,
        "format": "browser-speech",
        "source": "browser_fallback",
        "message": "Use Web Speech Synthesis API in browser"
    }


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translation endpoint.
    Translates text between hi, kn, en using Sarvam AI Translate (mayura:v1).
    If target is 'en', uses translate_to_english.
    If source is 'en', uses translate_from_english.
    """
    if request.target_language == "en":
        translated = await translate_to_english(request.text, request.source_language)
    else:
        # Translate to target via English as pivot if needed
        en_text = await translate_to_english(request.text, request.source_language)
        translated = await translate_from_english(en_text, request.target_language)

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated,
        source_language=request.source_language,
        target_language=request.target_language,
        translation_source="sarvam_ai" if settings.SARVAM_API_KEY else "passthrough"
    )
