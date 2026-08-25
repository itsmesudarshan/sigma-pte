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


def estimate_pronunciation(target_words, transcript_words, confidence=None) -> int:
    """
    Blends two signals: word-level match against the target text (was the
    right vocabulary produced), and the browser's own recognition confidence
    when available (a genuine per-utterance signal from the speech engine,
    not a guess). Falls back to word-overlap alone if confidence wasn't
    captured (older browsers, or Firefox/Safari which don't expose it).
    """
    overlap = word_overlap_ratio(target_words, transcript_words)

    if confidence is not None:
        combined = (confidence * 0.6) + (overlap * 0.4)
    else:
        combined = overlap

    if combined >= 0.9:
        return 5
    elif combined >= 0.75:
        return 4
    elif combined >= 0.55:
        return 3
    elif combined >= 0.35:
        return 2
    elif combined > 0:
        return 1
    return 0


def repetition_penalty(words) -> int:
    """
    Detects repeated 3-word phrases as a proxy for disfluent, padded, or
    circular speech — something pure words-per-minute can't catch, since a
    rambling response can still hit a natural pace. Returns a 0-2 point
    penalty to subtract from the fluency score.
    """
    if len(words) < 6:
        return 0
    trigrams = [tuple(words[i:i + 3]) for i in range(len(words) - 2)]
    if not trigrams:
        return 0
    seen = set()
    repeats = 0
    for t in trigrams:
        if t in seen:
            repeats += 1
        seen.add(t)
    repeat_ratio = repeats / len(trigrams)
    if repeat_ratio >= 0.25:
        return 2
    elif repeat_ratio >= 0.12:
        return 1
    return 0


# ---------------- Read Aloud / Repeat Sentence ----------------
# Both compare a spoken transcript against a fixed target text.

def score_read_aloud_or_repeat(target_text: str, transcript: str, duration_seconds: float, confidence=None) -> dict:
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

    fluency_score = max(0, estimate_fluency(len(transcript_words), duration_seconds) - repetition_penalty(transcript_words))
    pronunciation_score = estimate_pronunciation(target_words, transcript_words, confidence)

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
            "pronunciation_caveat": "Blends browser recognition confidence with word-level match — not true phonetic analysis." if confidence is not None else "Estimated from speech-recognition word match only, not true phonetic analysis (browser didn't report confidence).",
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


# ---------------- Describe Image ----------------
# Open-ended spoken response describing a chart/graph — no fixed target text,
# so Content is scored against key_points (keyword coverage + optional AI
# judgment, same pattern as Writing), while Fluency stays rate-based.
# Pronunciation has no target text to compare against here, so it's
# approximated from how many transcribed words are recognizable English
# words at all — a weaker proxy than Read Aloud's word-overlap method,
# flagged accordingly in the response.

from app.scoring_writing import _spell as _dictionary


def _recognizable_word_ratio(words):
    if not words:
        return 0.0
    candidates = [w for w in words if w.isalpha() and len(w) > 2]
    if not candidates:
        return 0.0
    unknown = _dictionary.unknown(candidates)
    return 1 - (len(unknown) / len(candidates))


CHART_TYPE_WORDS = {
    "bar": ["bar chart", "bar graph", "bar diagram"],
    "line": ["line chart", "line graph", "line diagram"],
    "pie": ["pie chart", "pie graph", "pie diagram"],
}


def _detect_chart_type_mismatch(transcript_lower: str, correct_chart_type: str) -> bool:
    """Returns True if the speaker explicitly named a DIFFERENT chart type
    than the one actually shown (e.g. said 'bar graph' for a pie chart) —
    a factual error that keyword-overlap scoring alone would miss, since
    'graph' still matches regardless of which chart type precedes it."""
    for chart_type, phrases in CHART_TYPE_WORDS.items():
        if chart_type == correct_chart_type:
            continue
        if any(phrase in transcript_lower for phrase in phrases):
            return True
    return False


def score_describe_image(task_description: str, key_points: list, transcript: str, duration_seconds: float, chart_type: str = None, confidence=None) -> dict:
    transcript_words = _tokenize(transcript)
    transcript_lower = transcript.lower()

    transcript_set = set(transcript_words)
    covered = sum(1 for point in key_points if any(kw.lower() in transcript_set for kw in point))
    coverage = covered / len(key_points) if key_points else 0.0

    chart_mismatch = chart_type and _detect_chart_type_mismatch(transcript_lower, chart_type)

    if len(transcript_words) < 5:
        heuristic_content = 0
    elif chart_mismatch:
        # Naming the wrong chart type is a factual error about the prompt
        # itself — cap content regardless of how much other vocabulary matches.
        heuristic_content = 1
    elif coverage >= 0.75:
        heuristic_content = 3
    elif coverage >= 0.4:
        heuristic_content = 2
    elif coverage > 0:
        heuristic_content = 1
    else:
        heuristic_content = 0

    task_with_type = f"{task_description} (The image is actually a {chart_type} chart — penalize the response if it misidentifies the chart type.)" if chart_type else task_description
    ai_result = ai_score_speaking_content(task_with_type, ", ".join(kw[0] for kw in key_points), transcript) if len(transcript_words) >= 5 else None
    ai_used = ai_result is not None
    content_score = blend(heuristic_content, ai_result["content"] if ai_result else None, max_score=3)
    if chart_mismatch:
        content_score = min(content_score, 1)

    fluency_score = max(0, estimate_fluency(len(transcript_words), duration_seconds) - repetition_penalty(transcript_words))

    if confidence is not None:
        recognizable_ratio = _recognizable_word_ratio(transcript_words)
        combined = (confidence * 0.6) + (recognizable_ratio * 0.4)
    else:
        combined = _recognizable_word_ratio(transcript_words)

    if combined >= 0.9:
        pronunciation_score = 5
    elif combined >= 0.75:
        pronunciation_score = 4
    elif combined >= 0.55:
        pronunciation_score = 3
    elif combined >= 0.35:
        pronunciation_score = 2
    elif combined > 0:
        pronunciation_score = 1
    else:
        pronunciation_score = 0

    total = content_score + fluency_score + pronunciation_score

    return {
        "content": content_score, "content_max": 3,
        "fluency": fluency_score, "fluency_max": 5,
        "pronunciation": pronunciation_score, "pronunciation_max": 5,
        "total": total, "max_total": 13,
        "transcript": transcript,
        "coverage_ratio": round(coverage, 2),
        "chart_type_mismatch": bool(chart_mismatch),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "notes": {
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
            "pronunciation_caveat": "Blends browser recognition confidence with recognizable-word ratio — not true phonetic analysis." if confidence is not None else "Estimated from how many transcribed words are recognizable English words — a weaker proxy since there's no target sentence to compare against.",
            **({"chart_type_warning": f"You referred to this as a different chart type than what's shown ({chart_type} chart) — this caps your Content score."} if chart_mismatch else {}),
        },
    }
