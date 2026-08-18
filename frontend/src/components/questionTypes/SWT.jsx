function countWords(text) {
  return (text.match(/[A-Za-z']+/g) || []).length;
}
function countSentences(text) {
  return text.split(/(?<=[.!?])\s+/).filter((s) => s.trim()).length;
}

export default function SWT({ passage, userAnswer, onChange, result }) {
  const text = userAnswer?.text || '';
  const wordCount = countWords(text);
  const sentenceCount = countSentences(text);
  const inRange = wordCount >= 5 && wordCount <= 75;
  const oneSentence = sentenceCount === 1;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div
        style={{
          padding: 16, background: 'var(--paper)', borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--line)', fontSize: 14, lineHeight: 1.7, color: 'var(--text-primary)',
          maxHeight: 220, overflowY: 'auto',
        }}
      >
        {passage}
      </div>

      <textarea
        disabled={!!result}
        value={text}
        onChange={(e) => onChange({ text: e.target.value })}
        placeholder="Write your one-sentence summary here (5-75 words)..."
        rows={4}
        style={{
          padding: 14, fontSize: 15, lineHeight: 1.6, borderRadius: 'var(--radius-sm)',
          border: `1.5px solid ${result ? 'var(--line)' : (inRange && oneSentence ? 'var(--success)' : 'var(--line-strong)')}`,
          fontFamily: 'var(--font-body)', resize: 'vertical',
          background: result ? 'var(--paper)' : 'var(--paper-raised)',
        }}
      />

      <div style={{ display: 'flex', gap: 16, fontSize: 12 }}>
        <span className="mono" style={{ color: inRange ? 'var(--success)' : 'var(--text-muted)', fontWeight: 700 }}>
          {wordCount} words {!inRange && '(need 5-75)'}
        </span>
        <span className="mono" style={{ color: oneSentence ? 'var(--success)' : 'var(--text-muted)', fontWeight: 700 }}>
          {sentenceCount} sentence{sentenceCount !== 1 ? 's' : ''} {!oneSentence && '(need exactly 1)'}
        </span>
      </div>

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 4 }}>
          <TraitBar label="Content" score={result.breakdown.content} max={result.breakdown.content_max} />
          <TraitBar label="Form" score={result.breakdown.form} max={result.breakdown.form_max} />
          <TraitBar label="Grammar" score={result.breakdown.grammar} max={result.breakdown.grammar_max} />
          <TraitBar label="Vocabulary" score={result.breakdown.vocabulary} max={result.breakdown.vocabulary_max} />
          {result.breakdown.misspelled_words?.length > 0 && (
            <p style={{ fontSize: 12, color: 'var(--error)' }}>
              Possible spelling issues: {result.breakdown.misspelled_words.join(', ')}
            </p>
          )}
          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
            {result.breakdown.ai_assisted ? '✓ AI-assisted scoring (blended with heuristic)' : 'Heuristic scoring (add a free Groq API key for AI-assisted scoring)'}
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
      <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', width: 90, flexShrink: 0 }}>{label}</span>
      <div style={{ flex: 1, height: 6, borderRadius: 999, background: 'var(--line)', overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: 'var(--focus)' }} />
      </div>
      <span className="mono" style={{ fontSize: 12, fontWeight: 700, color: 'var(--ink)', width: 36, textAlign: 'right' }}>
        {score}/{max}
      </span>
    </div>
  );
}
