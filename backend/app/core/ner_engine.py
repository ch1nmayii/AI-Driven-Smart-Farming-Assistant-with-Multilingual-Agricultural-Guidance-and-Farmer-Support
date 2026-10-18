"""
Week 1-2 Task 2: Hugging Face models for Named Entity Recognition on agricultural vocabulary.
Uses a rule-based NER with curated agricultural dictionaries as a robust base
that works without GPU, supplemented by transformers pipeline when available.

Entity Types:
  CROP      - crop names (wheat, rice, tomato, cotton...)
  PEST      - insect pests (stem borer, aphid, whitefly...)
  DISEASE   - plant diseases (rust, blight, wilt...)
  CHEMICAL  - pesticides/fungicides/fertilizers (urea, DAP, mancozeb...)
  SCHEME    - government schemes (PM-KISAN, PMFBY...)
  QUANTITY  - dosages (1 ml/litre, 10 kg/acre...)
  LOCATION  - states/districts (Uttar Pradesh, Karnataka...)
"""
import re
from typing import List, Dict, Any, Optional

# ─── Curated Agricultural Entity Dictionaries ────────────────────────────────

CROP_ENTITIES = {
    "wheat":     ["wheat", "गेहूं", "गेहूँ", "ಗೋಧಿ"],
    "rice":      ["rice", "paddy", "dhaan", "धान", "ಭತ್ತ"],
    "cotton":    ["cotton", "kapas", "कपास", "ಹತ್ತಿ"],
    "tomato":    ["tomato", "tamatar", "टमाटर", "ಟೊಮ್ಯಾಟೊ"],
    "sugarcane": ["sugarcane", "ganna", "गन्ना", "ಕಬ್ಬು"],
    "maize":     ["maize", "corn", "makka", "मक्का", "ಮೆಕ್ಕೆ ಜೋಳ"],
    "potato":    ["potato", "aloo", "आलू", "ಆಲೂಗಡ್ಡೆ"],
    "onion":     ["onion", "pyaz", "प्याज", "ಈರುಳ್ಳಿ"],
    "mustard":   ["mustard", "sarson", "सरसों", "ಸಾಸಿವೆ"],
    "chickpea":  ["chickpea", "chana", "gram", "चना", "ಕಡಲೆ"],
    "soybean":   ["soybean", "soya", "सोयाबीन", "ಸೋಯಾ"],
    "groundnut": ["groundnut", "peanut", "moongfali", "मूंगफली", "ಕಡಲೆಕಾಯಿ"],
    "banana":    ["banana", "kela", "केला", "ಬಾಳೆ"],
    "mango":     ["mango", "aam", "आम", "ಮಾವು"],
    "ragi":      ["ragi", "finger millet", "ರಾಗಿ"],
}

PEST_ENTITIES = {
    "stem_borer":     ["stem borer", "tana chhedak", "तना छेदक", "ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು"],
    "aphid":          ["aphid", "mahu", "माहू", "ಮಾಹು", "ಜಿಗಿಹುಳು"],
    "whitefly":       ["whitefly", "white fly", "ಬಿಳಿ ನೊಣ"],
    "armyworm":       ["armyworm", "army worm", "fall armyworm", "ಸೈನ್ಯ ಹುಳು"],
    "thrips":         ["thrips", "ಥ್ರಿಪ್ಸ್"],
    "bollworm":       ["bollworm", "boll worm", "pink bollworm", "ಕಾಯಿ ಕೊರೆಯುವ ಹುಳು"],
    "leaf_miner":     ["leaf miner", "ಎಲೆ ತಿನ್ನುವ ಹುಳು"],
    "mealybug":       ["mealybug", "mealy bug", "ಹಿಟ್ಟು ತಿಗಣೆ"],
    "red_spider":     ["red spider mite", "spider mite", "ಕೆಂಪು ಜೇಡ"],
    "locust":         ["locust", "tida", "tiddi", "टिड्डी", "ಮಿಡತೆ"],
}

