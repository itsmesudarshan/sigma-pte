from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuestionOut(BaseModel):
    id: int
    module: str
    q_type: str
    difficulty: str
    tags: List[str]
    title: str
    passage: Optional[str] = None
    content: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    module: str
    q_type: str
    difficulty: str
    tags: List[str] = []
    title: str
    passage: Optional[str] = None
    content: Dict[str, Any]
    correct_answer: Optional[Dict[str, Any]] = None
    explanation: str = ""


class AttemptSubmit(BaseModel):
    question_id: int
    user_id: str = "guest"
    user_answer: Dict[str, Any]     # for writing types: {"text": "..."}
    time_taken_seconds: int = 0


class AttemptResult(BaseModel):
    attempt_id: int
    question_id: int
    score: float
    max_score: float
    accuracy: float
    correct_answer: Optional[Dict[str, Any]] = None
    explanation: str
    breakdown: Dict[str, Any] = {}


class FavoriteToggle(BaseModel):
    user_id: str = "guest"
    question_id: int


class SignupRequest(BaseModel):
    email: str
    password: str


class VerifyOtpRequest(BaseModel):
    email: str
    otp: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    token: str
    user: UserOut
