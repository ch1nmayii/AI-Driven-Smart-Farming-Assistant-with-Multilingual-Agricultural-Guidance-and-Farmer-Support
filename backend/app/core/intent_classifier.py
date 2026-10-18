"""
Week 1-2 Task 2: Hugging Face models for Intent Classification on agricultural vocabulary.
Multi-class intent classification with confidence scoring.
Uses weighted keyword scoring + HuggingFace zero-shot classification (optional).

Intent Classes:
  pest_disease     - crop disease and pest queries
  scheme_subsidy   - government scheme eligibility and benefit queries
  mandi_prices     - wholesale market price queries
  soil_fertilizer  - soil health and fertilizer application queries
  weather_forecast - weather and rainfall advisory queries
  crop_sowing      - sowing calendar, variety selection queries
  general_advisory - general agricultural guidance
"""
from typing import Dict, List, Tuple

# ─── Weighted keyword dictionary per intent ───────────────────────────────────
# Format: { "intent": [(keyword, weight), ...] }
# Higher weight = stronger signal for that intent

INTENT_KEYWORDS: Dict[str, List[Tuple[str, float]]] = {
    "pest_disease": [
        # Hindi
        ("कीड़ा", 3.0), ("कीट", 3.0), ("रतुआ", 3.5), ("रोग", 2.5), ("झुलसा", 3.5),
        ("दवा", 2.0), ("छिड़काव", 2.5), ("फफूंद", 3.0), ("सुंडी", 3.0), ("माहू", 3.0),
        ("मुरझाना", 2.5), ("पत्ती पर धब्बे", 3.0), ("नाशक", 2.5),
        # Kannada
        ("ಹುಳು", 3.0), ("ರೋಗ", 2.5), ("ತುಕ್ಕು", 3.5), ("ಅಂಗಮಾರಿ", 3.5),
        ("ಔಷಧಿ", 2.0), ("ಸಿಂಪಡಣೆ", 2.5), ("ಶಿಲೀಂಧ್ರ", 3.0), ("ಕೀಟ", 3.0),
        # English
        ("pest", 3.0), ("disease", 2.5), ("rust", 3.5), ("blight", 3.5),
        ("spray", 2.5), ("fungicide", 3.0), ("insecticide", 3.0), ("pesticide", 3.0),
        ("wilt", 3.0), ("mildew", 3.0), ("stem borer", 3.5), ("armyworm", 3.5),
        ("bollworm", 3.5), ("aphid", 3.0), ("whitefly", 3.0), ("leaf spot", 3.0),
        ("blast", 3.0), ("control", 1.5), ("treatment", 2.0), ("remedy", 2.5),
    ],
    "scheme_subsidy": [
        # Hindi
        ("योजना", 3.0), ("सब्सिडी", 3.5), ("पीएम किसान", 4.0), ("सम्मान निधि", 4.0),
        ("बीमा", 3.5), ("फसल बीमा", 4.0), ("क्रेडिट कार्ड", 3.5), ("अनुदान", 3.0),
        ("मुआवजा", 3.0), ("किसान क्रेडिट", 3.5), ("मिट्टी स्वास्थ्य कार्ड", 3.5),
        ("पंजीकरण", 2.5), ("आवेदन", 2.5), ("पात्रता", 3.0),
        # Kannada
        ("ಯೋಜನೆ", 3.0), ("ಸಬ್ಸಿಡಿ", 3.5), ("ಪಿಎಂ ಕಿಸಾನ್", 4.0), ("ಬೆಳೆ ವಿಮೆ", 4.0),
        ("ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್", 3.5), ("ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ", 3.5),
        # English
        ("pm kisan", 4.0), ("pmfby", 4.0), ("scheme", 3.0), ("subsidy", 3.5),
        ("crop insurance", 4.0), ("kisan credit card", 3.5), ("kcc", 3.0),
        ("soil health card", 3.5), ("enam", 3.0), ("smam", 3.0), ("benefit", 2.0),
        ("eligibility", 3.0), ("register", 2.5), ("apply", 2.0), ("government", 2.0),
    ],
    "mandi_prices": [
        # Hindi
        ("मंडी", 4.0), ("भाव", 3.5), ("दाम", 3.0), ("कीमत", 3.0), ("रेट", 3.0),
        ("बाजार", 3.0), ("एपीएमसी", 3.5), ("थोक", 3.0), ("बिक्री", 2.0),
        # Kannada
        ("ಮಾರುಕಟ್ಟೆ", 3.5), ("ಬೆಲೆ", 3.0), ("ದರ", 3.0), ("ಎಪಿಎಂಸಿ", 3.5),
        # English
        ("mandi", 4.0), ("market price", 4.0), ("apmc", 4.0), ("rate", 3.0),
        ("price", 3.0), ("wholesale", 3.5), ("agmarknet", 4.0), ("sell", 2.0),
        ("selling price", 3.5), ("commodity price", 3.5), ("quintal", 2.5),
    ],
    "soil_fertilizer": [
        # Hindi
        ("खाद", 3.5), ("यूरिया", 4.0), ("डीएपी", 4.0), ("उर्वरक", 3.5),
        ("मिट्टी", 3.0), ("एनपीके", 3.5), ("नाइट्रोजन", 3.0), ("फास्फोरस", 3.0),
        ("पोटाश", 3.0), ("मृदा", 3.0), ("खेत की मिट्टी", 3.5), ("जैविक", 2.5),
        ("जैव खाद", 3.0), ("कम्पोस्ट", 3.0), ("वर्मीकम्पोस्ट", 3.0),
        # Kannada
        ("ಗೊಬ್ಬರ", 3.5), ("ಯೂರಿಯಾ", 4.0), ("ಡಿಎಪಿ", 4.0), ("ಮಣ್ಣು", 3.0),
        ("ರಸಗೊಬ್ಬರ", 3.5), ("ಸಾವಯವ", 2.5), ("ಕಾಂಪೋಸ್ಟ್", 3.0),
        # English
        ("urea", 4.0), ("dap", 4.0), ("fertilizer", 3.5), ("npk", 3.5),
        ("soil", 3.0), ("nitrogen", 3.0), ("phosphorus", 3.0), ("potash", 3.0),
        ("organic", 2.5), ("compost", 3.0), ("vermicompost", 3.0),
        ("soil test", 3.5), ("soil health", 3.5), ("micronutrient", 3.0),
    ],
    "weather_forecast": [
        # Hindi
        ("मौसम", 4.0), ("बारिश", 3.5), ("तापमान", 3.5), ("वर्षा", 3.5),
        ("ओलावृष्टि", 3.5), ("सूखा", 3.0), ("बाढ़", 3.0), ("पाला", 3.5),
        # Kannada
        ("ಹವಾಮಾನ", 4.0), ("ಮಳೆ", 3.5), ("ತಾಪಮಾನ", 3.5), ("ಬರ", 3.0), ("ಪ್ರವಾಹ", 3.0),
        # English
        ("weather", 4.0), ("rain", 3.5), ("rainfall", 3.5), ("temperature", 3.5),
        ("drought", 3.0), ("flood", 3.0), ("frost", 3.5), ("hail", 3.5),
        ("forecast", 3.5), ("imd", 3.0), ("monsoon", 3.0), ("sowing advisory", 3.0),
    ],
    "crop_sowing": [
        # Hindi
        ("बुवाई", 4.0), ("बीज", 3.5), ("रोपाई", 3.5), ("किस्म", 3.5),
        ("फसल चक्र", 3.5), ("खरीफ", 3.5), ("रबी", 3.5), ("जायद", 3.0),
        ("उन्नत किस्म", 3.5), ("बीजोपचार", 3.5),
        # Kannada
        ("ಬಿತ್ತನೆ", 4.0), ("ಬೀಜ", 3.5), ("ತಳಿ", 3.5), ("ಖಾರೀಫ್", 3.5), ("ರಬಿ", 3.5),
        ("ಬೆಳೆ ಚಕ್ರ", 3.5), ("ನಾಟಿ", 3.5),
        # English
        ("sowing", 4.0), ("planting", 3.5), ("seed", 3.5), ("variety", 3.5),
        ("crop rotation", 3.5), ("kharif", 3.5), ("rabi", 3.5), ("nursery", 3.0),
        ("transplant", 3.0), ("seed treatment", 3.5), ("germination", 3.0),
        ("spacing", 2.5), ("when to sow", 3.5),
    ],
    "general_advisory": [
        # Default fallback - low weight to always be a candidate
        ("farming", 1.0), ("agriculture", 1.0), ("crop", 1.0), ("खेती", 1.0),
        ("फसल", 1.0), ("ಕೃಷಿ", 1.0), ("ಬೆಳೆ", 1.0), ("help", 0.5), ("advice", 1.0),
    ],
}