DISEASE_ENTITIES = {
    "yellow_rust":    ["yellow rust", "pila ratua", "पीला रतुआ", "stripe rust", "ಹಳದಿ ತುಕ್ಕು"],
    "brown_rust":     ["brown rust", "leaf rust", "ಕಂದು ತುಕ್ಕು"],
    "blight":         ["blight", "jhulaas", "झुलसा", "ಅಂಗಮಾರಿ"],
    "wilt":           ["wilt", "murjhana", "मुरझाना", "ಬಾಡು ರೋಗ"],
    "powdery_mildew": ["powdery mildew", "choorni rog", "चूर्णी रोग", "ಪುಡಿ ರೋಗ"],
    "downy_mildew":   ["downy mildew", "ಮೃದು ರೋಗ"],
    "mosaic":         ["mosaic", "mosaic virus", "ಮೊಸಾಯಿಕ್"],
    "leaf_spot":      ["leaf spot", "ಎಲೆ ಚುಕ್ಕಿ ರೋಗ"],
    "blast":          ["blast", "neck blast", "blast disease", "ಬ್ಲಾಸ್ಟ್ ರೋಗ"],
    "smut":           ["smut", "kangar", "कांगर", "ಕಂಬಳಿ ರೋಗ"],
}

CHEMICAL_ENTITIES = {
    "urea":          ["urea", "यूरिया", "ಯೂರಿಯಾ"],
    "dap":           ["dap", "diammonium phosphate", "डीएपी", "ಡಿಎಪಿ"],
    "mancozeb":      ["mancozeb", "mancozeb 75wp", "indofil m-45", "ಮ್ಯಾಂಕೋಜೆಬ್"],
    "propiconazole": ["propiconazole", "tilt", "ಪ್ರೊಪಿಕೊನಜೋಲ್"],
    "chlorpyrifos":  ["chlorpyrifos", "dursban", "ಕ್ಲೋರ್‌ಪೈರಿಫಾಸ್"],
    "imidacloprid":  ["imidacloprid", "confidor", "gaucho"],
    "npk":           ["npk", "np", "pk", "complex fertilizer"],
    "cartap":        ["cartap", "cartap hydrochloride", "padan"],
    "coragen":       ["coragen", "chlorantraniliprole", "ಕೊರಾಜೆನ್"],
    "ridomil":       ["ridomil", "ridomil gold", "metalaxyl", "ರಿಡೋಮಿಲ್"],
    "neem_oil":      ["neem oil", "neem", "neemicide", "ಬೇವಿನ ಎಣ್ಣೆ"],
}

SCHEME_ENTITIES = {
    "pm_kisan":  ["pm kisan", "pm-kisan", "pradhan mantri kisan", "पीएम किसान", "samman nidhi", "ಪಿಎಂ ಕಿಸಾನ್"],
    "pmfby":     ["pmfby", "fasal bima", "crop insurance", "फसल बीमा", "ಬೆಳೆ ವಿಮೆ"],
    "kcc":       ["kisan credit card", "kcc", "किसान क्रेडिट कार्ड", "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್"],
    "soil_card": ["soil health card", "shc", "mittti parikshan", "मिट्टी परीक्षण", "ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ"],
    "enam":      ["enam", "e-nam", "national agriculture market", "राष्ट्रीय कृषि बाजार"],
    "smam":      ["smam", "sub mission agricultural mechanization", "farm machinery"],
}

QUANTITY_PATTERN = re.compile(
    r'\d+(?:\.\d+)?\s*(?:ml|kg|g|gm|litre|liter|l|acre|hectare|quintal|ton|'
    r'मिली|किग्रा|ग्राम|लीटर|एकड़|हेक्टेयर|ಮಿ\.ಲೀ|ಕೆಜಿ|ಗ್ರಾಂ|ಲೀಟರ್|ಎಕರೆ)'
    r'(?:\s*/\s*(?:litre|liter|l|acre|hectare|plant|ಲೀಟರ್|ಎಕರೆ|लीटर|एकड़))?',
    re.IGNORECASE
)

LOCATION_ENTITIES = [
    "uttar pradesh", "karnataka", "maharashtra", "punjab", "haryana",
    "rajasthan", "madhya pradesh", "bihar", "gujarat", "andhra pradesh",
    "telangana", "tamil nadu", "kerala", "odisha", "west bengal",
    "उत्तर प्रदेश", "कर्नाटक", "महाराष्ट्र", "पंजाब", "हरियाणा",
    "ಕರ್ನಾಟಕ", "ಉತ್ತರ ಪ್ರದೇಶ", "ಮಹಾರಾಷ್ಟ್ರ",
]


# ─── HuggingFace Transformer NER (optional enhancement) ─────────────────────

