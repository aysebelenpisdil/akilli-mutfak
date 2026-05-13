# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Buzdolabı Şefi** (Smart Fridge Chef) — an AI-powered Turkish recipe recommendation web app. Users enter their fridge ingredients and receive recipe suggestions via a RAG pipeline (FAISS → Cross-encoder reranker → Gemini LLM). Optimized for Turkish cuisine and the Turkish language.

## Commands

### Frontend (React + Vite + TypeScript)
```bash
npm install          # Install dependencies
npm run dev          # Dev server at http://127.0.0.1:3000
npm run build        # Production build
npm run test         # Run Vitest tests once
npm run test:watch   # Run Vitest in watch mode
```

### Backend (FastAPI + Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build FAISS index (required on first setup or after recipe data changes)
python scripts/build_faiss_index.py

# Run backend (port 3001)
uvicorn app.main:app --reload --port 3001 --reload-exclude 'venv/*'
# Or from root:
npm run dev:backend

# Run backend tests
npm run test:backend
# Or directly:
cd backend && ./venv/bin/python -m pytest tests/ -v
```

### Environment Setup
- **Backend**: copy `backend/.env.example` → `backend/.env`, set `GEMINI_API_KEY` and `SESSION_SECRET`
- **Frontend**: optionally create `.env.local` with `VITE_API_URL=http://localhost:3001/api`
- **API docs**: available at `http://localhost:3001/docs` when backend is running

## Architecture

### Frontend
- **Entry**: `index.tsx` → `App.tsx` — uses `HashRouter` with routes for `/`, `/recipes`, `/recipe/:title`, `/preferences`, `/login`, `/profile`
- **State**: Two React Contexts in `store/`:
  - `AuthContext` — session management, magic-link login
  - `FridgeContext` — fridge ingredients + dietary preferences + excluded ingredients; syncs to localStorage for anonymous users, to backend API for logged-in users (with 500ms debounce)
- **Pages** (`pages/`): `FridgePage` (ingredient input), `RecipesPage` (RAG results), `RecipeDetailPage`, `PreferencesPage`, `LoginPage`, `ProfilePage`
- **Ingredient search** (`hooks/useIngredientSearch.ts`): client-side fuzzy search over `src/data/cleanedIngredients.json` using Levenshtein distance; scores matches as exact > starts-with > contains > fuzzy

### Backend RAG Pipeline
Three-stage pipeline in `backend/app/services/rag_pipeline.py`:
1. **Retriever** (`faiss_service.py`): FAISS vector similarity search over recipe embeddings; falls back to string matching if index not loaded
2. **Reranker** (`reranker_service.py`): Cross-encoder model for contextual re-ranking of top-50 FAISS results
3. **Generator** (`llm_service.py`): Gemini LLM generates recipe explanations and ingredient substitution suggestions

All three services are singletons that lazy-load on first use. The pipeline gracefully degrades if any component is unavailable.

### Backend Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI app, startup init, CORS
│   ├── config.py        # Settings from env vars
│   ├── database.py      # SQLite connection
│   ├── routes/          # auth.py, recipes.py, feedback.py, fridge.py
│   ├── services/        # RAG pipeline components + auth/email/db services
│   ├── models/          # Pydantic models
│   └── middleware/
├── data/                # Recipe JSON data
├── scripts/             # build_faiss_index.py
└── tests/
```

### API Routes (all prefixed `/api`)
- `auth` — magic-link email login, session management
- `recipes` — RAG recommendation endpoint, ingredient substitution
- `feedback` — like/skip/cook interactions, consumption logging, user features
- `fridge` — persist fridge ingredients per user

### Frontend Utilities (`utils/`)
- `recipeFilter.ts` — client-side filtering by dietary preferences, excluded ingredients, calorie range
- `dietaryRules.ts` — maps dietary flags (vegan, glutenFree, etc.) to forbidden ingredient lists
- `ingredientNormalizer.ts` — substring matching for ingredient exclusion
- `calorieEstimator.ts` — estimates calories from `src/data/calorieData.json`
- `api.ts` — all `fetch` calls to the backend

### Data
- `data/recipes.ts` — static recipe data used for client-side fallback
- `src/data/cleanedIngredients.json` — canonical ingredient list with frequency counts (used by fuzzy search)
- `src/data/calorieData.json` — calorie data per ingredient
- `constants/ingredientData.ts` — additional ingredient constants