# ─── HuggingFace Zero-Shot Intent Classifier (optional) ──────────────────────

_hf_classifier = None
CANDIDATE_LABELS = [
    "crop pest and disease control",
    "government agriculture scheme and subsidy",
    "market price and mandi rate",
    "soil health and fertilizer",
    "weather forecast and farming advisory",
    "crop sowing and variety selection",
    "general farming question",
]

def _get_hf_classifier():
    global _hf_classifier
    if _hf_classifier is None:
        try:
            from transformers import pipeline
            _hf_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # CPU
            )
            print("[IntentClassifier] HuggingFace zero-shot classifier loaded (CPU)")
        except Exception as e:
            print(f"[IntentClassifier] HuggingFace unavailable, using keyword scoring only: {e}")
            _hf_classifier = "unavailable"
    return _hf_classifier if _hf_classifier != "unavailable" else None


LABEL_TO_INTENT = {
    "crop pest and disease control":          "pest_disease",
    "government agriculture scheme and subsidy": "scheme_subsidy",
    "market price and mandi rate":            "mandi_prices",
    "soil health and fertilizer":             "soil_fertilizer",
    "weather forecast and farming advisory":  "weather_forecast",
    "crop sowing and variety selection":      "crop_sowing",
    "general farming question":               "general_advisory",
}


