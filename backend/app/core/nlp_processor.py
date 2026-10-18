"""
Week 1-2: Updated NLP Processor
Orchestrates: language detection → NER → intent classification → session context
"""
import re
from typing import Dict, Any, List, Optional
from app.core.language_pipeline import detect_language
from app.core.intent_classifier import intent_classifier
from app.core.ner_engine import ner_engine


class NLPProcessor:
    """
    Main NLP orchestrator combining:
    - Language detection (Indic script + langdetect)
    - Named Entity Recognition (agricultural vocab, Hugging Face supplemented)
    - Intent classification (keyword scoring + HuggingFace zero-shot)
    """

    def process_query(self, text: str, preferred_language: Optional[str] = None) -> Dict[str, Any]:
        """
        Full NLP processing pipeline for a farmer query.

        Steps:
          1. Detect language (Unicode script analysis + statistical fallback)
          2. Extract named entities (CROP, PEST, DISEASE, CHEMICAL, SCHEME, QUANTITY, LOCATION)
          3. Classify intent with confidence scoring

        Returns:
          {
            language: str,          # detected or preferred language code
            language_confidence: float,
            intent: str,            # classified intent
            intent_confidence: float,
            entities: list,         # NER results
            crop_context: str|None, # primary crop from entities
            pest_disease: str|None, # primary pest/disease
          }
        """
        if not text or not text.strip():
            return self._empty_result(preferred_language or "hi")

        # Step 1: Language Detection
        lang_result = detect_language(text)
        language = preferred_language if preferred_language else lang_result["language"]
        language_confidence = lang_result["confidence"]

        # Step 2: Named Entity Recognition
        entities = ner_engine.extract_entities(text)
        crop_context = ner_engine.get_crop_context(entities)
        pest_disease = ner_engine.get_primary_pest_or_disease(entities)

        # Step 3: Intent Classification
        intent_result = intent_classifier.classify(text)
        intent = intent_result["intent"]
        intent_confidence = intent_result["confidence"]

        return {
            "language": language,
            "language_confidence": language_confidence,
            "intent": intent,
            "intent_confidence": intent_confidence,
            "intent_scores": intent_result.get("scores", {}),
            "intent_method": intent_result.get("method", "keyword"),
            "entities": entities,
            "crop_context": crop_context,
            "pest_disease": pest_disease,
        }

    def _empty_result(self, language: str) -> Dict[str, Any]:
        return {
            "language": language,
            "language_confidence": 0.5,
            "intent": "general_advisory",
            "intent_confidence": 0.45,
            "intent_scores": {},
            "intent_method": "default",
            "entities": [],
            "crop_context": None,
            "pest_disease": None,
        }


nlp_processor = NLPProcessor()
