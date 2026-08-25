"""
Scoring engine for PTE Academic Listening question types.

Multiple Choice (Single/Multiple), Fill in the Blanks, Highlight Correct
Summary, and Select Missing Word reuse the exact same official partial-credit
rules already implemented for Reading (they're graded identically per
Pearson's rubric — only the input modality differs, audio vs text).

Write From Dictation gets its own scorer here: official rule is +1 point per
correctly transcribed word, in the correct position, case-insensitive.
"""

from typing import Dict, Any
from app.scoring import score_mcq_single, score_mcq_multi, score_fill_blanks

score_highlight_correct_summary = score_mcq_single
score_select_missing_word = score_mcq_single


def score_write_from_dictation(correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    correct_text = correct_answer.get("text", "")
    given_text = user_answer.get("text", "")

    correct_words = correct_text.strip().split()
    given_words = given_text.strip().split()

    max_score = len(correct_words)
    correct_count = 0
    per_word = []

    for i, correct_word in enumerate(correct_words):
        given_word = given_words[i] if i < len(given_words) else ""
        is_correct = given_word.strip(".,!?;:'\"").lower() == correct_word.strip(".,!?;:'\"").lower()
        per_word.append({"position": i, "given": given_word, "correct": correct_word, "is_correct": is_correct})
        if is_correct:
            correct_count += 1

    return {
        "score": float(correct_count),
        "max_score": float(max_score),
        "accuracy": correct_count / max_score if max_score else 0.0,
        "breakdown": {"per_word": per_word, "correct_text": correct_text},
    }


LISTENING_SCORERS = {
    "l_mcq_single": score_mcq_single,
    "l_mcq_multi": score_mcq_multi,
    "l_fill_blanks": score_fill_blanks,
    "highlight_summary": score_highlight_correct_summary,
    "select_missing_word": score_select_missing_word,
    "write_from_dictation": score_write_from_dictation,
}


def score_listening_attempt(q_type: str, correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    scorer = LISTENING_SCORERS.get(q_type)
    if not scorer:
        raise ValueError(f"No listening scorer registered for question type: {q_type}")
    return scorer(correct_answer, user_answer)
