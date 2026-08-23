import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const TYPES = [
  { q_type: 'l_mcq_single', title: 'Multiple Choice', desc: 'Listen to the audio, then choose the correct answer.' },
  { q_type: 'l_fill_blanks', title: 'Fill in the Blanks', desc: 'Type the missing words as you hear them.' },
  { q_type: 'select_missing_word', title: 'Select Missing Word', desc: 'Choose the word that completes the recording.' },
  { q_type: 'write_from_dictation', title: 'Write From Dictation', desc: 'Type the sentence exactly as heard, word for word.' },
];

export default function Listening() {
  const [counts, setCounts] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    TYPES.forEach(({ q_type }) => {
      api.listQuestions({ module: 'listening', q_type }).then((qs) => setCounts((c) => ({ ...c, [q_type]: qs.length })));
    });
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 6 }}>Listening</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 28 }}>
        Audio prompts, scored using the same official partial-credit rules as Reading.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
        {TYPES.map((t) => (
          <button
            key={t.q_type}
            onClick={() => navigate(`/question-bank?module=listening&q_type=${t.q_type}`)}
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
