"""
Scoring engine for PTE Academic Speaking question types (Read Aloud,
Repeat Sentence, Answer Short Question, Describe Image), aligned to
Pearson's official scoring traits: Content (0-3), Oral Fluency (0-5),
Pronunciation (0-5).

PRONUNCIATION & FLUENCY SCORING — two tiers:

  1. Real acoustic scoring (preferred, when configured): the actual audio
     recording is sent to Azure AI Speech's Pronunciation Assessment API
     (see app/azure_pronunciation.py). This performs a genuine phoneme-
     level comparison between the sounds you actually produced and what's
     expected for the target text, computed on Microsoft's servers — not
     a text-matching proxy. Free tier (F0): 5 audio hours/month.

  2. Heuristic fallback (always available, used automatically if Azure
     isn't configured, the free quota is exhausted, or a call to it
     fails): estimates pronunciation from how accurately the browser's
     built-in speech recognizer transcribed the target vocabulary,
     optionally blended with the recognizer's own confidence score when
     the browser provides one. This is a weaker proxy — a recognizer can
     still guess the right words from imperfect pronunciation — which is
     exactly why tier 1 exists.

Which tier was used is always reported in the response so the person can
see which kind of signal they're looking at.
"""

import re
from app.scoring_ai import ai_score_speaking_content, blend
from app.azure_pronunciation import score_pronunciation_via_azure, is_azure_configured

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
    Heuristic fallback only (used when real phoneme scoring isn't
    available). Blends word-level match against the target text with the
    browser's own recognition confidence when available.
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
    """Detects repeated 3-word phrases as a proxy for disfluent, padded, or
    circular speech — something pure words-per-minute can't catch."""
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


def _get_pronunciation_and_fluency(target_text, transcript, transcript_words, duration_seconds, confidence, wav_base64):
    """Tries real Azure phoneme-level scoring first, falls back to heuristic."""
    if is_azure_configured() and wav_base64:
        azure_result = score_pronunciation_via_azure(wav_base64, target_text)
        if azure_result:
            return {
                "pronunciation": azure_result["pronunciation"],
                "fluency": azure_result["fluency"],
                "scoring_tier": "azure",
                "phoneme_detail": {
                    "recognized_text": azure_result.get("recognized_text"),
                    "accuracy_raw": azure_result.get("accuracy_raw"),
                    "completeness_raw": azure_result.get("completeness_raw"),
                },
            }

    # Fallback: heuristic
    target_words = _tokenize(target_text)
    fluency = max(0, estimate_fluency(len(transcript_words), duration_seconds) - repetition_penalty(transcript_words))
    pronunciation = estimate_pronunciation(target_words, transcript_words, confidence)
    return {
        "pronunciation": pronunciation,
        "fluency": fluency,
        "scoring_tier": "heuristic",
        "phoneme_detail": None,
    }


# ---------------- Read Aloud / Repeat Sentence ----------------

def score_read_aloud_or_repeat(target_text: str, transcript: str, duration_seconds: float, confidence=None, wav_base64=None) -> dict:
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

    pf = _get_pronunciation_and_fluency(target_text, transcript, transcript_words, duration_seconds, confidence, wav_base64)

    total = content_score + pf["fluency"] + pf["pronunciation"]

    return {
        "content": content_score, "content_max": 3,
        "fluency": pf["fluency"], "fluency_max": 5,
        "pronunciation": pf["pronunciation"], "pronunciation_max": 5,
        "total": total, "max_total": 13,
        "transcript": transcript,
        "word_match_ratio": round(overlap, 2),
        "sequence_similarity": round(order_similarity, 2),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "pronunciation_scoring_tier": pf["scoring_tier"],
        "phoneme_detail": pf["phoneme_detail"],
        "notes": {
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
            "pronunciation_caveat": (
                "Real phoneme-level acoustic scoring." if pf["scoring_tier"] == "azure"
                else "Estimated from speech-recognition word match, not true phonetic analysis (phoneme model not configured or unavailable)."
            ),
        },
    }


# ---------------- Answer Short Question ----------------

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


CHART_TYPE_WORDS = {
    "bar": ["bar chart", "bar graph", "bar diagram"],
    "line": ["line chart", "line graph", "line diagram"],
    "pie": ["pie chart", "pie graph", "pie diagram"],
}


def _detect_chart_type_mismatch(transcript_lower: str, correct_chart_type: str) -> bool:
    for chart_type, phrases in CHART_TYPE_WORDS.items():
        if chart_type == correct_chart_type:
            continue
        if any(phrase in transcript_lower for phrase in phrases):
            return True
    return False


def score_describe_image(task_description: str, key_points: list, transcript: str, duration_seconds: float, chart_type: str = None, confidence=None, wav_base64=None) -> dict:
    transcript_words = _tokenize(transcript)
    transcript_lower = transcript.lower()

    transcript_set = set(transcript_words)
    covered = sum(1 for point in key_points if any(kw.lower() in transcript_set for kw in point))
    coverage = covered / len(key_points) if key_points else 0.0

    chart_mismatch = chart_type and _detect_chart_type_mismatch(transcript_lower, chart_type)

    if len(transcript_words) < 5:
        heuristic_content = 0
    elif chart_mismatch:
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

    # For Describe Image there's no fixed target sentence, so real phoneme
    # scoring compares against the transcript itself (self-consistency
    # check on how clearly the words were articulated) rather than a
    # known target text.
    pf = _get_pronunciation_and_fluency(transcript, transcript, transcript_words, duration_seconds, confidence, wav_base64)

    total = content_score + pf["fluency"] + pf["pronunciation"]

    return {
        "content": content_score, "content_max": 3,
        "fluency": pf["fluency"], "fluency_max": 5,
        "pronunciation": pf["pronunciation"], "pronunciation_max": 5,
        "total": total, "max_total": 13,
        "transcript": transcript,
        "coverage_ratio": round(coverage, 2),
        "chart_type_mismatch": bool(chart_mismatch),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "pronunciation_scoring_tier": pf["scoring_tier"],
        "phoneme_detail": pf["phoneme_detail"],
        "notes": {
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
            "pronunciation_caveat": (
                "Real phoneme-level acoustic scoring." if pf["scoring_tier"] == "azure"
                else "Estimated from recognizable-word ratio — a weaker proxy since there's no fixed target sentence."
            ),
            **({"chart_type_warning": f"You referred to this as a different chart type than what's shown ({chart_type} chart) — this caps your Content score."} if chart_mismatch else {}),
        },
    }
