from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models import Question, Attempt
from app.schemas import AttemptSubmit, AttemptResult
from app.scoring import score_attempt
from app.scoring_writing import score_swt, score_essay

router = APIRouter(prefix="/api/attempts", tags=["attempts"])

WRITING_TYPES = {"swt", "essay"}


def _score_writing(question: Question, user_answer: Dict[str, Any]) -> Dict[str, Any]:
    response_text = user_answer.get("text", "")
    content = question.content or {}
    key_points = content.get("key_points", [])

    if question.q_type == "swt":
        result = score_swt(question.passage or "", key_points, response_text)
    elif question.q_type == "essay":
        result = score_essay(question.passage or "", key_points, response_text)
    else:
        raise ValueError(f"Unknown writing type: {question.q_type}")

    return {
        "score": float(result["total"]),
        "max_score": float(result["max_total"]),
        "accuracy": result["total"] / result["max_total"] if result["max_total"] else 0.0,
        "breakdown": result,
    }


@router.post("/submit", response_model=AttemptResult)
def submit_attempt(payload: AttemptSubmit, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.q_type in WRITING_TYPES:
        result = _score_writing(question, payload.user_answer)
        correct_answer_out = None
    else:
        result = score_attempt(question.q_type, question.correct_answer, payload.user_answer)
        correct_answer_out = question.correct_answer

    attempt = Attempt(
        question_id=question.id,
        user_id=payload.user_id,
        user_answer=payload.user_answer,
        score=result["score"],
        max_score=result["max_score"],
        accuracy=result["accuracy"],
        breakdown=result.get("breakdown", {}),
        time_taken_seconds=payload.time_taken_seconds,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return AttemptResult(
        attempt_id=attempt.id,
        question_id=question.id,
        score=result["score"],
        max_score=result["max_score"],
        accuracy=result["accuracy"],
        correct_answer=correct_answer_out,
        explanation=question.explanation,
        breakdown=result.get("breakdown", {}),
    )


@router.get("/history")
def get_history(user_id: str = "guest", limit: int = 50, db: Session = Depends(get_db)):
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "attempt_id": a.id,
            "question_id": a.question_id,
            "score": a.score,
            "max_score": a.max_score,
            "accuracy": a.accuracy,
            "time_taken_seconds": a.time_taken_seconds,
            "created_at": a.created_at,
        }
        for a in attempts
    ]


@router.get("/stats")
def get_stats(user_id: str = "guest", db: Session = Depends(get_db)):
    attempts = db.query(Attempt).filter(Attempt.user_id == user_id).all()
    if not attempts:
        return {"total_attempts": 0, "average_accuracy": 0, "by_type": {}}

    by_type: Dict[str, Dict[str, Any]] = {}
    for a in attempts:
        q = db.query(Question).filter(Question.id == a.question_id).first()
        if not q:
            continue
        t = q.q_type
        by_type.setdefault(t, {"count": 0, "total_accuracy": 0.0})
        by_type[t]["count"] += 1
        by_type[t]["total_accuracy"] += a.accuracy

    for t, v in by_type.items():
        v["average_accuracy"] = round(v["total_accuracy"] / v["count"], 3)
        del v["total_accuracy"]

    avg_accuracy = sum(a.accuracy for a in attempts) / len(attempts)

    return {
        "total_attempts": len(attempts),
        "average_accuracy": round(avg_accuracy, 3),
        "by_type": by_type,
    }
