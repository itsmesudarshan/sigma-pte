"""Combined Reading module seed data — 20 questions per type, 100 total."""

from app.data.seed_reading_mcq_single import MCQ_SINGLE
from app.data.seed_reading_mcq_multi import MCQ_MULTI
from app.data.seed_reading_fill_blanks import FILL_BLANKS
from app.data.seed_reading_rw_fill_blanks import RW_FILL_BLANKS
from app.data.seed_reading_reorder import REORDER

SEED_QUESTIONS = MCQ_SINGLE + MCQ_MULTI + FILL_BLANKS + RW_FILL_BLANKS + REORDER
