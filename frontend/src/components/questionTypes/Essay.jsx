function countWords(text) {
  return (text.match(/[A-Za-z']+/g) || []).length;
}

export default function Essay({ passage, userAnswer, onChange, result }) {
  const text = userAnswer?.text || '';
  const wordCount = countWords(text);
  const inFullRange = wordCount >= 200 && wordCount <= 300;
  const inPartialRange = (wordCount >= 120 && wordCount < 200) || (wordCount > 300 && wordCount <= 380);

  let counterColor = 'var(--text-muted)';
  if (inFullRange) counterColor = 'var(--success)';
  else if (inPartialRange) counterColor = 'var(--amber)';
  else if (wordCount > 0) counterColor = 'var(--error)';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div
        style={{
          padding: 16, background: 'var(--paper)', borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--line)', fontSize: 14, lineHeight: 1.7, color: 'var(--text-primary)',
        }}
      >
        {passage}
      </div>

      <textarea
        disabled={!!result}
        value={text}
        onChange={(e) => onChange({ text: e.target.value })}
        placeholder="Write your essay here. Aim for 200-300 words across 4 clear paragraphs: introduction, two body paragraphs, and a conclusion..."
        rows={14}
        style={{
          padding: 14, fontSize: 15, lineHeight: 1.7, borderRadius: 'var(--radius-sm)',
          border: `1.5px solid ${result ? 'var(--line)' : 'var(--line-strong)'}`,
          fontFamily: 'var(--font-body)', resize: 'vertical',
          background: result ? 'var(--paper)' : 'var(--paper-raised)',
        }}
      />

      <span className="mono" style={{ fontSize: 12, fontWeight: 700, color: counterColor }}>
        {wordCount} words {inFullRange ? '(full Form marks range)' : '(target: 200-300)'}
      </span>

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 4 }}>
          <TraitBar label="Content" score={result.breakdown.content} max={result.breakdown.content_max} />
          <TraitBar label="Form" score={result.breakdown.form} max={result.breakdown.form_max} />
          <TraitBar label="Dev./Structure" score={result.breakdown.dsc} max={result.breakdown.dsc_max} />
          <TraitBar label="Grammar" score={result.breakdown.grammar} max={result.breakdown.grammar_max} />
          <TraitBar label="Linguistic Range" score={result.breakdown.linguistic_range} max={result.breakdown.linguistic_range_max} />
          <TraitBar label="Vocabulary" score={result.breakdown.vocabulary} max={result.breakdown.vocabulary_max} />
          <TraitBar label="Spelling" score={result.breakdown.spelling} max={result.breakdown.spelling_max} />
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
      <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', width: 110, flexShrink: 0 }}>{label}</span>
      <div style={{ flex: 1, height: 6, borderRadius: 999, background: 'var(--line)', overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: 'var(--focus)' }} />
      </div>
      <span className="mono" style={{ fontSize: 12, fontWeight: 700, color: 'var(--ink)', width: 36, textAlign: 'right' }}>
        {score}/{max}
      </span>
    </div>
  );
}
