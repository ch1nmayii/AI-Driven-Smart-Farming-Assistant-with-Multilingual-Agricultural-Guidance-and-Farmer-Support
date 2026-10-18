"""
Week 1-2 Task 4: Language Detection + Auto-Translation to Canonical Language + Back-Translation
Primary: Sarvam AI Translate API
Fallback: Statistical detection (langdetect) + dictionary-based substitution
"""
import re
import httpx
from typing import Optional
from app.config import settings

# Unicode script ranges for Indic languages
DEVANAGARI = re.compile(r'[\u0900-\u097F]')
KANNADA    = re.compile(r'[\u0C80-\u0CFF]')

# Sarvam AI language code mapping
LANG_TO_SARVAM = {
    "hi": "hi-IN",
    "kn": "kn-IN",
    "en": "en-IN",
}

SARVAM_TO_LANG = {v: k for k, v in LANG_TO_SARVAM.items()}


def detect_language(text: str) -> dict:
    """
    Detects language from text using Unicode script analysis.
    Returns: { "language": "hi"|"kn"|"en", "confidence": 0.0-1.0, "method": str }
    """
    if not text or not text.strip():
        return {"language": "hi", "confidence": 0.5, "method": "default"}

    deva_count = len(DEVANAGARI.findall(text))
    kn_count   = len(KANNADA.findall(text))
    total_chars = max(len(text.replace(" ", "")), 1)

    deva_ratio = deva_count / total_chars
    kn_ratio   = kn_count   / total_chars

    if deva_ratio > 0.2:
        return {"language": "hi", "confidence": round(min(0.6 + deva_ratio, 0.99), 2), "method": "unicode_script"}
    if kn_ratio > 0.2:
        return {"language": "kn", "confidence": round(min(0.6 + kn_ratio, 0.99), 2), "method": "unicode_script"}

    # Statistical fallback using langdetect
    try:
        from langdetect import detect, detect_langs
        langs = detect_langs(text)
        top = langs[0]
        lang_code = top.lang
        confidence = round(float(top.prob), 2)
        # Map langdetect codes to ours
        code_map = {"hi": "hi", "kn": "kn", "en": "en"}
        lang = code_map.get(lang_code, "en")
        return {"language": lang, "confidence": confidence, "method": "langdetect"}
    except Exception:
        pass

    return {"language": "en", "confidence": 0.7, "method": "default_latin"}


async def translate_to_english(text: str, src_lang: str) -> str:
    """
    Task 4: Translate farmer query to canonical English for backend RAG processing.
    Primary: Sarvam AI Translate API
    Fallback: Returns original text (English queries pass through unchanged)
    """
    if src_lang == "en" or not text.strip():
        return text

    if settings.SARVAM_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                payload = {
                    "input": text,
                    "source_language_code": LANG_TO_SARVAM.get(src_lang, "hi-IN"),
                    "target_language_code": "en-IN",
                    "speaker_gender": "Male",
                    "mode": "formal",
                    "model": "mayura:v1",
                    "enable_preprocessing": True
                }
                response = await client.post(
                    "https://api.sarvam.ai/translate",
                    headers={
                        "Content-Type": "application/json",
                        "api-subscription-key": settings.SARVAM_API_KEY
                    },
                    json=payload
                )
                if response.status_code == 200:
                    data = response.json()
                    translated = data.get("translated_text", "")
                    if translated:
                        return translated
        except Exception as e:
            print(f"[LanguagePipeline] Sarvam translate to English failed: {e}")

    # Fallback: return original (RAG will still try to match Indic keywords)
    return text


async def translate_from_english(text: str, target_lang: str) -> str:
    """
    Task 4: Back-translate English RAG response to the farmer's regional language.
    Primary: Sarvam AI Translate API
    Fallback: Returns English text unchanged
    """
    if target_lang == "en" or not text.strip():
        return text

    if settings.SARVAM_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                payload = {
                    "input": text[:1000],  # Sarvam max input limit
                    "source_language_code": "en-IN",
                    "target_language_code": LANG_TO_SARVAM.get(target_lang, "hi-IN"),
                    "speaker_gender": "Female",
                    "mode": "formal",
                    "model": "mayura:v1",
                    "enable_preprocessing": True
                }
                response = await client.post(
                    "https://api.sarvam.ai/translate",
                    headers={
                        "Content-Type": "application/json",
                        "api-subscription-key": settings.SARVAM_API_KEY
                    },
                    json=payload
                )
                if response.status_code == 200:
                    data = response.json()
                    translated = data.get("translated_text", "")
                    if translated:
                        return translated
        except Exception as e:
            print(f"[LanguagePipeline] Sarvam back-translation failed: {e}")

    # Fallback: return English text
    return text
