from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String, index=True)          # reading, writing, speaking, listening
    q_type = Column(String, index=True)           # rw_fill_blanks, fill_blanks, reorder, mcq_single, mcq_multi, swt, essay
    difficulty = Column(String, index=True)        # easy, medium, hard
    tags = Column(JSON, default=list)
    title = Column(String)
    passage = Column(Text)                         # main text/passage/prompt
    content = Column(JSON)                          # type-specific structured content (options, blanks, paragraphs, key_points...)
    correct_answer = Column(JSON, nullable=True)     # type-specific correct answer key (null for open-ended writing types)
    explanation = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(String, index=True, default="guest")
    user_answer = Column(JSON)
    score = Column(Float)
    max_score = Column(Float)
    accuracy = Column(Float)
    breakdown = Column(JSON, default=dict)          # full trait breakdown, used by Writing module
    time_taken_seconds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="guest")
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
