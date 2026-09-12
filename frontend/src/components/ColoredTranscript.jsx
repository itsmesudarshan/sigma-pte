const STATUS_STYLES = {
  correct: { bg: 'var(--success-soft)', color: 'var(--success)', label: 'Correct' },
  mispronunciation: { bg: 'var(--amber-soft)', color: 'var(--amber)', label: 'Mispronounced' },
  omission: { bg: 'var(--error-soft)', color: 'var(--error)', label: 'Missed word' },
  insertion: { bg: 'rgba(139,92,246,0.12)', color: '#8B5CF6', label: 'Extra word' },
  extra: { bg: 'rgba(139,92,246,0.12)', color: '#8B5CF6', label: 'Extra word' },
};

export default function ColoredTranscript({ wordsDetail, scoringTier }) {
  if (!wordsDetail || wordsDetail.length === 0) return null;

  const hasOmissions = wordsDetail.some((w) => w.status === 'omission');
  const spoken = wordsDetail.filter((w) => w.status !== 'omission');
  const omitted = wordsDetail.filter((w) => w.status === 'omission');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <p style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        Your response
      </p>

      <p style={{ fontSize: 15, lineHeight: 2.1 }}>
        {spoken.map((w, i) => {
          const style = STATUS_STYLES[w.status] || STATUS_STYLES.correct;
          return (
            <span
              key={i}
              style={{
                display: 'inline-block', padding: '2px 6px', margin: '0 3px 4px 0', borderRadius: 5,
                background: style.bg, color: style.color, fontWeight: 600,
              }}
              title={style.label}
            >
              {w.word}
            </span>
          );
        })}
      </p>

      {hasOmissions && (
        <div>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 4 }}>Words you missed:</p>
          <p style={{ fontSize: 14, lineHeight: 1.8 }}>
            {omitted.map((w, i) => (
              <span
                key={i}
                style={{ display: 'inline-block', padding: '2px 6px', margin: '0 3px 4px 0', borderRadius: 5, background: 'var(--error-soft)', color: 'var(--error)', fontWeight: 600 }}
              >
                {w.word}
              </span>
            ))}
          </p>
        </div>
      )}

      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginTop: 2 }}>
        {Object.entries({ correct: 'Correct', mispronunciation: 'Mispronounced', omission: 'Missed', insertion: 'Extra' }).map(([key, label]) => (
          <span key={key} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 11, color: 'var(--text-muted)' }}>
            <span style={{ width: 9, height: 9, borderRadius: 3, background: STATUS_STYLES[key].color, display: 'inline-block' }} />
            {label}
          </span>
        ))}
      </div>

      {scoringTier === 'heuristic' && (
        <p style={{ fontSize: 11, color: 'var(--text-muted)' }}>
          Based on word matching only — mispronunciation detection needs real acoustic scoring (not configured).
        </p>
      )}
    </div>
  );
}
