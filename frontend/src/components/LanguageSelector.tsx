'use client';

import React from 'react';
import { Language } from '../lib/i18n';

interface LanguageSelectorProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
}

const languages: { code: Language; label: string; sub: string }[] = [
  { code: 'hi', label: 'हिन्दी', sub: 'Hindi' },
  { code: 'kn', label: 'ಕನ್ನಡ', sub: 'Kannada' },
  { code: 'en', label: 'English', sub: 'English' },
];

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  currentLanguage,
  onLanguageChange,
}) => {
  return (
    <div className="flex items-center gap-2 bg-emerald-950/40 p-1.5 rounded-2xl border border-emerald-500/30 backdrop-blur-md">
      {languages.map((lang) => {
        const isActive = currentLanguage === lang.code;
        return (
          <button
            key={lang.code}
            onClick={() => onLanguageChange(lang.code)}
            className={`flex-1 py-2 px-3 rounded-xl transition-all duration-200 flex flex-col items-center justify-center ${
              isActive
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-700/50 scale-[1.02] font-bold'
                : 'text-emerald-100/80 hover:bg-emerald-900/40'
            }`}
          >
            <span className="text-base sm:text-lg leading-tight">{lang.label}</span>
            <span className="text-[11px] opacity-75">{lang.sub}</span>
          </button>
        );
      })}
    </div>
  );
};
