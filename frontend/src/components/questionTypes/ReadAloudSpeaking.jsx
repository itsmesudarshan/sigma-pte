import SpeechRecorder from '../SpeechRecorder';

export default function ReadAloudSpeaking({ passage, content, userAnswer, onChange, result, isRepeat }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {!isRepeat && (
        <div style={{ padding: 18, background: 'var(--paper)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line)', fontSize: 16, lineHeight: 1.7, color: 'var(--ink)' }}>
          {passage}
        </div>
      )}
      {isRepeat && (
        <div style={{ padding: 18, background: 'var(--amber-soft)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--amber)', fontSize: 13, color: 'var(--text-primary)' }}>
          Listen to the sentence, then repeat it exactly. (Sentence text is hidden until you submit — in this
          browser-based version, read it silently once to simulate hearing it, then record.)
          <p style={{ marginTop: 10, fontStyle: 'italic', color: 'var(--text-secondary)' }}>{passage}</p>
        </div>
      )}

      <SpeechRecorder
        disabled={!!result}
        autoStopSeconds={content.record_seconds || 40}
        onResult={onChange}
      />

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 4 }}>
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
