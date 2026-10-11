import { Language } from './i18n';

const API_BASE = '/api/backend';

export interface ChatMessage {
  id: string;
  sender: 'farmer' | 'assistant';
  text: string;
  language: string;
  confidence?: number;
  sources?: string[];
  audioBase64?: string;
  timestamp: string;
}

export interface MandiItem {
  crop: string;
  market: string;
  state: string;
  min_price: number;
  max_price: number;
  modal_price: number;
  unit: string;
  updated_at: string;
}

export interface WeatherData {
  location: string;
  temperature: number;
  condition: string;
  humidity: number;
  rainfall_probability: number;
  advisory: string;
}

export async function sendChatMessage(message: string, language: Language, location?: string): Promise<{
  response_text: string;
  language: string;
  intent: string;
  confidence_score: number;
  flagged_for_review: boolean;
  sources: string[];
  audio_base64?: string;
}> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      language,
      location: location || 'Uttar Pradesh',
      session_id: 'farmer-session-' + (typeof window !== 'undefined' ? localStorage.getItem('farmer_sid') || '1' : '1')
    })
  });
  if (!res.ok) {
    throw new Error('Failed to send message to agricultural backend');
  }
  return res.json();
}

export async function fetchMandiPrices(): Promise<MandiItem[]> {
  try {
    const res = await fetch(`${API_BASE}/advisory/mandi-prices`);
    if (res.ok) return await res.json();
  } catch (e) {
    console.warn('Using fallback mandi prices:', e);
  }
  return [
    { crop: "Wheat (गेहूं / ಗೋಧಿ)", market: "Agra APMC", state: "UP", min_price: 2200, max_price: 2350, modal_price: 2275, unit: "₹/Quintal", updated_at: "Today" },
    { crop: "Paddy (धान / ಭತ್ತ)", market: "Karnal APMC", state: "Haryana", min_price: 2150, max_price: 2280, modal_price: 2183, unit: "₹/Quintal", updated_at: "Today" }
  ];
}

export async function fetchWeather(): Promise<WeatherData> {
  try {
    const res = await fetch(`${API_BASE}/advisory/weather`);
    if (res.ok) return await res.json();
  } catch (e) {
    console.warn('Using fallback weather:', e);
  }
  return {
    location: "Agricultural Belt",
    temperature: 28.5,
    condition: "Partly Cloudy",
    humidity: 65,
    rainfall_probability: 20,
    advisory: "Favorable for weeding and intercultural operations."
  };
}

export async function fetchAdminAnalytics() {
  const res = await fetch(`${API_BASE}/admin/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function fetchFlaggedQueries() {
  const res = await fetch(`${API_BASE}/admin/flagged-queries`);
  if (!res.ok) throw new Error('Failed to fetch flagged queries');
  return res.json();
}

export async function resolveQuery(id: string) {
  const res = await fetch(`${API_BASE}/admin/resolve-query/${id}`, { method: 'POST' });
  return res.json();
}
