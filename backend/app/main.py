from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.routers import questions, attempts
from app.models import Question
from app.data.seed_questions import SEED_QUESTIONS
from app.data.seed_writing import SEED_WRITING
from app.data.seed_speaking import SEED_SPEAKING
from app.data.seed_listening import SEED_LISTENING

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prepwise PTE Prep Platform API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(attempts.router)


@app.on_event("startup")
def seed_database():
    db = SessionLocal()
    try:
        if db.query(Question).count() == 0:
            for q in SEED_QUESTIONS + SEED_WRITING + SEED_SPEAKING + SEED_LISTENING:
                db.add(Question(**q))
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok", "service": "Prepwise PTE Prep Platform API"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}