class IntentClassifier:
    """
    Multi-class intent classifier combining:
    1. Weighted keyword scoring (fast, Indic-aware, always runs)
    2. HuggingFace zero-shot classification (English, best-effort)
    """

    def classify(self, text: str) -> Dict:
        """
        Classify query intent.
        Returns: {
          "intent": str,
          "confidence": float (0.0-1.0),
          "scores": {intent: score, ...},
          "method": "keyword" | "hybrid"
        }
        """
        keyword_result = self._keyword_classify(text)

        # Try HuggingFace zero-shot only for English queries with enough words
        import re
        if re.search(r'[a-zA-Z]{4,}', text) and len(text.split()) >= 3:
            hf = _get_hf_classifier()
            if hf:
                try:
                    result = hf(text[:256], CANDIDATE_LABELS)
                    top_label = result["labels"][0]
                    top_score = result["scores"][0]
                    hf_intent = LABEL_TO_INTENT.get(top_label, "general_advisory")

                    # Blend: 60% keyword + 40% HuggingFace
                    kw_score = keyword_result["scores"].get(keyword_result["intent"], 0)
                    blended_confidence = round(0.6 * kw_score + 0.4 * top_score, 3)

                    # Use HF if it strongly disagrees AND has high confidence
                    if hf_intent != keyword_result["intent"] and top_score > 0.75:
                        return {
                            "intent": hf_intent,
                            "confidence": blended_confidence,
                            "scores": keyword_result["scores"],
                            "method": "hybrid"
                        }
                    else:
                        return {
                            "intent": keyword_result["intent"],
                            "confidence": blended_confidence,
                            "scores": keyword_result["scores"],
                            "method": "hybrid"
                        }
                except Exception:
                    pass

        return keyword_result

    def _keyword_classify(self, text: str) -> Dict:
        """Weighted keyword scoring across all intent classes."""
        text_lower = text.lower()
        scores: Dict[str, float] = {}

        for intent, keywords in INTENT_KEYWORDS.items():
            score = 0.0
            for kw, weight in keywords:
                if kw.lower() in text_lower:
                    score += weight
            scores[intent] = round(score, 2)

        # Always ensure general_advisory has a minimum baseline score
        scores["general_advisory"] = max(scores.get("general_advisory", 0), 0.5)

        top_intent = max(scores, key=lambda k: scores[k])
        top_score = scores[top_intent]

        # Normalize confidence to 0-1 range (cap at reasonable max)
        max_possible = 20.0
        confidence = round(min(top_score / max_possible, 0.99), 3)
        if top_score == 0.5:  # only general_advisory baseline
            confidence = 0.45

        return {
            "intent": top_intent,
            "confidence": confidence,
            "scores": scores,
            "method": "keyword"
        }


intent_classifier = IntentClassifier()
