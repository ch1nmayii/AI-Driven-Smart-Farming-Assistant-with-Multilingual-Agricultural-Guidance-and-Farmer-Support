export type Language = 'hi' | 'kn' | 'en';

export interface UIStrings {
  appTitle: string;
  appSubtitle: string;
  tapToSpeak: string;
  listening: string;
  thinking: string;
  tapToStop: string;
  speakPrompt: string;
  typePlaceholder: string;
  send: string;
  weatherTitle: string;
  mandiTitle: string;
  adminLink: string;
  farmerView: string;
  offlineNotice: string;
  audioPlaying: string;
  clearHistory: string;
  sampleQuestionsTitle: string;
  sampleQuestions: string[];
}

export const translations: Record<Language, UIStrings> = {
  hi: {
    appTitle: "किसान साथी एआई (Kisan AI)",
    appSubtitle: "आपकी अपनी भाषा में कृषि विशेषज्ञ सलाह और सरकारी योजनाएं",
    tapToSpeak: "बोलने के लिए माइक दबाएं",
    listening: "सुन रहे हैं... बोलिए",
    thinking: "कृषि विशेषज्ञ सलाह तैयार हो रही है...",
    tapToStop: "रोकने के लिए दबाएं",
    speakPrompt: "फसल, रोग, खाद, मंडी भाव या योजनाओं के बारे में पूछें",
    typePlaceholder: "या यहाँ अपना सवाल लिखें...",
    send: "पूछें",
    weatherTitle: "आज का मौसम और कृषि सलाह",
    mandiTitle: "ताज़ा मंडी भाव",
    adminLink: "कृषि विस्तार डैशबोर्ड",
    farmerView: "किसान इंटरफ़ेस",
    offlineNotice: "ऑफ़लाइन मोड — सवाल पूछने के लिए इंटरनेट कनेक्ट करें",
    audioPlaying: "सलाह बोली जा रही है...",
    clearHistory: "बातचीत मिटाएं",
    sampleQuestionsTitle: "अक्सर पूछे जाने वाले सवाल:",
    sampleQuestions: [
      "गेहूं में पीला रतुआ रोग का क्या उपाय है?",
      "पीएम किसान सम्मान निधि में ₹2000 कैसे मिलेंगे?",
      "धान में तना छेदक कीट की रोकथाम कैसे करें?",
      "टमाटर में झुलसा रोग की कौन सी दवा डालें?"
    ]
  },
  kn: {
    appTitle: "ಕಿಸಾನ್ ಎಐ (Kisan AI)",
    appSubtitle: "ನಿಮ್ಮದೇ ಭಾಷೆಯಲ್ಲಿ ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಮತ್ತು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
    tapToSpeak: "ಮಾತನಾಡಲು ಮೈಕ್ ಒತ್ತಿರಿ",
    listening: "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇವೆ... ಮಾತನಾಡಿ",
    thinking: "ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಸಿದ್ಧವಾಗುತ್ತಿದೆ...",
    tapToStop: "ನಿಲ್ಲಿಸಲು ಒತ್ತಿರಿ",
    speakPrompt: "ಬೆಳೆ, ರೋಗ, ಗೊಬ್ಬರ, ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಅಥವಾ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ",
    typePlaceholder: "ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
    send: "ಕೇಳಿ",
    weatherTitle: "ಇಂದಿನ ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ",
    mandiTitle: "ತಾಜಾ ಮಾರುಕಟ್ಟೆ ದರಗಳು",
    adminLink: "ಕೃಷಿ ಅಧಿಕಾರಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    farmerView: "ರೈತ ಇಂಟರ್‌ಫೇಸ್",
    offlineNotice: "ಆಫ್‌ಲೈನ್ ಮೋಡ್ — ಹೊಸ ಪ್ರಶ್ನೆ ಕೇಳಲು ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕಿಸಿ",
    audioPlaying: "ಸಲಹೆಯನ್ನು ಓದಲಾಗುತ್ತಿದೆ...",
    clearHistory: "ಇತಿಹಾಸ ಅಳಿಸಿ",
    sampleQuestionsTitle: "ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳು:",
    sampleQuestions: [
      "ಗೋಧಿಯಲ್ಲಿ ಹಳದಿ ತುಕ್ಕು ರೋಗಕ್ಕೆ ಪರಿಹಾರವೇನು?",
      "ಪಿಎಂ ಕಿಸಾನ್ ₹2000 ಕಂತು ಪಡೆಯುವುದು ಹೇಗೆ?",
      "ಭತ್ತದ ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು ನಿಯಂತ್ರಣ ಹೇಗೆ?",
      "ಟೊಮ್ಯಾಟೊ ಅಂಗಮಾರಿ ರೋಗಕ್ಕೆ ಔಷಧ ತಿಳಿಸಿ"
    ]
  },
  en: {
    appTitle: "Kisan AI Assistant",
    appSubtitle: "Multilingual AI Agricultural Guidance & Voice Support",
    tapToSpeak: "Tap Microphone to Speak",
    listening: "Listening... Please speak",
    thinking: "Analyzing with Agricultural Knowledge Base...",
    tapToStop: "Tap to stop",
    speakPrompt: "Ask anything about crops, pests, soil, mandi prices, or schemes",
    typePlaceholder: "Or type your farming question here...",
    send: "Send",
    weatherTitle: "Weather & Agromet Advisory",
    mandiTitle: "Live Mandi Rates",
    adminLink: "Extension Worker Portal",
    farmerView: "Farmer View",
    offlineNotice: "Offline Mode — Connect to internet to ask new questions",
    audioPlaying: "Reading response aloud...",
    clearHistory: "Clear Chat",
    sampleQuestionsTitle: "Frequently Asked Questions:",
    sampleQuestions: [
      "How to control yellow rust in wheat?",
      "How to register for PM-KISAN ₹6,000 benefit?",
      "What is the remedy for stem borer in paddy?",
      "Best fungicide for tomato late blight?"
    ]
  }
};
