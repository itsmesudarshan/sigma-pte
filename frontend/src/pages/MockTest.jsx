import { useNavigate } from 'react-router-dom';
import { BookOpen, PenLine, Mic, Headphones, Layers } from 'lucide-react';

const SECTIONS = [
  { module: 'reading', label: 'Reading Test', desc: '5 questions across all Reading types.', icon: BookOpen, color: 'var(--ink)' },
  { module: 'writing', label: 'Writing Test', desc: '3 questions: Summarize Text and Essay.', icon: PenLine, color: 'var(--focus)' },
  { module: 'speaking', label: 'Speaking Test', desc: '5 questions across all Speaking types.', icon: Mic, color: 'var(--success)' },
  { module: 'listening', label: 'Listening Test', desc: '5 questions across all Listening types.', icon: Headphones, color: 'var(--amber)' },
];

export default function MockTest() {
  const navigate = useNavigate();

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 6 }}>Mock Test</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 28 }}>
        Take a timed, sequential test — either a full-length mock or a single-section test — and get a score report at the end.
      </p>

      <button
        onClick={() => navigate('/mock-test/run?scope=full')}
        style={{
          width: '100%', textAlign: 'left', padding: 24, borderRadius: 'var(--radius-lg)', border: 'none',
          background: 'var(--ink)', color: '#fff', display: 'flex', alignItems: 'center', gap: 16, marginBottom: 24,
        }}
      >
        <div style={{ width: 48, height: 48, borderRadius: 12, background: 'rgba(255,255,255,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <Layers size={22} />
        </div>
        <div>
          <p style={{ fontSize: 16, fontWeight: 700 }}>Full Mock Test</p>
          <p style={{ fontSize: 13, opacity: 0.75, marginTop: 2 }}>2 questions from each section — Reading, Writing, Speaking, and Listening. ~8 questions total.</p>
        </div>
      </button>

      <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 12 }}>
        Or test one section
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 16 }}>
        {SECTIONS.map((s) => (
          <button
            key={s.module}
            onClick={() => navigate(`/mock-test/run?scope=${s.module}`)}
            style={{ textAlign: 'left', padding: 20, borderRadius: 'var(--radius-md)', border: '1px solid var(--line)', background: 'var(--paper-raised)', boxShadow: 'var(--shadow-card)', display: 'flex', flexDirection: 'column', gap: 10 }}
          >
            <div style={{ width: 36, height: 36, borderRadius: 10, background: s.color, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <s.icon size={18} color="#fff" />
            </div>
            <h3 style={{ fontSize: 16 }}>{s.label}</h3>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>{s.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