_hf_ner_pipeline = None

def _get_hf_pipeline():
    """Lazily load HuggingFace NER pipeline. Works on CPU."""
    global _hf_ner_pipeline
    if _hf_ner_pipeline is None:
        try:
            from transformers import pipeline
            # Use a lightweight multilingual NER model
            _hf_ner_pipeline = pipeline(
                "token-classification",
                model="Jean-Baptiste/roberta-large-ner-english",
                aggregation_strategy="simple",
                device=-1  # CPU only
            )
            print("[NER] HuggingFace NER pipeline loaded (CPU mode)")
        except Exception as e:
            print(f"[NER] HuggingFace pipeline unavailable, using rule-based only: {e}")
            _hf_ner_pipeline = "unavailable"
    return _hf_ner_pipeline if _hf_ner_pipeline != "unavailable" else None


# ─── Main NER Engine ─────────────────────────────────────────────────────────

class NEREngine:
    """
    Named Entity Recognition for agricultural queries.
    Combines curated dictionary matching (fast, Indic-aware)
    with optional HuggingFace transformer NER for English queries.
    """

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract agricultural named entities from query text.
        Returns list of: { entity_type, entity_value, canonical_name, start, end }
        """
        entities = []
        text_lower = text.lower()

        # 1. Dictionary-based entity extraction (Hindi + Kannada + English)
        for canonical, variants in CROP_ENTITIES.items():
            for v in variants:
                if v.lower() in text_lower:
                    entities.append({"entity_type": "CROP", "entity_value": v, "canonical_name": canonical})
                    break

        for canonical, variants in PEST_ENTITIES.items():
            for v in variants:
                if v.lower() in text_lower:
                    entities.append({"entity_type": "PEST", "entity_value": v, "canonical_name": canonical})
                    break

        for canonical, variants in DISEASE_ENTITIES.items():
            for v in variants:
                if v.lower() in text_lower:
                    entities.append({"entity_type": "DISEASE", "entity_value": v, "canonical_name": canonical})
                    break

        for canonical, variants in CHEMICAL_ENTITIES.items():
            for v in variants:
                if v.lower() in text_lower:
                    entities.append({"entity_type": "CHEMICAL", "entity_value": v, "canonical_name": canonical})
                    break

        for canonical, variants in SCHEME_ENTITIES.items():
            for v in variants:
                if v.lower() in text_lower:
                    entities.append({"entity_type": "SCHEME", "entity_value": v, "canonical_name": canonical})
                    break

        for loc in LOCATION_ENTITIES:
            if loc.lower() in text_lower:
                entities.append({"entity_type": "LOCATION", "entity_value": loc, "canonical_name": loc})

        # 2. Quantity extraction using regex
        for match in QUANTITY_PATTERN.finditer(text):
            entities.append({"entity_type": "QUANTITY", "entity_value": match.group(), "canonical_name": match.group().strip()})

        # 3. Optional: HuggingFace NER for English queries (supplements dictionary)
        # Only runs if text is primarily English and pipeline loaded
        if re.search(r'[a-zA-Z]{3,}', text) and len(text.split()) > 3:
            hf = _get_hf_pipeline()
            if hf:
                try:
                    results = hf(text[:256])
                    for r in results:
                        if r.get("score", 0) > 0.85 and r.get("entity_group") in ("ORG", "LOC", "MISC"):
                            # Only take locations/orgs not already captured
                            val = r.get("word", "").strip()
                            if val and not any(e["entity_value"].lower() == val.lower() for e in entities):
                                entities.append({
                                    "entity_type": "LOCATION" if r["entity_group"] == "LOC" else "MISC",
                                    "entity_value": val,
                                    "canonical_name": val,
                                    "hf_score": round(r["score"], 3)
                                })
                except Exception as e:
                    pass  # HF NER is best-effort

        return entities

    def get_crop_context(self, entities: List[Dict]) -> Optional[str]:
        """Extract primary crop from entities list."""
        for e in entities:
            if e["entity_type"] == "CROP":
                return e["canonical_name"]
        return None

    def get_primary_pest_or_disease(self, entities: List[Dict]) -> Optional[str]:
        """Extract primary pest or disease from entities."""
        for e in entities:
            if e["entity_type"] in ("PEST", "DISEASE"):
                return e["canonical_name"]
        return None


from typing import Optional
ner_engine = NEREngine()
