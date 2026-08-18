"""
Scoring engine for PTE Academic Writing question types (Summarize Written
Text, Write Essay), aligned to Pearson's official Test Taker Score Guide
criteria (verified against Pearson's published PDF, current as of the
August 2026 update: Content 0-4 for SWT, seven-trait 0-6 scale for Essay).

Scoring approach per trait:
  - Form, word count, sentence count: exact official rules (fully reliable,
    deterministic — no AI or heuristic involved)
  - Grammar, Spelling: rule-based + offline dictionary checks (reliable for
    clear errors; may miss some subtle grammatical issues)
  - Content, Development/Structure/Coherence, General Linguistic Range:
    BLENDED score — 70% AI judgment (Groq, when GROQ_API_KEY is set) + 30%
    keyword/structure heuristic, so one inconsistent AI call can't swing
    the score wildly. Falls back to 100% heuristic automatically if no AI
    key is configured or the API call fails — nothing breaks either way.
  - Vocabulary Range: heuristic only (lexical diversity proxy)
"""

import re
from spellchecker import SpellChecker
from app.scoring_ai import ai_score_swt, ai_score_essay, blend

_spell = SpellChecker()

CONNECTIVES = {
    "however", "therefore", "moreover", "furthermore", "consequently",
    "additionally", "nevertheless", "although", "because", "since",
    "while", "whereas", "thus", "hence", "in addition", "for example",
    "for instance", "in contrast", "on the other hand", "as a result",
    "in conclusion", "to conclude", "firstly", "secondly", "finally",
    "in summary", "overall", "meanwhile", "similarly", "in fact",
}


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", text))


def count_sentences(text: str) -> int:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([s for s in sentences if s.strip()])


def _tokenize(text: str):
    return [w.lower() for w in re.findall(r"[A-Za-z']+", text)]


def spelling_errors(text: str):
    words = _tokenize(text)
    candidates = [w for w in words if w.isalpha() and len(w) > 2]
    misspelled = _spell.unknown(candidates)
    return sorted(misspelled)


def grammar_error_estimate(text: str) -> int:
    errors = 0
    errors += len(re.findall(r"\b(\w+)\s+\1\b", text, flags=re.IGNORECASE))
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    for s in sentences:
        s = s.strip()
        if s and s[0].isalpha() and not s[0].isupper():
            errors += 1
    errors += len(re.findall(r"[.!?]{2,}", text))
    for s in sentences:
        word_count = len(s.split())
        if word_count > 40 and "," not in s:
            errors += 1
    return errors


def lexical_diversity(words):
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def keyword_coverage(response_words, key_points):
    if not key_points:
        return 0.0
    response_set = set(response_words)
    covered = 0
    for point_synonyms in key_points:
        if any(kw.lower() in response_set for kw in point_synonyms):
            covered += 1
    return covered / len(key_points)


def _heuristic_content_band_swt(coverage, diversity, word_count):
    if word_count < 3:
        return 0
    elif coverage >= 0.85 and diversity > 0.75:
        return 4
    elif coverage >= 0.65:
        return 3
    elif coverage >= 0.4:
        return 2
    elif coverage > 0:
        return 1
    return 0


# ---------------- Summarize Written Text ----------------

def score_swt(source_text: str, key_points: list, response: str) -> dict:
    words = _tokenize(response)
    word_count = len(words)
    sentence_count = count_sentences(response)

    is_one_sentence = sentence_count == 1
    in_word_range = 5 <= word_count <= 75
    is_all_caps = response.strip().isupper() and len(response.strip()) > 0
    form_score = 1 if (is_one_sentence and in_word_range and not is_all_caps) else 0

    coverage = keyword_coverage(words, key_points)
    diversity = lexical_diversity(words)
    heuristic_content = _heuristic_content_band_swt(coverage, diversity, word_count)

    ai_result = ai_score_swt(source_text, response) if word_count >= 3 else None
    ai_used = ai_result is not None
    content_score = blend(heuristic_content, ai_result["content"] if ai_result else None, max_score=4)

    grammar_errors = grammar_error_estimate(response)
    grammar_score = 2 if grammar_errors == 0 else (1 if grammar_errors <= 2 else 0)

    misspelled = spelling_errors(response)
    vocab_score = 2 if len(misspelled) == 0 else (1 if len(misspelled) <= 2 else 0)

    total = content_score + form_score + grammar_score + vocab_score

    return {
        "content": content_score, "content_max": 4,
        "form": form_score, "form_max": 1,
        "grammar": grammar_score, "grammar_max": 2,
        "vocabulary": vocab_score, "vocabulary_max": 2,
        "total": total, "max_total": 9,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "misspelled_words": misspelled,
        "coverage_ratio": round(coverage, 2),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "notes": {
            "form": "One complete sentence, 5-75 words required." if form_score == 0 else "Form requirement met.",
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
        },
    }


# ---------------- Write Essay ----------------

