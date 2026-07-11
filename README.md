# Prepwise — PTE Academic Prep Platform

Original, from-scratch PTE Academic preparation platform. This first milestone
covers the **Reading module** (all 5 official question types) with a working
Question Bank, rule-based scoring engine, and a Dashboard — built on a stack
that runs entirely on free tiers, same as your other projects.

## Stack
- **Backend:** FastAPI + SQLite (SQLAlchemy) — free, self-hosted
- **Frontend:** React + Vite — free static hosting
- **Scoring:** Deterministic, rule-based, following the publicly documented
  official Pearson PTE Academic scoring criteria (no paid AI API needed for
  Reading, since answers are objectively gradable)

## What's included
- 5 Reading question types: Reading & Writing Fill in the Blanks, Fill in
  the Blanks, Re-order Paragraphs, MCQ (Single), MCQ (Multiple)
- 8 original seed questions (2 per type on average) across easy/medium/hard
- Question Bank: search, filter by type/difficulty, favorites
- Rule-based scoring matching official partial-credit rules:
  - MCQ Multi: +1 per correct pick, −1 per incorrect pick, floored at 0
  - Re-order: scored on correct *adjacent pairs*, not exact position
  - Fill blanks: 1 point per correctly filled blank
- Dashboard: overall accuracy, accuracy by question type (chart), recent
  activity, total attempts
- Attempt history stored per user (defaults to a "guest" user — add real
  auth later when you're ready)

## Local development

### Backend
```bash
cd backend
pip install -r requirements.txt --break-system-packages
python3 -m uvicorn app.main:app --reload --port 8000
```
API runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.
The SQLite database (`pte_platform.db`) is created and seeded automatically on first run.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at `http://localhost:5173`. It reads the backend URL from `.env` (`VITE_API_URL`).

## Free deployment (same pattern as your other projects)

**Backend → Render (free tier)**
1. Push `backend/` to a GitHub repo (or a subfolder of one).
2. New Web Service on Render, connect the repo, root directory `backend`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Render's free SQLite storage is ephemeral (resets on redeploy) — fine for
   now; swap to Render's free Postgres add-on later if you want data to persist
   across deploys.

**Frontend → Vercel or Cloudflare Pages (free tier)**
1. Push `frontend/` to GitHub.
2. Import the repo, set root directory to `frontend`.
3. Build command: `npm run build`, output directory: `dist`.
4. Set environment variable `VITE_API_URL` to your deployed Render backend URL.

## Project structure
```
backend/
  app/
    main.py           # FastAPI app, CORS, DB seeding
    database.py        # SQLAlchemy engine/session
    scoring.py          # Rule-based scoring engine (all 5 types)
    models/              # Question, Attempt, Favorite tables
    schemas/               # Pydantic request/response models
    routers/
      questions.py          # question bank: list/filter/search/favorites
      attempts.py             # submit answers, history, stats
    data/seed_questions.py     # original seed content
frontend/
  src/
    api/client.js              # backend API wrapper
    components/                 # Layout, Timer, ScoreGauge
    components/questionTypes/    # one component per Reading question type
    pages/                        # Dashboard, Reading, QuestionBank, Practice
```

## Next milestones (not built yet)
- Writing module (Summarize Text, Essay) — will need AI scoring since these
  are open-ended; can use free-tier Groq/Claude API credits like your
  AstroNepal project, kept optional/gated so it never requires payment
- Speaking Studio — browser-based Web Speech API for basic pronunciation/
  fluency feedback (free, no installs, runs entirely client-side)
- Listening module
- Real authentication (currently a single "guest" user)
- Mock tests, study planner, gamification, vocabulary trainer
