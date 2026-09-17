export default function MCQSingle({ passage, content, userAnswer, onChange, result }) {
  const selected = userAnswer?.option;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {passage && (
        <div
          style={{
            padding: 16, background: 'var(--paper)', borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--line)', fontSize: 14, lineHeight: 1.7, color: 'var(--text-primary)',
            maxHeight: 260, overflowY: 'auto',
          }}
        >
          {passage}
        </div>
      )}

      <p style={{ fontSize: 15, fontWeight: 600, color: 'var(--ink)', marginBottom: 4 }}>
        {content.question}
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {content.options.map((opt) => {
          const isSelected = selected === opt.id;
          const isCorrect = result && result.breakdown?.correct === opt.id;
          const isWrongPick = result && isSelected && !isCorrect;

          let bg = 'var(--paper-raised)';
          let border = 'var(--line)';
          if (result) {
            if (isCorrect) { bg = 'var(--success-soft)'; border = 'var(--success)'; }
            else if (isWrongPick) { bg = 'var(--error-soft)'; border = 'var(--error)'; }
          } else if (isSelected) {
            bg = 'var(--focus-soft)'; border = 'var(--focus)';
          }

          return (
            <button
              key={opt.id}
              disabled={!!result}
              onClick={() => onChange({ option: opt.id })}
              style={{
                textAlign: 'left', padding: '12px 14px', borderRadius: 'var(--radius-sm)',
                border: `1.5px solid ${border}`, background: bg, fontSize: 14,
                color: 'var(--text-primary)', display: 'flex', gap: 10,
              }}
            >
              <span style={{ fontWeight: 700, color: 'var(--text-secondary)' }}>{opt.id}</span>
              {opt.text}
            </button>
          );
        })}
      </div>
    </div>
  );
}
