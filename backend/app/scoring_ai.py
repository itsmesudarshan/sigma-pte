"""
Optional AI-assisted scoring for the semantic Writing traits (Content,
Development/Structure/Coherence, General Linguistic Range) using Groq's
free-tier API (llama-3.3-70b-versatile — same model already used in
jodi_makerbot).

This is entirely optional: if GROQ_API_KEY is not set, or the API call
fails for any reason (network, rate limit, malformed response), every
function here returns None and the caller falls back to pure heuristic
scoring. Nothing breaks without a key.

The AI is prompted with Pearson's actual published band descriptors
(pulled from the official Score Guide) so its judgments are anchored to
the real rubric rather than a generic "grade this essay" request.
"""

import os
import json
import re
from urllib import request as urlrequest, error as urlerror

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


def _call_groq(system_prompt: str, user_prompt: str) -> dict | None:
    if not GROQ_API_KEY:
        return None

    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 400,
    }).encode("utf-8")

    req = urlrequest.Request(
        GROQ_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        return json.loads(match.group(0))
    except (urlerror.URLError, KeyError, IndexError, json.JSONDecodeError, TimeoutError):
        return None


SWT_SYSTEM_PROMPT = """You are scoring a PTE Academic "Summarize Written Text" response \
using Pearson's official Content band descriptors (0-4 scale):
4 = source text summarised comprehensively, full comprehension, effective paraphrasing, all main ideas synthesized concisely.
3 = summarised adequately, good comprehension, paraphrasing not always consistent, minor omissions.
2 = summarised partially, basic comprehension, relies on repeating source excerpts rather than own words.
1 = relevant but not meaningfully summarised, limited comprehension, disconnected excerpts.
0 = too limited, no comprehension shown.

Respond ONLY with JSON: {"content": <0-4 integer>, "reason": "<one short sentence>"}"""


ESSAY_SYSTEM_PROMPT = """You are scoring a PTE Academic Essay using Pearson's official band \
descriptors. Score three traits:

CONTENT (0-6): 6=fully addresses prompt in depth with own-words reformulation and specific \
supporting examples; 5=adequately addresses prompt, persuasive, minor gaps; 4=addresses main \
point but lacks depth; 3=relevant but doesn't address main points adequately; 2=superficial, \
generic, or relies on prompt language; 1=incomplete understanding, generic/repetitive; 0=does \
not deal with prompt.

DEVELOPMENT_STRUCTURE_COHERENCE (0-6): 6=effective logical structure, smooth flow, clear \
argument developed at length, intro+conclusion+organized paragraphs, varied connectives; \
5=conventional appropriate structure, clear argument, intro/conclusion/paragraphs present; \
4=structure mostly present but some elements missing; 3=traces of structure, disconnected \
ideas, undeveloped position; 2=little recognizable structure, disorganized; 1=disconnected \
ideas, no hierarchy; 0=no recognizable structure.

GENERAL_LINGUISTIC_RANGE (0-6): 6=varied expression/vocabulary used with ease and precision, \
no limitations; 5=varied expression throughout, ideas clear; 4=sufficient range for basic \
ideas, limitations on complex ideas; 3=narrow range, simple expressions repeated; 2=limited \
vocabulary, compromised communication; 1=highly restricted, ideas generally unclear; 0=meaning \
not accessible.

Respond ONLY with JSON:
{"content": <0-6>, "dsc": <0-6>, "linguistic_range": <0-6>, "reason": "<one short sentence>"}"""


def ai_score_swt(source_text: str, response: str) -> dict | None:
    user_prompt = f"SOURCE TEXT:\n{source_text}\n\nSTUDENT SUMMARY:\n{response}"
    result = _call_groq(SWT_SYSTEM_PROMPT, user_prompt)
    if not result or "content" not in result:
        return None
    try:
        content = int(result["content"])
    except (TypeError, ValueError):
        return None
    if not 0 <= content <= 4:
        return None
    return {"content": content, "reason": result.get("reason", "")}


def ai_score_essay(prompt_text: str, response: str) -> dict | None:
    user_prompt = f"ESSAY PROMPT:\n{prompt_text}\n\nSTUDENT ESSAY:\n{response}"
    result = _call_groq(ESSAY_SYSTEM_PROMPT, user_prompt)
    if not result:
        return None
    try:
        content = int(result["content"])
        dsc = int(result["dsc"])
        glr = int(result["linguistic_range"])
    except (TypeError, ValueError, KeyError):
        return None
    if not (0 <= content <= 6 and 0 <= dsc <= 6 and 0 <= glr <= 6):
        return None
    return {"content": content, "dsc": dsc, "linguistic_range": glr, "reason": result.get("reason", "")}


SPEAKING_CONTENT_SYSTEM_PROMPT = """You are scoring the CONTENT of a PTE Academic spoken response that has \
been transcribed to text. Score 0-3 using Pearson's Content descriptors:
3 = response covers all/nearly all relevant aspects of the task (target text, image, lecture, or question).
2 = response covers most relevant aspects, with minor omissions.
1 = response covers some relevant aspects, notable omissions or irrelevant content.
0 = response has little or no relevant content.

Respond ONLY with JSON: {"content": <0-3 integer>, "reason": "<one short sentence>"}"""


def ai_score_speaking_content(task_description: str, target_or_reference: str, transcript: str) -> dict | None:
    user_prompt = (
        f"TASK: {task_description}\n\nREFERENCE MATERIAL:\n{target_or_reference}\n\n"
        f"STUDENT'S SPOKEN RESPONSE (transcribed):\n{transcript}"
    )
    result = _call_groq(SPEAKING_CONTENT_SYSTEM_PROMPT, user_prompt)
    if not result or "content" not in result:
        return None
    try:
        content = int(result["content"])
    except (TypeError, ValueError):
        return None
    if not 0 <= content <= 3:
        return None
    return {"content": content, "reason": result.get("reason", "")}


def blend(heuristic_score: int, ai_score: int | None, max_score: int, ai_weight: float = 0.7) -> int:
    """Blend AI + heuristic, rounding to nearest valid integer band. Falls back
    to pure heuristic if AI score is unavailable."""
    if ai_score is None:
        return heuristic_score
    blended = ai_weight * ai_score + (1 - ai_weight) * heuristic_score
    return max(0, min(max_score, round(blended)))
