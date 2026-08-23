import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const TYPES = [
  { q_type: 'read_aloud', title: 'Read Aloud', desc: 'Read the displayed text aloud clearly and at a natural pace.' },
  { q_type: 'repeat_sentence', title: 'Repeat Sentence', desc: 'Repeat a sentence exactly as heard.' },
  { q_type: 'answer_short_question', title: 'Answer Short Question', desc: 'Answer a short factual question in one or two words.' },
];

export default function Speaking() {
  const [counts, setCounts] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    TYPES.forEach(({ q_type }) => {
      api.listQuestions({ module: 'speaking', q_type }).then((qs) => setCounts((c) => ({ ...c, [q_type]: qs.length })));
    });
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 6 }}>Speaking</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 12 }}>
        Scored on Content, Oral Fluency, and Pronunciation using your browser's built-in speech recognition — free, no installs.
      </p>
      <p style={{ color: 'var(--text-muted)', fontSize: 12, marginBottom: 28 }}>
        Works best in Chrome or Edge. Allow microphone access when prompted.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
        {TYPES.map((t) => (
          <button
            key={t.q_type}
            onClick={() => navigate(`/question-bank?module=speaking&q_type=${t.q_type}`)}
            style={{ textAlign: 'left', padding: 20, borderRadius: 'var(--radius-md)', border: '1px solid var(--line)', background: 'var(--paper-raised)', boxShadow: 'var(--shadow-card)', display: 'flex', flexDirection: 'column', gap: 10 }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <h3 style={{ fontSize: 16 }}>{t.title}</h3>
              <span className="mono" style={{ fontSize: 12, fontWeight: 700, color: 'var(--focus)', background: 'var(--focus-soft)', padding: '2px 8px', borderRadius: 999, flexShrink: 0, marginLeft: 8 }}>
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
