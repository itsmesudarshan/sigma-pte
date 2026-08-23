"""
Scoring engine for PTE Academic Speaking question types (Read Aloud, Repeat
Sentence, Answer Short Question), aligned to Pearson's official scoring
traits: Content (0-3), Oral Fluency (0-5), Pronunciation (0-5).

IMPORTANT HONESTY NOTE:
Speech is captured in-browser via the free Web Speech API (SpeechRecognition),
which transcribes what you said to text — there is no paid speech service
involved. This means:
  - Content scoring compares your transcript to the target text/expected
    answer (word overlap + AI judgment when available) — reliable.
  - Oral Fluency is estimated from speaking rate (words per minute) and
    response timing, since the browser doesn't expose pause-by-pause audio
    analysis — a genuine approximation, not Pearson's proprietary fluency
    model.
  - Pronunciation is approximated by how accurately the browser's speech
    recognizer could transcribe your words. This is an indirect proxy: poor
    recognition often does correlate with unclear pronunciation, but this
    is the weakest-evidence trait here and should be read as directional,
    not exact.
"""

import re
from app.scoring_ai import ai_score_speaking_content, blend

WORDS_PER_MINUTE_IDEAL_MIN = 90
WORDS_PER_MINUTE_IDEAL_MAX = 160


def _tokenize(text: str):
    return [w.lower().strip(".,!?;:'\"") for w in text.split() if w.strip(".,!?;:'\"")]


def word_overlap_ratio(target_words, transcript_words):
    if not target_words:
        return 0.0
    target_set = set(target_words)
    transcript_set = set(transcript_words)
    matched = target_set & transcript_set
    return len(matched) / len(target_set)


def sequence_similarity(target_words, transcript_words):
    """Longest common subsequence ratio — rewards correct word order, not just presence."""
    if not target_words or not transcript_words:
        return 0.0
    m, n = len(target_words), len(transcript_words)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if target_words[i - 1] == transcript_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    return lcs / max(m, n)


def estimate_fluency(word_count: int, duration_seconds: float) -> int:
    """0-5 band based on speaking rate. Rewards a natural pace, penalizes
    both rushed and overly slow/hesitant delivery."""
    if duration_seconds <= 0 or word_count == 0:
        return 0
    wpm = (word_count / duration_seconds) * 60

    if WORDS_PER_MINUTE_IDEAL_MIN <= wpm <= WORDS_PER_MINUTE_IDEAL_MAX:
        return 5
    elif 70 <= wpm < WORDS_PER_MINUTE_IDEAL_MIN or WORDS_PER_MINUTE_IDEAL_MAX < wpm <= 190:
        return 4
    elif 50 <= wpm < 70 or 190 < wpm <= 220:
        return 3
    elif 30 <= wpm < 50 or wpm > 220:
        return 2
    elif wpm > 0:
        return 1
    return 0


def estimate_pronunciation(target_words, transcript_words) -> int:
    """Proxy: how cleanly the recognizer transcribed target vocabulary.
    Higher word-level match => clearer pronunciation, as a heuristic."""
    overlap = word_overlap_ratio(target_words, transcript_words)
    if overlap >= 0.9:
        return 5
    elif overlap >= 0.75:
        return 4
    elif overlap >= 0.55:
        return 3
    elif overlap >= 0.35:
        return 2
    elif overlap > 0:
        return 1
    return 0


# ---------------- Read Aloud / Repeat Sentence ----------------
# Both compare a spoken transcript against a fixed target text.

def score_read_aloud_or_repeat(target_text: str, transcript: str, duration_seconds: float) -> dict:
    target_words = _tokenize(target_text)
    transcript_words = _tokenize(transcript)

    overlap = word_overlap_ratio(target_words, transcript_words)
    order_similarity = sequence_similarity(target_words, transcript_words)
    heuristic_content_ratio = (overlap * 0.6) + (order_similarity * 0.4)

    if heuristic_content_ratio >= 0.9:
        heuristic_content = 3
    elif heuristic_content_ratio >= 0.65:
        heuristic_content = 2
    elif heuristic_content_ratio >= 0.35:
        heuristic_content = 1
    else:
        heuristic_content = 0

    ai_result = (
        ai_score_speaking_content("Read Aloud / Repeat Sentence — reproduce the target text exactly.", target_text, transcript)
        if transcript_words else None
    )
    ai_used = ai_result is not None
    content_score = blend(heuristic_content, ai_result["content"] if ai_result else None, max_score=3)

    fluency_score = estimate_fluency(len(transcript_words), duration_seconds)
    pronunciation_score = estimate_pronunciation(target_words, transcript_words)

    total = content_score + fluency_score + pronunciation_score

    return {
        "content": content_score, "content_max": 3,
        "fluency": fluency_score, "fluency_max": 5,
        "pronunciation": pronunciation_score, "pronunciation_max": 5,
        "total": total, "max_total": 13,
        "transcript": transcript,
        "word_match_ratio": round(overlap, 2),
        "sequence_similarity": round(order_similarity, 2),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "notes": {
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
            "pronunciation_caveat": "Estimated from speech-recognition accuracy, not true phonetic analysis.",
        },
    }


# ---------------- Answer Short Question ----------------
# Short factual answer, scored 0-1 (correct/incorrect) per official rubric —
# no fluency/pronunciation trait for this item type.

def score_answer_short_question(acceptable_answers: list, transcript: str) -> dict:
    transcript_words = set(_tokenize(transcript))
    is_correct = any(
        all(kw.lower() in transcript_words for kw in ans.split())
        for ans in acceptable_answers
    )
    score = 1 if is_correct else 0

    return {
        "content": score, "content_max": 1,
        "total": score, "max_total": 1,
        "transcript": transcript,
        "is_correct": is_correct,
        "ai_assisted": False,
        "notes": {"scoring_method": "Exact/near-match against acceptable answers (official rubric: correct=1, incorrect=0)."},
    }
