from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

from app.database import get_db
from app.models import Question, Favorite, Attempt
from app.schemas import QuestionOut, QuestionCreate, FavoriteToggle

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("", response_model=List[QuestionOut])
def list_questions(
    module: Optional[str] = None,
    q_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    favorites_only: bool = False,
    user_id: str = "guest",
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Question)

    if module:
        query = query.filter(Question.module == module)
    if q_type:
        query = query.filter(Question.q_type == q_type)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Question.title.ilike(like), Question.passage.ilike(like)))

    if favorites_only:
        fav_ids = [f.question_id for f in db.query(Favorite).filter(Favorite.user_id == user_id).all()]
        query = query.filter(Question.id.in_(fav_ids))

    results = query.offset(offset).limit(limit).all()

    if tag:
        results = [q for q in results if tag in (q.tags or [])]

    return results


@router.get("/recent", response_model=List[QuestionOut])
def recently_attempted(user_id: str = "guest", limit: int = 10, db: Session = Depends(get_db)):
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(limit * 3)
        .all()
    )
    seen = []
    for a in attempts:
        if a.question_id not in seen:
            seen.append(a.question_id)
        if len(seen) >= limit:
            break
    questions = db.query(Question).filter(Question.id.in_(seen)).all()
    order_map = {qid: i for i, qid in enumerate(seen)}
    questions.sort(key=lambda q: order_map.get(q.id, 999))
    return questions


@router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.post("", response_model=QuestionOut)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    q = Question(**payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.post("/favorites/toggle")
def toggle_favorite(payload: FavoriteToggle, db: Session = Depends(get_db)):
    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == payload.user_id, Favorite.question_id == payload.question_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return {"favorited": False}
    else:
        fav = Favorite(user_id=payload.user_id, question_id=payload.question_id)
        db.add(fav)
        db.commit()
        return {"favorited": True}


@router.get("/meta/tags")
def list_tags(db: Session = Depends(get_db)):
    questions = db.query(Question.tags).all()
    tag_set = set()
    for (tags,) in questions:
        tag_set.update(tags or [])
    return sorted(tag_set)
