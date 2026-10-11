'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, Sparkles } from 'lucide-react';
import { Language, translations } from '../lib/i18n';

interface VoiceMicButtonProps {
  language: Language;
  onTranscriptionComplete: (text: string) => void;
  isProcessing: boolean;
  isPlayingAudio: boolean;
}

export const VoiceMicButton: React.FC<VoiceMicButtonProps> = ({
  language,
  onTranscriptionComplete,
  isProcessing,
  isPlayingAudio,
}) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  const t = translations[language];

  useEffect(() => {
    // Setup Web Speech Recognition if supported in browser
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        const langMap: Record<Language, string> = {
          hi: 'hi-IN',
          kn: 'kn-IN',
          en: 'en-IN',
        };
        recognition.lang = langMap[language];

        recognition.onstart = () => setIsListening(true);
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          if (transcript) {
            onTranscriptionComplete(transcript);
          }
          setIsListening(false);
        };
        recognition.onerror = (e: any) => {
          console.warn('Speech recognition error:', e);
          setIsListening(false);
        };
        recognition.onend = () => setIsListening(false);

        recognitionRef.current = recognition;
      }
    }
  }, [language, onTranscriptionComplete]);

  const toggleMic = () => {
    if (isProcessing) return;

    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
    } else {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
          setIsListening(true);
        } catch (e) {
          console.error(e);
        }
      } else {
        // Fallback demo question for devices without microphone permissions
        const demoQuestions: Record<Language, string> = {
          hi: 'गेहूं में पीला रतुआ का क्या उपचार है?',
          kn: 'ಗೋಧಿಯಲ್ಲಿ ಹಳದಿ ತುಕ್ಕು ರೋಗಕ್ಕೆ ಪರಿಹಾರ ತಿಳಿಸಿ?',
          en: 'What is the treatment for yellow rust in wheat?',
        };
        onTranscriptionComplete(demoQuestions[language]);
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center my-4">
      {/* Visual glowing ripple rings when listening or speaking */}
      <div className="relative flex items-center justify-center">
        {isListening && (
          <>
            <span className="absolute w-36 h-36 rounded-full bg-emerald-500/20 animate-ping"></span>
            <span className="absolute w-44 h-44 rounded-full bg-emerald-500/10 animate-pulse"></span>
          </>
        )}
        {isPlayingAudio && (
          <span className="absolute w-36 h-36 rounded-full bg-amber-500/30 animate-pulse"></span>
        )}

        <button
          onClick={toggleMic}
          disabled={isProcessing}
          aria-label={isListening ? t.tapToStop : t.tapToSpeak}
          className={`relative z-10 w-28 h-28 sm:w-32 sm:h-32 rounded-full flex flex-col items-center justify-center shadow-2xl transition-all duration-300 transform active:scale-95 ${
            isListening
              ? 'bg-rose-600 text-white shadow-rose-600/60 scale-105 animate-pulse'
              : isPlayingAudio
              ? 'bg-amber-500 text-slate-900 shadow-amber-500/50 scale-105'
              : isProcessing
              ? 'bg-emerald-800 text-emerald-200 cursor-wait'
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-900/60 hover:scale-105'
          }`}
        >
          {isListening ? (
            <>
              <MicOff className="w-12 h-12 mb-1" />
              <span className="text-xs font-semibold uppercase tracking-wider">{t.tapToStop}</span>
            </>
          ) : isPlayingAudio ? (
            <>
              <Volume2 className="w-12 h-12 mb-1 animate-bounce" />
              <span className="text-xs font-semibold uppercase tracking-wider">Speaking</span>
            </>
          ) : isProcessing ? (
            <>
              <Sparkles className="w-12 h-12 mb-1 animate-spin" />
              <span className="text-xs font-semibold uppercase tracking-wider">Thinking</span>
            </>
          ) : (
            <>
              <Mic className="w-12 h-12 mb-1" />
              <span className="text-xs font-bold uppercase tracking-wider">TAP & SPEAK</span>
            </>
          )}
        </button>
      </div>

      {/* Dynamic tactile status label */}
      <div className="mt-4 text-center">
        <p className="text-emerald-100 font-medium text-base sm:text-lg">
          {isListening ? (
            <span className="text-rose-300 animate-pulse font-bold">{t.listening}</span>
          ) : isPlayingAudio ? (
            <span className="text-amber-300 font-bold">{t.audioPlaying}</span>
          ) : isProcessing ? (
            <span className="text-emerald-300 font-bold">{t.thinking}</span>
          ) : (
            <span>{t.tapToSpeak}</span>
          )}
        </p>
        <p className="text-xs sm:text-sm text-emerald-200/60 mt-0.5">{t.speakPrompt}</p>
      </div>
    </div>
  );
};
