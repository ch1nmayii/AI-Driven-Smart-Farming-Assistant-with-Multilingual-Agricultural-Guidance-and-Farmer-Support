import re
from typing import Tuple, Dict, Any

class NLPProcessor:
    def __init__(self):
        # Unicode ranges: Devanagari 0900-097F, Kannada 0C80-0CFF
        self.devanagari_regex = re.compile(r'[\u0900-\u097F]')
        self.kannada_regex = re.compile(r'[\u0C80-\u0CFF]')

    def detect_language(self, text: str) -> str:
        """Detect language based on Indic script characters, falling back to English."""
        if not text:
            return "en"
        
        devanagari_chars = len(self.devanagari_regex.findall(text))
        kannada_chars = len(self.kannada_regex.findall(text))
        
        if devanagari_chars > 0 and devanagari_chars >= kannada_chars:
            return "hi"
        elif kannada_chars > 0:
            return "kn"
        return "en"

    def classify_intent(self, text: str) -> str:
        """
        Classifies intent into:
        - pest_disease: Crop disease, pest remedies, sprays
        - scheme_subsidy: PM-Kisan, PMFBY, government aid
        - mandi_prices: Current market rates, APMC prices
        - soil_fertilizer: Urea, DAP, soil tests
        - weather_forecast: Rainfall, temperature advisories
        - general_advisory: General farming questions
        """
        text_lower = text.lower()
        
        # Pests & Diseases
        pest_keywords = ["कीड़ा", "रतुआ", "रोग", "कीट", "दवा", "छिड़काव", "pest", "disease", "rust", "blight", "spray", "ಹುಳು", "ರೋಗ", "ಔಷಧಿ"]
        if any(kw in text_lower for kw in pest_keywords):
            return "pest_disease"

        # Government Schemes
        scheme_keywords = ["योजना", "सब्सिडी", "पीएम किसान", "सम्मान निधि", "बीमा", "scheme", "subsidy", "pm kisan", "pmfby", "ಯೋಜನೆ", "ಸಬ್ಸಿಡಿ", "ವಿಮೆ"]
        if any(kw in text_lower for kw in scheme_keywords):
            return "scheme_subsidy"

        # Mandi / Market Prices
        mandi_keywords = ["मंडी", "भाव", "दाम", "कीमत", "रेट", "mandi", "market", "price", "rate", "ಮಾರುಕಟ್ಟೆ", "ಬೆಲೆ", "ದರ"]
        if any(kw in text_lower for kw in mandi_keywords):
            return "mandi_prices"

        # Soil & Fertilizer
        soil_keywords = ["खाद", "यूरिया", "डीएपी", "उर्वरक", "मिट्टी", "fertilizer", "urea", "dap", "soil", "NPK", "ಗೊಬ್ಬರ", "ಯೂರಿಯಾ", "ಮಣ್ಣು"]
        if any(kw in text_lower for kw in soil_keywords):
            return "soil_fertilizer"

        # Weather
        weather_keywords = ["मौसम", "बारिश", "तापमान", "पानी", "weather", "rain", "temperature", "ಹವಾಮಾನ", "ಮಳೆ"]
        if any(kw in text_lower for kw in weather_keywords):
            return "weather_forecast"

        return "general_advisory"

nlp_processor = NLPProcessor()
