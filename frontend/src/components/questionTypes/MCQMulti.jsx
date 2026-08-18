export default function MCQMulti({ content, userAnswer, onChange, result }) {
  const selected = new Set(userAnswer?.options || []);

  const toggle = (id) => {
    const next = new Set(selected);
    next.has(id) ? next.delete(id) : next.add(id);
    onChange({ options: Array.from(next) });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <p style={{ fontSize: 15, fontWeight: 600, color: 'var(--ink)', marginBottom: 4 }}>
        {content.question}
      </p>
      {content.options.map((opt) => {
        const isSelected = selected.has(opt.id);
        const correctSet = new Set(result?.breakdown?.correct_selected || []);
        const incorrectSet = new Set(result?.breakdown?.incorrect_selected || []);
        const missedSet = new Set(result?.breakdown?.missed || []);

        let bg = 'var(--paper-raised)';
        let border = 'var(--line)';
        if (result) {
          if (correctSet.has(opt.id)) { bg = 'var(--success-soft)'; border = 'var(--success)'; }
          else if (incorrectSet.has(opt.id)) { bg = 'var(--error-soft)'; border = 'var(--error)'; }
          else if (missedSet.has(opt.id)) { bg = 'var(--amber-soft)'; border = 'var(--amber)'; }
        } else if (isSelected) {
          bg = 'var(--focus-soft)'; border = 'var(--focus)';
        }

        return (
          <button
            key={opt.id}
            disabled={!!result}
            onClick={() => toggle(opt.id)}
            style={{
              textAlign: 'left',
              padding: '12px 14px',
              borderRadius: 'var(--radius-sm)',
              border: `1.5px solid ${border}`,
              background: bg,
              fontSize: 14,
              display: 'flex',
              gap: 10,
              alignItems: 'center',
            }}
          >
            <span
              style={{
                width: 16, height: 16, borderRadius: 4,
                border: `1.5px solid ${isSelected ? 'var(--focus)' : 'var(--line-strong)'}`,
                background: isSelected ? 'var(--focus)' : 'transparent',
                flexShrink: 0,
              }}
            />
            <span style={{ fontWeight: 700, color: 'var(--text-secondary)' }}>{opt.id}</span>
            {opt.text}
          </button>
        );
      })}
      {result && (
        <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
          Green = correct pick · Red = incorrect pick (−1 point) · Amber = missed correct answer
        </p>
      )}
    </div>
  );
}
