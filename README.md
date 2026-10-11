# 🌾 Kisan AI: Smart Farming Assistant with Multilingual Indic Voice & RAG Support

A mobile-first, voice-first Progressive Web App (PWA) and FastAPI platform designed for Indian farmers. Farmers can speak queries in Hindi, Kannada, or English and hear verified agricultural guidance read back aloud — requiring no typing or English literacy.

---

## 🚀 Quick Start (Running Frontend & Backend)

### 1. Backend (FastAPI on Port 6000)
```bash
cd backend
# Create and activate virtual environment (optional but recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server on port 6000
python -m uvicorn app.main:app --host 0.0.0.0 --port 6000 --reload
```
- **Backend API**: `http://localhost:6000`
- **Swagger Documentation**: `http://localhost:6000/docs`
- **Health Check**: `http://localhost:6000/health`

---

### 2. Frontend (Next.js Farmer PWA on Port 3000)
```bash
cd frontend
# Install dependencies
npm install

# Start Next.js PWA development server on port 3000
npm run dev
```
- **Farmer Voice PWA**: `http://localhost:3000`
- **Extension Worker Admin Panel**: `http://localhost:3000/admin`

> **Note on Port 6000 Proxy**: Next.js automatically proxies requests from `http://localhost:3000/api/backend/*` to `http://localhost:6000/api/*`, ensuring web browsers don't block port 6000 under restricted port policies.

---

## 🌿 System Architecture & Flow Chart

```mermaid
flowchart TD
    subgraph Farmer_PWA["📱 Farmer Mobile PWA (Port 3000)"]
        UI["Voice-First Interface\n(Hindi / Kannada / English)"]
        Mic["Tactile Mic Button\n(Speech Capture)"]
        Speaker["Speech Readback\n(TTS Audio Player)"]
        Cache["Service Worker Cache\n(Offline Fallback)"]
    end

    subgraph Backend_Gateway["⚡ FastAPI Server (Port 6000)"]
        API_Chat["/api/chat"]
        API_Audio["/api/audio (STT / TTS)"]
        API_Advisory["/api/advisory (Mandi & Weather)"]
        API_Admin["/api/admin (Human Review)"]
    end

    subgraph Indic_AI_Pipeline["🧠 Multilingual NLP & Speech Engine"]
        Sarvam["Sarvam AI Indic STT / TTS\n(Hindi, Kannada, Indic models)"]
        LangDetect["Language & Intent Classifier\n(Pests, Soil, Schemes, Market)"]
    end

    subgraph RAG_Layer["📚 Agricultural Knowledge Base & RAG"]
        KB_ICAR["ICAR Advisory Knowledge Base"]
        KB_KCC["Kisan Call Centre FAQs"]
        KB_Schemes["Government Schemes (PM-KISAN, PMFBY)"]
        Scorer["Confidence Scoring (<0.70 flags for review)"]
    end

    subgraph Admin_Portal["🛡️ Extension Worker Admin"]
        ReviewQueue["Human Review Queue"]
        Analytics["Regional Usage Metrics"]
    end

    Mic -->|Audio Stream| API_Audio
    API_Audio --> Sarvam
    Sarvam -->|Transcribed Text| LangDetect
    LangDetect --> API_Chat
    API_Chat --> RAG_Layer
    RAG_Layer --> Scorer
    Scorer -->|High Confidence Answer| Speaker
    Scorer -->|Low Confidence (<0.70)| ReviewQueue
    API_Advisory -->|Real-time Mandi & Weather| UI
```

---

## 📤 Pushing to Git Repository

1. **Initialize Git (if not done)**:
   ```bash
   git init
   git add .
   git commit -m "feat: AI-driven smart farming assistant with multilingual Indic voice and RAG support"
   ```

2. **Add Remote & Push to GitHub / GitLab**:
   ```bash
   git branch -M main
   git remote add origin <YOUR_GITHUB_OR_GITLAB_REPO_URL>
   git push -u origin main
   ```

---

## 🛠️ Key Technologies
- **Frontend**: Next.js 14, React 18, Tailwind CSS, Lucide Icons, Service Worker (PWA)
- **Backend**: FastAPI, Uvicorn, Pydantic, HTTPX, Python 3.10+
- **Indic AI**: Sarvam AI Indic Speech-to-Text & Text-to-Speech (Hindi, Kannada), Web Speech API
- **RAG & Knowledge Base**: ICAR guidelines, Kisan Call Center records, Agmarknet wholesale data
