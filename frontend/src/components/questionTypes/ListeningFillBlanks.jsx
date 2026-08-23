import TTSPlayer from '../TTSPlayer';

function splitPassage(passage) {
  const parts = passage.split(/(\{\d+\})/g);
  return parts.map((part) => {
    const match = part.match(/^\{(\d+)\}$/);
    return match ? { blank: match[1] } : { text: part };
  });
}

export default function ListeningFillBlanks({ passage, content, userAnswer, onChange, result }) {
  const blanks = userAnswer?.blanks || {};
  const tokens = splitPassage(passage);

  const setBlank = (num, value) => onChange({ blanks: { ...blanks, [num]: value } });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
      <TTSPlayer text={content.audio_text} />

      <p style={{ fontSize: 15, lineHeight: 2.1, color: 'var(--ink)' }}>
        {tokens.map((tok, i) => {
          if (tok.text !== undefined) return <span key={i}>{tok.text}</span>;
          const num = tok.blank;
          const perBlank = result?.breakdown?.per_blank?.[num];
          let border = 'var(--line-strong)';
          if (result && perBlank) border = perBlank.is_correct ? 'var(--success)' : 'var(--error)';

          return (
            <input
              key={i}
              disabled={!!result}
              value={blanks[num] || ''}
              onChange={(e) => setBlank(num, e.target.value)}
              className="mono"
              style={{
                width: 110, margin: '0 4px', padding: '4px 8px', fontSize: 14, fontWeight: 600,
                borderRadius: 6, border: `1.5px solid ${border}`,
                background: result ? (perBlank?.is_correct ? 'var(--success-soft)' : 'var(--error-soft)') : 'var(--paper-raised)',
              }}
            />
          );
        })}
      </p>

      {result && (
        <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          Correct answers: {Object.entries(result.correct_answer.blanks).map(([k, v]) => `${k}: ${v}`).join(' · ')}
        </p>
      )}
    </div>
  );
}
