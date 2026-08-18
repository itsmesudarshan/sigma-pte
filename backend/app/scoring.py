"""
Scoring engine for PTE Academic Reading question types.

Verified directly against Pearson's official "PTE Academic Test Taker Score
Guide" (Part 2: Reading, page 39-40):
  - Fill in the Blanks (Dropdown / Drag&Drop): +1 per correctly completed blank
  - Multiple Choice, Multiple Answers: +1 per correct response, -1 per
    incorrect response chosen, floor at 0
  - Re-order Paragraph: +1 per correctly ordered adjacent pair
  - Multiple Choice, Single Answer: correct/incorrect, 1 or 0
"""

from typing import Dict, Any


def score_mcq_single(correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    correct = correct_answer.get("option")
    given = user_answer.get("option")
    is_correct = correct == given
    score = 1.0 if is_correct else 0.0
    return {
        "score": score,
        "max_score": 1.0,
        "accuracy": score,
        "breakdown": {"selected": given, "correct": correct, "is_correct": is_correct},
    }


def score_mcq_multi(correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    correct_set = set(correct_answer.get("options", []))
    given_set = set(user_answer.get("options", []))

    correct_selected = correct_set & given_set
    incorrect_selected = given_set - correct_set

    raw_score = len(correct_selected) - len(incorrect_selected)
    max_score = len(correct_set)
    score = max(0, min(raw_score, max_score))

    return {
        "score": float(score),
        "max_score": float(max_score),
        "accuracy": score / max_score if max_score else 0.0,
        "breakdown": {
            "correct_selected": list(correct_selected),
            "incorrect_selected": list(incorrect_selected),
            "missed": list(correct_set - given_set),
        },
    }


def score_fill_blanks(correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    correct_blanks = correct_answer.get("blanks", {})
    given_blanks = user_answer.get("blanks", {})

    max_score = len(correct_blanks)
    per_blank = {}
    correct_count = 0

    for key, correct_val in correct_blanks.items():
        given_val = str(given_blanks.get(key, "")).strip().lower()
        is_correct = given_val == str(correct_val).strip().lower()
        per_blank[key] = {"given": given_blanks.get(key, ""), "correct": correct_val, "is_correct": is_correct}
        if is_correct:
            correct_count += 1

    return {
        "score": float(correct_count),
        "max_score": float(max_score),
        "accuracy": correct_count / max_score if max_score else 0.0,
        "breakdown": {"per_blank": per_blank},
    }


def score_reorder(correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    correct_order = correct_answer.get("order", [])
    given_order = user_answer.get("order", [])

    max_score = max(len(correct_order) - 1, 0)
    correct_pairs = []
    score = 0

    correct_pair_set = {
        (correct_order[i], correct_order[i + 1]) for i in range(len(correct_order) - 1)
    }

    for i in range(len(given_order) - 1):
        pair = (given_order[i], given_order[i + 1])
        if pair in correct_pair_set:
            score += 1
            correct_pairs.append(pair)

    return {
        "score": float(score),
        "max_score": float(max_score),
        "accuracy": score / max_score if max_score else 0.0,
        "breakdown": {"correct_order": correct_order, "given_order": given_order, "correct_adjacent_pairs": correct_pairs},
    }


SCORERS = {
    "mcq_single": score_mcq_single,
    "mcq_multi": score_mcq_multi,
    "fill_blanks": score_fill_blanks,
    "rw_fill_blanks": score_fill_blanks,
    "reorder": score_reorder,
}


def score_attempt(q_type: str, correct_answer: Dict[str, Any], user_answer: Dict[str, Any]) -> Dict[str, Any]:
    scorer = SCORERS.get(q_type)
    if not scorer:
        raise ValueError(f"No scorer registered for question type: {q_type}")
    return scorer(correct_answer, user_answer)
