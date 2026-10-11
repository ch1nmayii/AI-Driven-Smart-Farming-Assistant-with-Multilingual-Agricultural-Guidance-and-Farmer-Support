'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Sprout,
  Send,
  Trash2,
  WifiOff,
  Shield,
  VolumeX,
  Volume2
} from 'lucide-react';
import { Language, translations } from '../lib/i18n';
import { LanguageSelector } from '../components/LanguageSelector';
import { VoiceMicButton } from '../components/VoiceMicButton';
import { AdvisoryCards } from '../components/AdvisoryCards';
import { ChatHistory } from '../components/ChatHistory';
import { sendChatMessage, ChatMessage } from '../lib/api';

export default function FarmerPWA() {
  const [language, setLanguage] = useState<Language>('hi');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [isOffline, setIsOffline] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(true);

  const t = translations[language];

  // Monitor network connectivity & register Service Worker
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsOffline(!navigator.onLine);
      const handleOnline = () => setIsOffline(false);
      const handleOffline = () => setIsOffline(true);

      window.addEventListener('online', handleOnline);
      window.addEventListener('offline', handleOffline);

      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(console.error);
      }

      // Restore cached session
      const saved = localStorage.getItem('kisan_chat_history');
      if (saved) {
        try {
          setMessages(JSON.parse(saved));
        } catch (e) {
          console.error(e);
        }
      }

      return () => {
        window.removeEventListener('online', handleOnline);
        window.removeEventListener('offline', handleOffline);
      };
    }
  }, []);

  // Cache messages locally for offline viewing
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('kisan_chat_history', JSON.stringify(messages));
    }
  }, [messages]);

  // Voice readback using browser SpeechSynthesis or audio playback
  const playSpeechAudio = (text: string, langCode: string) => {
    if (!audioEnabled || typeof window === 'undefined') return;

    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      
      const langVoiceMap: Record<string, string> = {
        hi: 'hi-IN',
        kn: 'kn-IN',
        en: 'en-IN'
      };
      utterance.lang = langVoiceMap[langCode] || 'hi-IN';
      utterance.rate = 0.95; // slightly slower for rural farmer clarity

      utterance.onstart = () => setIsPlayingAudio(true);
      utterance.onend = () => setIsPlayingAudio(false);
      utterance.onerror = () => setIsPlayingAudio(false);

      window.speechSynthesis.speak(utterance);
    }
  };

  const handleFarmerQuery = async (queryText: string) => {
    if (!queryText.trim() || isProcessing) return;

    const farmerMsg: ChatMessage = {
      id: 'msg-' + Date.now(),
      sender: 'farmer',
      text: queryText,
      language,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, farmerMsg]);
    setInputQuery('');
    setIsProcessing(true);

    try {
      const response = await sendChatMessage(queryText, language);
      const assistantMsg: ChatMessage = {
        id: 'msg-' + (Date.now() + 1),
        sender: 'assistant',
        text: response.response_text,
        language: response.language,
        confidence: response.confidence_score,
        sources: response.sources,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMsg]);

      // Automatically read response aloud in farmer's regional language
      if (audioEnabled) {
        playSpeechAudio(response.response_text, response.language);
      }
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: 'msg-err-' + Date.now(),
        sender: 'assistant',
        text: language === 'hi'
          ? "माफ़ करें, सर्वर से संपर्क नहीं हो पाया। कृपया दोबारा प्रयास करें या किसान कॉल सेंटर 1800-180-1551 पर कॉल करें।"
          : language === 'kn'
          ? "ಕ್ಷಮಿಸಿ, ಸರ್ವರ್ ಸಂಪರ್ಕಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಪುನಃ ಪ್ರಯತ್ನಿಸಿ."
          : "Sorry, unable to connect to the agricultural advisory server. Please retry.",
        language,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClearHistory = () => {
    if (confirm(language === 'hi' ? 'क्या आप बातचीत मिटाना चाहते हैं?' : 'Clear conversation history?')) {
      setMessages([]);
      localStorage.removeItem('kisan_chat_history');
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setIsPlayingAudio(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col justify-between max-w-xl mx-auto px-4 py-4 sm:py-6">
      {/* Top App Header & Controls */}
      <header className="space-y-3">
        {/* Title bar */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="bg-emerald-600 p-2 rounded-xl text-white shadow-lg shadow-emerald-700/50">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-black text-white leading-tight tracking-tight">
                {t.appTitle}
              </h1>
              <p className="text-xs text-emerald-300/80 leading-none">
                {t.appSubtitle}
              </p>
            </div>
          </div>

          {/* Audio toggle & Admin Portal link */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setAudioEnabled(!audioEnabled);
                if (isPlayingAudio && typeof window !== 'undefined') {
                  window.speechSynthesis.cancel();
                  setIsPlayingAudio(false);
                }
              }}
              title={audioEnabled ? "Disable Voice Output" : "Enable Voice Output"}
              className={`p-2 rounded-xl border transition-colors ${
                audioEnabled
                  ? 'bg-emerald-900/40 border-emerald-500/30 text-emerald-300'
                  : 'bg-slate-800 border-slate-700 text-slate-400'
              }`}
            >
              {audioEnabled ? <Volume2 className="w-4 h-4 text-emerald-300" /> : <VolumeX className="w-4 h-4" />}
            </button>

            <Link
              href="/admin"
              title="Extension Worker Admin"
              className="p-2 rounded-xl bg-slate-900/60 border border-slate-700/60 text-slate-300 hover:text-white transition-colors flex items-center gap-1 text-xs"
            >
              <Shield className="w-4 h-4 text-emerald-400" />
            </Link>
          </div>
        </div>

        {/* Offline Banner */}
        {isOffline && (
          <div className="flex items-center gap-2 bg-amber-950/80 border border-amber-500/50 text-amber-200 px-3 py-2 rounded-xl text-xs font-medium">
            <WifiOff className="w-4 h-4 shrink-0 text-amber-400" />
            <span>{t.offlineNotice}</span>
          </div>
        )}

        {/* Regional Language Selector */}
        <LanguageSelector currentLanguage={language} onLanguageChange={setLanguage} />
      </header>

      {/* Main Body: Voice Centerpiece + Conversation */}
      <section className="flex-1 my-3 overflow-y-auto">
        {/* Weather & Mandi Summary */}
        <AdvisoryCards language={language} />

        {/* Voice-First Focal Point */}
        <VoiceMicButton
          language={language}
          onTranscriptionComplete={(text) => handleFarmerQuery(text)}
          isProcessing={isProcessing}
          isPlayingAudio={isPlayingAudio}
        />

        {/* Quick tap sample questions */}
        {messages.length === 0 && (
          <div className="my-4 bg-emerald-950/30 border border-emerald-500/20 rounded-2xl p-4">
            <p className="text-xs font-semibold text-emerald-300 uppercase tracking-wider mb-2.5">
              {t.sampleQuestionsTitle}
            </p>
            <div className="flex flex-col gap-2">
              {t.sampleQuestions.map((sq, i) => (
                <button
                  key={i}
                  onClick={() => handleFarmerQuery(sq)}
                  className="text-left text-xs sm:text-sm bg-emerald-900/30 hover:bg-emerald-800/50 text-emerald-100 p-2.5 rounded-xl border border-emerald-500/10 transition-all flex items-center justify-between"
                >
                  <span>🌾 {sq}</span>
                  <span className="text-emerald-400 font-bold ml-2">→</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Conversation Stream */}
        <ChatHistory
          messages={messages}
          onPlayAudio={(text, lang) => playSpeechAudio(text, lang)}
        />
      </section>

      {/* Bottom Footer: Fallback Text Input & Session Actions */}
      <footer className="space-y-2 pt-2 border-t border-emerald-950/80">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleFarmerQuery(inputQuery);
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={t.typePlaceholder}
            disabled={isProcessing}
            className="flex-1 bg-emerald-950/60 border border-emerald-500/30 text-white placeholder-emerald-200/40 px-4 py-3 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
          />

          <button
            type="submit"
            disabled={isProcessing || !inputQuery.trim()}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-900/40 disabled:text-emerald-500 text-white p-3 rounded-2xl shadow-lg transition-all"
          >
            <Send className="w-5 h-5" />
          </button>

          {messages.length > 0 && (
            <button
              type="button"
              onClick={handleClearHistory}
              title={t.clearHistory}
              className="p-3 bg-emerald-950/50 hover:bg-rose-950/60 text-emerald-300 hover:text-rose-400 border border-emerald-500/20 rounded-2xl transition-colors"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          )}
        </form>

        <div className="flex items-center justify-between text-[11px] text-emerald-400/60 px-1">
          <span>Kisan AI v1.0 • Sarvam Indic Voice & RAG</span>
          <span>Toll-Free Helpline: 1800-180-1551</span>
        </div>
      </footer>
    </main>
  );
}
