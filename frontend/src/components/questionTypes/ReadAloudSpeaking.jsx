import { useState } from 'react';
import { Play } from 'lucide-react';
import PrepCountdown from '../PrepCountdown';
import TTSPlayer from '../TTSPlayer';
import SpeechRecorder from '../SpeechRecorder';
import ColoredTranscript from '../ColoredTranscript';

export default function ReadAloudSpeaking({ passage, content, onChange, result, isRepeat }) {
  const [prepDone, setPrepDone] = useState(false);
  const [audioDone, setAudioDone] = useState(false);
  const [audioKey, setAudioKey] = useState(0);

  const readyToRecord = isRepeat ? (prepDone && audioDone) : prepDone;

  const skipAudioWait = () => {
    window.speechSynthesis?.cancel();
    setAudioDone(true);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {!isRepeat ? (
        <div style={{ padding: 18, background: 'var(--paper)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line)', fontSize: 16, lineHeight: 1.7, color: 'var(--ink)' }}>
          {passage}
        </div>
      ) : (
        <>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
            Listen to the sentence, then repeat it exactly as you heard it.
          </p>
          {prepDone && (
            <TTSPlayer key={audioKey} text={passage} rate={1} autoPlay onEnd={() => setAudioDone(true)} />
          )}
          {result && (
            <div style={{ padding: 14, borderRadius: 'var(--radius-sm)', background: 'var(--paper)', border: '1px solid var(--line)', fontSize: 13, color: 'var(--text-secondary)' }}>
              <strong style={{ color: 'var(--text-primary)' }}>Original sentence:</strong> {passage}
            </div>
          )}
        </>
      )}

      {!result && !readyToRecord && !(isRepeat && prepDone) && (
        <PrepCountdown
          seconds={isRepeat ? 3 : (content.prep_seconds || 20)}
          label={isRepeat ? 'Get ready' : 'Preparation time'}
          onComplete={() => setPrepDone(true)}
        />
      )}

      {!result && isRepeat && prepDone && !audioDone && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', background: 'var(--paper)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line)' }}>
          <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>Listening... recording starts automatically once the audio ends.</p>
          <button
            onClick={skipAudioWait}
            style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '6px 14px', borderRadius: 999, border: 'none', background: 'var(--ink)', color: '#fff', fontSize: 12, fontWeight: 700, flexShrink: 0 }}
          >
            <Play size={12} fill="#fff" /> Start Now
          </button>
        </div>
      )}

      {(readyToRecord || result) && (
        <SpeechRecorder
          disabled={!!result}
          autoStart={readyToRecord && !result}
          autoStopSeconds={content.record_seconds || 40}
          onResult={onChange}
        />
      )}

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 4 }}>
          <ColoredTranscript wordsDetail={result.breakdown.words_detail} scoringTier={result.breakdown.pronunciation_scoring_tier} />
          <TraitBar label="Content" score={result.breakdown.content} max={result.breakdown.content_max} />
          <TraitBar label="Oral Fluency" score={result.breakdown.fluency} max={result.breakdown.fluency_max} />
          <TraitBar label="Pronunciation" score={result.breakdown.pronunciation} max={result.breakdown.pronunciation_max} />
          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
            {result.breakdown.notes?.pronunciation_caveat}
          </p>
          <p style={{ fontSize: 11, color: 'var(--text-muted)' }}>
            {result.breakdown.ai_assisted ? '✓ AI-assisted content scoring' : 'Heuristic content scoring (add a free Groq API key for AI assistance)'}
          </p>
        </div>
      )}
    </div>
  );
}

function TraitBar({ label, score, max }) {
  const pct = max ? (score / max) * 100 : 0;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', width: 110, flexShrink: 0 }}>{label}</span>
      <div style={{ flex: 1, height: 6, borderRadius: 999, background: 'var(--line)', overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: 'var(--focus)' }} />
      </div>
      <span className="mono" style={{ fontSize: 12, fontWeight: 700, color: 'var(--ink)', width: 36, textAlign: 'right' }}>{score}/{max}</span>
    </div>
  );
}
