import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const TYPES = [
  { q_type: 'swt', title: 'Summarize Written Text', desc: 'Read a passage, summarize it in one sentence (5-75 words).' },
  { q_type: 'essay', title: 'Write Essay', desc: 'Respond to a prompt with a 200-300 word argumentative essay.' },
];

export default function Writing() {
  const [counts, setCounts] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    TYPES.forEach(({ q_type }) => {
      api.listQuestions({ module: 'writing', q_type }).then((qs) =>
        setCounts((c) => ({ ...c, [q_type]: qs.length }))
      );
    });
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 6 }}>Writing</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 28 }}>
        Scored on Pearson's official criteria — Content, Form, Grammar, and Vocabulary/Structure,
        with AI-assisted judgment for the semantic traits when available.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
        {TYPES.map((t) => (
          <button
            key={t.q_type}
            onClick={() => navigate(`/question-bank?module=writing&q_type=${t.q_type}`)}
            style={{
              textAlign: 'left',
              padding: 20,
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--line)',
              background: 'var(--paper-raised)',
              boxShadow: 'var(--shadow-card)',
              display: 'flex',
              flexDirection: 'column',
              gap: 10,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <h3 style={{ fontSize: 16 }}>{t.title}</h3>
              <span
                className="mono"
                style={{
                  fontSize: 12, fontWeight: 700, color: 'var(--focus)',
                  background: 'var(--focus-soft)', padding: '2px 8px', borderRadius: 999, flexShrink: 0, marginLeft: 8,
                }}
              >
                {counts[t.q_type] ?? '–'}
              </span>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>{t.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
