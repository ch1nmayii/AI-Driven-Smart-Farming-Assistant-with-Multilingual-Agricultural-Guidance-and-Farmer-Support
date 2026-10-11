'use client';

import React, { useEffect, useState } from 'react';
import { CloudSun, TrendingUp, IndianRupee, MapPin } from 'lucide-react';
import { Language, translations } from '../lib/i18n';
import { fetchMandiPrices, fetchWeather, MandiItem, WeatherData } from '../lib/api';

interface AdvisoryCardsProps {
  language: Language;
}

export const AdvisoryCards: React.FC<AdvisoryCardsProps> = ({ language }) => {
  const [mandiPrices, setMandiPrices] = useState<MandiItem[]>([]);
  const [weather, setWeather] = useState<WeatherData | null>(null);

  const t = translations[language];

  useEffect(() => {
    fetchMandiPrices().then(setMandiPrices);
    fetchWeather().then(setWeather);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
      {/* Weather Card */}
      {weather && (
        <div className="bg-emerald-950/50 border border-emerald-500/20 rounded-2xl p-4 backdrop-blur-sm text-emerald-50">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <CloudSun className="w-5 h-5 text-amber-400" />
              <h3 className="font-semibold text-sm sm:text-base text-emerald-200">{t.weatherTitle}</h3>
            </div>
            <span className="text-xs bg-emerald-800/60 px-2 py-0.5 rounded-full flex items-center gap-1 text-emerald-200">
              <MapPin className="w-3 h-3" /> {weather.location}
            </span>
          </div>

          <div className="flex items-baseline justify-between mt-1">
            <span className="text-3xl font-extrabold text-white">{weather.temperature}°C</span>
            <span className="text-sm text-emerald-300 font-medium">{weather.condition}</span>
          </div>

          <div className="mt-2 text-xs text-emerald-100/80 bg-emerald-900/30 p-2 rounded-xl border border-emerald-500/20">
            🌱 <strong className="text-emerald-200">Advisory:</strong> {weather.advisory}
          </div>
        </div>
      )}

      {/* Mandi Prices Card */}
      <div className="bg-emerald-950/50 border border-emerald-500/20 rounded-2xl p-4 backdrop-blur-sm text-emerald-50">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <h3 className="font-semibold text-sm sm:text-base text-emerald-200">{t.mandiTitle}</h3>
          </div>
          <span className="text-xs text-emerald-400 font-mono">AGMARKNET</span>
        </div>

        <div className="space-y-1.5 max-h-32 overflow-y-auto pr-1">
          {mandiPrices.slice(0, 3).map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between bg-emerald-900/30 px-3 py-1.5 rounded-xl border border-emerald-500/10 text-xs sm:text-sm"
            >
              <div>
                <span className="font-medium text-emerald-100">{item.crop}</span>
                <span className="text-[11px] text-emerald-400 block opacity-80">{item.market}</span>
              </div>
              <div className="text-right">
                <span className="font-bold text-amber-300 flex items-center justify-end">
                  <IndianRupee className="w-3.5 h-3.5 inline" /> {item.modal_price}
                </span>
                <span className="text-[10px] text-emerald-300/70">{item.unit}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
