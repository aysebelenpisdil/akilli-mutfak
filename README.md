# Akıllı Mutfak Şefi

An AI-powered Turkish recipe recommendation web app. Enter what's in your fridge and get personalized recipe suggestions with explanations — built for Turkish cuisine and the Turkish language.

**Live at [akillimutfak.me](https://akillimutfak.me) · Built by Belen Pişdil**

---

## Features

- **AI Recipe Recommendations** — Hybrid retrieval (FAISS vector search + TF-IDF) fused with Reciprocal Rank Fusion, re-ranked by a multilingual cross-encoder, then explained by Gemini 2.5 Flash
- **532 Turkish Recipes** — Curated dataset covering a wide range of Turkish home cooking
- **Personalization** — Like, skip, cook, and save feedback adjusts future ranking scores per user
- **Dietary Filters** — Vegan, vegetarian, gluten-free, dairy-free, nut-free
- **Ingredient Substitutions** — LLM-powered suggestions when you're missing something
- **Shopping List** — Auto-generated from missing recipe ingredients
- **Passwordless Auth** — Magic link login via email (Supabase Auth)
- **Android App** — Capacitor wrapper for native Android distribution

---

## Architecture

```
Browser / Android App (React 19 + Capacitor)
          │
          │  HTTPS
          ▼
    FastAPI Backend  ─────────────────────────────────────┐
          │                                               │
          ▼                                               ▼
  RAG Pipeline                                  Supabase PostgreSQL
  ┌──────────────────────────────────┐           (users, feedback,
  │  1. Hybrid Retrieval             │            preferences,
  │     ├─ FAISS (dense vectors)     │            sessions)
  │     ├─ TF-IDF (sparse BM-style)  │
  │     └─ RRF Fusion                │
  │                                  │
  │  2. Cross-Encoder Reranker       │
  │     (mmarco-mMiniLMv2-L12)       │
  │                                  │
  │  3. Personalization              │
  │     (history score adjustments)  │
  │                                  │
  │  4. LLM Generator                │
  │     (Gemini 2.5 Flash)           │
  └──────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite 6, Tailwind CSS v4 |
| Mobile | Capacitor 8 (Android) |
| Backend | FastAPI, Python 3.10+, Uvicorn |
| Vector Search | FAISS (IndexFlatL2), sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2` |
| Sparse Retrieval | TF-IDF + Reciprocal Rank Fusion |
| Reranker | `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (multilingual) |
| LLM | Gemini 2.5 Flash (fallback: Gemini 2.0 Flash) |
| Database | Supabase PostgreSQL (asyncpg + SQLAlchemy async) |
| Auth | Supabase Auth — magic link (passwordless) |
| Rate Limiting | SlowAPI |
| Deployment | DigitalOcean, Docker Compose |

---

## Prerequisites

- **Node.js** 18+
- **Python** 3.10+
- **Gemini API key** — [Get one from Google AI Studio](https://aistudio.google.com/)
- **Supabase project** — for PostgreSQL database and auth

---

## Installation

### 1. Install dependencies

```bash
# Frontend
npm install

# Backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

**Backend** (`backend/.env`):

```env
# Required
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SESSION_SECRET=a-long-random-secret-string

# Optional — magic link email delivery
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
FRONTEND_URL=http://localhost:3000
```

> Use a Gmail **App Password**, not your regular password.

**Frontend** (`.env.local`, optional):

```env
VITE_API_URL=http://localhost:3001/api
```

### 3. Build the FAISS index (first-time setup only)

```bash
cd backend
python scripts/build_faiss_index.py
```

This embeds all 532 recipes and saves `data/recipe_index.faiss` and supporting TF-IDF artifacts.

---

## Running Locally

**Terminal 1 — Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 3001 --reload-exclude 'venv/*'
```

Or via npm: `npm run dev:backend`

**Terminal 2 — Frontend:**

```bash
npm run dev
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

## Docker (Production)

```bash
docker compose up --build
```

- Frontend served on port `3000`
- Backend API on port `3001`

---

## Android Build

```bash
npm run cap:sync    # build frontend and sync to Android project
npm run cap:open    # open in Android Studio
```

---

## Tests

```bash
# Frontend
npm run test

# Backend
npm run test:backend
```

---

## Project Structure

```
.
├── src/                   # React frontend
│   ├── components/
│   ├── pages/
│   ├── store/
│   ├── hooks/
│   └── lib/
├── backend/
│   ├── app/
│   │   ├── routes/        # FastAPI routers (recipes, auth, feedback, fridge…)
│   │   ├── services/      # RAG pipeline, FAISS, reranker, LLM, DB, auth…
│   │   ├── models/
│   │   └── middleware/
│   ├── data/              # recipes.json, FAISS index, TF-IDF artifacts
│   ├── scripts/           # build_faiss_index.py and other utilities
│   └── tests/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── capacitor.config.ts
```

---

## API Docs

Interactive docs available while the backend is running: [http://localhost:3001/docs](http://localhost:3001/docs)

---

## Production Checklist

- [ ] Set a strong, random `SESSION_SECRET` (never use the default)
- [ ] Set `GEMINI_API_KEY` — without it, recipe explanations and substitutions are disabled
- [ ] Set `DATABASE_URL` pointing to your Supabase PostgreSQL instance
- [ ] Set `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- [ ] Set `FRONTEND_URL` to your live domain (e.g. `https://akillimutfak.me`) for CORS
- [ ] Configure SMTP if you want magic link emails
- [ ] Run `NODE_ENV=production` in the backend environment

---

## License

MIT
