function splitPassage(passage) {
  const parts = passage.split(/(\{\d+\})/g);
  return parts.map((part) => {
    const match = part.match(/^\{(\d+)\}$/);
    return match ? { blank: match[1] } : { text: part };
  });
}

export default function RWFillBlanks({ passage, content, userAnswer, onChange, result }) {
  const blanks = userAnswer?.blanks || {};
  const tokens = splitPassage(passage);

  const setBlank = (num, word) => onChange({ blanks: { ...blanks, [num]: word } });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <p style={{ fontSize: 15, lineHeight: 2.1, color: 'var(--ink)' }}>
        {tokens.map((tok, i) => {
          if (tok.text !== undefined) return <span key={i}>{tok.text}</span>;
          const num = tok.blank;
          const perBlank = result?.breakdown?.per_blank?.[num];
          let border = 'var(--line-strong)';
          if (result && perBlank) border = perBlank.is_correct ? 'var(--success)' : 'var(--error)';

          return (
            <select
              key={i}
              disabled={!!result}
              value={blanks[num] || ''}
              onChange={(e) => setBlank(num, e.target.value)}
              className="mono"
              style={{
                margin: '0 4px',
                padding: '4px 8px',
                fontSize: 14,
                fontWeight: 600,
                borderRadius: 6,
                border: `1.5px solid ${border}`,
                background: result ? (perBlank?.is_correct ? 'var(--success-soft)' : 'var(--error-soft)') : 'var(--paper-raised)',
                color: 'var(--ink)',
              }}
            >
              <option value="" disabled>choose...</option>
              {content.dropdown_options[num].map((word) => (
                <option key={word} value={word}>{word}</option>
              ))}
            </select>
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
