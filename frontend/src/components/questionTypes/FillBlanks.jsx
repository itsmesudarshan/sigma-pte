function splitPassage(passage) {
  const parts = passage.split(/(\{\d+\})/g);
  return parts.map((part) => {
    const match = part.match(/^\{(\d+)\}$/);
    return match ? { blank: match[1] } : { text: part };
  });
}

export default function FillBlanks({ passage, content, userAnswer, onChange, result }) {
  const blanks = userAnswer?.blanks || {};
  const tokens = splitPassage(passage);
  const usedWords = new Set(Object.values(blanks));

  const setBlank = (num, word) => {
    onChange({ blanks: { ...blanks, [num]: word } });
  };

  const clearBlank = (num) => {
    const next = { ...blanks };
    delete next[num];
    onChange({ blanks: next });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <p style={{ fontSize: 15, lineHeight: 1.9, color: 'var(--ink)' }}>
        {tokens.map((tok, i) => {
          if (tok.text !== undefined) return <span key={i}>{tok.text}</span>;
          const num = tok.blank;
          const filled = blanks[num];
          const perBlank = result?.breakdown?.per_blank?.[num];
          let border = 'var(--line-strong)';
          let bg = 'var(--paper-raised)';
          if (result && perBlank) {
            border = perBlank.is_correct ? 'var(--success)' : 'var(--error)';
            bg = perBlank.is_correct ? 'var(--success-soft)' : 'var(--error-soft)';
          }
          return (
            <button
              key={i}
              disabled={!!result}
              onClick={() => filled && clearBlank(num)}
              className="mono"
              style={{
                display: 'inline-flex',
                minWidth: 90,
                padding: '2px 10px',
                margin: '0 3px',
                borderRadius: 6,
                border: `1.5px dashed ${border}`,
                background: bg,
                fontSize: 14,
                fontWeight: 600,
                color: filled ? 'var(--ink)' : 'var(--text-muted)',
                verticalAlign: 'baseline',
              }}
            >
              {filled || `blank ${num}`}
            </button>
          );
        })}
      </p>

      {result && (
        <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          Correct answers: {Object.entries(result.correct_answer.blanks).map(([k, v]) => `${k}: ${v}`).join(' · ')}
        </p>
      )}

      <div>
        <p style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
          Word bank
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          {content.word_bank.map((word) => {
            const isUsed = usedWords.has(word);
            const nextEmptyBlank = Array.from({ length: content.blank_count }, (_, i) => String(i + 1)).find(
              (n) => !blanks[n]
            );
            return (
              <button
                key={word}
                disabled={!!result || isUsed || !nextEmptyBlank}
                onClick={() => nextEmptyBlank && setBlank(nextEmptyBlank, word)}
                style={{
                  padding: '8px 14px',
                  borderRadius: 999,
                  border: '1px solid var(--line-strong)',
                  background: isUsed ? 'var(--line)' : 'var(--paper-raised)',
                  color: isUsed ? 'var(--text-muted)' : 'var(--text-primary)',
                  fontSize: 13,
                  fontWeight: 600,
                  opacity: isUsed ? 0.5 : 1,
                }}
              >
                {word}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
