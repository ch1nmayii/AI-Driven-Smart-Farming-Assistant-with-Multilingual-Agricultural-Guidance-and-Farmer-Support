'use client';

import React from 'react';
import { Volume2, CheckCircle2, AlertCircle, ThumbsUp, ThumbsDown, BookOpen } from 'lucide-react';
import { ChatMessage } from '../lib/api';

interface ChatHistoryProps {
  messages: ChatMessage[];
  onPlayAudio: (text: string, language: string) => void;
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, onPlayAudio }) => {
  if (messages.length === 0) return null;

  return (
    <div className="space-y-4 my-4">
      {messages.map((msg) => {
        const isFarmer = msg.sender === 'farmer';
        return (
          <div
            key={msg.id}
            className={`flex flex-col ${isFarmer ? 'items-end' : 'items-start'} transition-all`}
          >
            <div
              className={`max-w-[90%] sm:max-w-[80%] rounded-2xl p-4 shadow-md ${
                isFarmer
                  ? 'bg-emerald-600 text-white rounded-br-none'
                  : 'bg-emerald-950/80 border border-emerald-500/30 text-emerald-50 rounded-bl-none backdrop-blur-sm'
              }`}
            >
              {/* Speaker Header */}
              <div className="flex items-center justify-between gap-4 mb-1.5 text-xs">
                <span className={`font-semibold ${isFarmer ? 'text-emerald-100' : 'text-emerald-400'}`}>
                  {isFarmer ? '👨‍🌾 You (Farmer)' : '🤖 Kisan Assistant (AI Expert)'}
                </span>
                <span className="text-[10px] opacity-60">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>

              {/* Message Content */}
              <p className="text-sm sm:text-base leading-relaxed whitespace-pre-line font-normal">
                {msg.text}
              </p>

              {/* Assistant Footer: Audio trigger, confidence & sources */}
              {!isFarmer && (
                <div className="mt-3 pt-2.5 border-t border-emerald-500/20 flex flex-wrap items-center justify-between gap-2 text-xs">
                  {/* Spoken audio replay button */}
                  <button
                    onClick={() => onPlayAudio(msg.text, msg.language)}
                    className="flex items-center gap-1.5 bg-emerald-800/60 hover:bg-emerald-700/80 text-emerald-100 px-2.5 py-1 rounded-lg border border-emerald-400/30 transition-colors"
                  >
                    <Volume2 className="w-3.5 h-3.5 text-amber-300" />
                    <span>सुनें (Listen)</span>
                  </button>

                  {/* Sources tag */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="flex items-center gap-1 text-[11px] text-emerald-300/80">
                      <BookOpen className="w-3 h-3" />
                      <span>{msg.sources[0]}</span>
                    </div>
                  )}

                  {/* Thumbs up / down feedback */}
                  <div className="flex items-center gap-2">
                    <button
                      className="p-1 hover:text-emerald-300 transition-colors"
                      title="Helpful advice"
                      onClick={() => alert('धन्यवाद! आपकी प्रतिक्रिया दर्ज कर ली गई है। (Thank you for your feedback!)')}
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                    </button>
                    <button
                      className="p-1 hover:text-rose-300 transition-colors"
                      title="Not accurate"
                      onClick={() => alert('यह प्रश्न कृषि विशेषज्ञ के पुनरीक्षण के लिए दर्ज कर लिया गया है। (Flagged for review.)')}
                    >
                      <ThumbsDown className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
