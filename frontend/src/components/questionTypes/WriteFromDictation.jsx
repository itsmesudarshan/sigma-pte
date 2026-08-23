import TTSPlayer from '../TTSPlayer';

export default function WriteFromDictation({ content, userAnswer, onChange, result }) {
  const text = userAnswer?.text || '';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
      <TTSPlayer text={content.audio_text} />

      <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Type exactly what you hear, word for word.</p>

      <textarea
        disabled={!!result}
        value={text}
        onChange={(e) => onChange({ text: e.target.value })}
        placeholder="Type the sentence here..."
        rows={3}
        style={{ padding: 14, fontSize: 15, borderRadius: 'var(--radius-sm)', border: '1.5px solid var(--line-strong)', fontFamily: 'var(--font-body)', resize: 'vertical' }}
      />

      {result && (
        <div>
          <p style={{ fontSize: 13, lineHeight: 2 }}>
            {result.breakdown.per_word.map((w, i) => (
              <span
                key={i}
                className="mono"
                style={{ padding: '2px 5px', margin: '0 2px', borderRadius: 4, background: w.is_correct ? 'var(--success-soft)' : 'var(--error-soft)', color: w.is_correct ? 'var(--success)' : 'var(--error)', fontWeight: 600 }}
              >
                {w.given || '—'}
              </span>
            ))}
          </p>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 8 }}>Correct text: {result.breakdown.correct_text}</p>
        </div>
      )}
    </div>
  );
}
