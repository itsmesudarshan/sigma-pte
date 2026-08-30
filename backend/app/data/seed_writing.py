"""Combined Writing module seed data — 20 questions per type, 40 total."""

from app.data.seed_writing_swt import SWT_QUESTIONS
from app.data.seed_writing_essay import ESSAY_QUESTIONS

SEED_WRITING = SWT_QUESTIONS + ESSAY_QUESTIONS