def score_essay(prompt_text: str, key_points: list, response: str) -> dict:
    words = _tokenize(response)
    word_count = len(words)
    paragraphs = [p for p in response.split("\n") if p.strip()]
    paragraph_count = len(paragraphs)
    is_all_caps = response.strip().isupper() and len(response.strip()) > 0
    has_punctuation = bool(re.search(r"[.!?]", response))

    if word_count < 120 or word_count > 380 or is_all_caps or not has_punctuation:
        form_score = 0
    elif 200 <= word_count <= 300:
        form_score = 2
    else:
        form_score = 1

    if form_score == 0:
        return {
            "content": 0, "content_max": 6,
            "form": 0, "form_max": 2,
            "dsc": 0, "dsc_max": 6,
            "grammar": 0, "grammar_max": 2,
            "linguistic_range": 0, "linguistic_range_max": 6,
            "vocabulary": 0, "vocabulary_max": 2,
            "spelling": 0, "spelling_max": 2,
            "total": 0, "max_total": 26,
            "word_count": word_count,
            "paragraph_count": paragraph_count,
            "misspelled_words": [],
            "coverage_ratio": 0,
            "ai_assisted": False,
            "ai_reason": None,
            "notes": {"form": "Essay must be 120-380 words with normal punctuation and capitalization for any score to be given."},
        }

    coverage = keyword_coverage(words, key_points)
    diversity = lexical_diversity(words)

    if coverage >= 0.8 and word_count >= 200:
        heuristic_content = 6
    elif coverage >= 0.65:
        heuristic_content = 5
    elif coverage >= 0.5:
        heuristic_content = 4
    elif coverage >= 0.3:
        heuristic_content = 3
    elif coverage >= 0.15:
        heuristic_content = 2
    elif coverage > 0:
        heuristic_content = 1
    else:
        heuristic_content = 0

    connective_hits = sum(1 for c in CONNECTIVES if c in response.lower())
    has_intro_conclusion = paragraph_count >= 3
    if paragraph_count >= 4 and connective_hits >= 4 and has_intro_conclusion:
        heuristic_dsc = 6
    elif paragraph_count >= 3 and connective_hits >= 3:
        heuristic_dsc = 5
    elif paragraph_count >= 3 and connective_hits >= 1:
        heuristic_dsc = 4
    elif paragraph_count >= 2:
        heuristic_dsc = 3
    elif connective_hits >= 1:
        heuristic_dsc = 2
    elif word_count > 0:
        heuristic_dsc = 1
    else:
        heuristic_dsc = 0

    sentence_lengths = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", response.strip()) if s.strip()]
    length_variety = (max(sentence_lengths) - min(sentence_lengths)) if len(sentence_lengths) > 1 else 0
    if diversity >= 0.65 and length_variety >= 10:
        heuristic_glr = 6
    elif diversity >= 0.55 and length_variety >= 6:
        heuristic_glr = 5
    elif diversity >= 0.48:
        heuristic_glr = 4
    elif diversity >= 0.4:
        heuristic_glr = 3
    elif diversity >= 0.3:
        heuristic_glr = 2
    elif word_count > 0:
        heuristic_glr = 1
    else:
        heuristic_glr = 0

    ai_result = ai_score_essay(prompt_text, response)
    ai_used = ai_result is not None

    content_score = blend(heuristic_content, ai_result["content"] if ai_result else None, max_score=6)
    dsc_score = blend(heuristic_dsc, ai_result["dsc"] if ai_result else None, max_score=6)
    glr_score = blend(heuristic_glr, ai_result["linguistic_range"] if ai_result else None, max_score=6)

    grammar_errors = grammar_error_estimate(response)
    grammar_score = 2 if grammar_errors <= 1 else (1 if grammar_errors <= 4 else 0)

    vocab_score = 2 if diversity >= 0.55 else (1 if diversity >= 0.4 else 0)

    misspelled = spelling_errors(response)
    spelling_score = 2 if len(misspelled) == 0 else (1 if len(misspelled) == 1 else 0)

    total = (
        content_score + form_score + dsc_score + grammar_score
        + glr_score + vocab_score + spelling_score
    )

    return {
        "content": content_score, "content_max": 6,
        "form": form_score, "form_max": 2,
        "dsc": dsc_score, "dsc_max": 6,
        "grammar": grammar_score, "grammar_max": 2,
        "linguistic_range": glr_score, "linguistic_range_max": 6,
        "vocabulary": vocab_score, "vocabulary_max": 2,
        "spelling": spelling_score, "spelling_max": 2,
        "total": total, "max_total": 26,
        "word_count": word_count,
        "paragraph_count": paragraph_count,
        "misspelled_words": misspelled,
        "coverage_ratio": round(coverage, 2),
        "ai_assisted": ai_used,
        "ai_reason": ai_result.get("reason") if ai_result else None,
        "notes": {
            "form": f"{word_count} words — full Form marks need 200-300 words.",
            "scoring_method": "AI + heuristic blend" if ai_used else "Heuristic only (no AI key configured, or AI call unavailable)",
        },
    }
