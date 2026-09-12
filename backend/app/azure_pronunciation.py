"""
Calls Azure AI Speech's Pronunciation Assessment REST API for genuine
acoustic pronunciation and fluency scoring — a real per-phoneme comparison
against the target text, computed on Microsoft's servers, not a local
model or a text-matching proxy.

Entirely optional: if AZURE_SPEECH_KEY / AZURE_SPEECH_REGION aren't set, or
the call fails for any reason (network error, quota exceeded, malformed
audio), this returns None and the caller falls back to the existing
heuristic-based estimate. Nothing breaks without it configured.

Audio format requirement: Azure's REST API for short audio only accepts
WAV/PCM or OGG/Opus, both at 16kHz mono — NOT the webm/opus format browsers
natively record. The frontend (see SpeechRecorder.jsx) handles this by
decoding and re-encoding to 16kHz mono WAV entirely in-browser via the Web
Audio API before sending audio here, so no server-side audio conversion
(e.g. ffmpeg) is needed.

Free tier (F0): 5 audio hours/month, shared across the whole account. Once
exceeded, Azure returns a quota error — handled here as a graceful
fallback to heuristic scoring, not a crash.
"""

import os
import json
import base64
from urllib import request as urlrequest, error as urlerror

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "").strip()
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "").strip()


def is_azure_configured() -> bool:
    return bool(AZURE_SPEECH_KEY and AZURE_SPEECH_REGION)


def _build_pronunciation_assessment_header(reference_text: str) -> str:
    config = {
        "ReferenceText": reference_text,
        "GradingSystem": "HundredMark",
        "Granularity": "Phoneme",
        "Dimension": "Comprehensive",
        "EnableMiscue": True,
    }
    config_json = json.dumps(config).encode("utf-8")
    return base64.b64encode(config_json).decode("utf-8")


def _map_100_to_5(score_100) -> int:
    """Azure scores 0-100; PTE's Speaking traits use a 0-5 band."""
    if score_100 is None:
        return 0
    band = round((float(score_100) / 100) * 5)
    return max(0, min(5, band))


def score_pronunciation_via_azure(wav_base64: str, reference_text: str) -> dict | None:
    if not is_azure_configured() or not wav_base64 or not reference_text.strip():
        return None

    try:
        audio_bytes = base64.b64decode(wav_base64)
    except Exception:
        return None

    url = (
        f"https://{AZURE_SPEECH_REGION}.stt.speech.microsoft.com"
        f"/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json",
        "Pronunciation-Assessment": _build_pronunciation_assessment_header(reference_text),
    }

    req = urlrequest.Request(url, data=audio_bytes, headers=headers, method="POST")

    try:
        with urlrequest.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urlerror.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None

    if data.get("RecognitionStatus") != "Success":
        return None

    try:
        best = data["NBest"][0]
        assessment = best["PronunciationAssessment"]
        accuracy = assessment.get("AccuracyScore")
        fluency = assessment.get("FluencyScore")
        pronunciation_overall = assessment.get("PronScore")
        completeness = assessment.get("CompletenessScore")
    except (KeyError, IndexError):
        return None

    # Per-word error categorization — Azure flags each word as correctly
    # pronounced ("None"), mispronounced, omitted (expected but not said),
    # or inserted (said but not expected), when EnableMiscue is on. This
    # is what powers the color-coded transcript shown after scoring,
    # rather than just an overall number.
    words_detail = []
    for w in best.get("Words", []):
        error_type = (w.get("PronunciationAssessment", {}) or {}).get("ErrorType", "None")
        status = {
            "None": "correct",
            "Mispronunciation": "mispronunciation",
            "Omission": "omission",
            "Insertion": "insertion",
        }.get(error_type, "correct")
        words_detail.append({
            "word": w.get("Word", ""),
            "status": status,
            "accuracy": (w.get("PronunciationAssessment", {}) or {}).get("AccuracyScore"),
        })

    return {
        "pronunciation": _map_100_to_5(pronunciation_overall if pronunciation_overall is not None else accuracy),
        "fluency": _map_100_to_5(fluency),
        "accuracy_raw": accuracy,
        "completeness_raw": completeness,
        "recognized_text": best.get("Display") or best.get("Lexical"),
        "words_detail": words_detail,
    }
