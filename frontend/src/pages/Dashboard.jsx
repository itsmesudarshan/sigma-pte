import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, CartesianGrid } from 'recharts';
import { api } from '../api/client';
import ScoreGauge from '../components/ScoreGauge';

const TYPE_LABELS = {
  rw_fill_blanks: 'R&W Fill Blanks',
  fill_blanks: 'Fill Blanks',
  reorder: 'Re-order',
  mcq_single: 'MCQ Single',
  mcq_multi: 'MCQ Multi',
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recent, setRecent] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.getStats('guest').then(setStats);
    api.recentlyAttempted('guest').then(setRecent);
  }, []);

  const chartData = stats
    ? Object.entries(stats.by_type).map(([type, v]) => ({
        name: TYPE_LABELS[type] || type,
        accuracy: Math.round(v.average_accuracy * 100),
      }))
    : [];

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 4 }}>Welcome back</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 28 }}>
        Here's how your Reading practice is going so far.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginBottom: 28 }}>
        <div style={{ padding: 20, background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', display: 'flex', alignItems: 'center', gap: 16 }}>
          <ScoreGauge accuracy={stats?.average_accuracy || 0} size={72} />
          <div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600 }}>Overall Accuracy</p>
            <p className="mono" style={{ fontSize: 22, fontWeight: 700, color: 'var(--ink)' }}>
              {Math.round((stats?.average_accuracy || 0) * 100)}%
            </p>
          </div>
        </div>

        <div style={{ padding: 20, background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)' }}>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600, marginBottom: 8 }}>Total Attempts</p>
          <p className="mono" style={{ fontSize: 32, fontWeight: 700, color: 'var(--ink)' }}>{stats?.total_attempts ?? '–'}</p>
        </div>

        <button
          onClick={() => navigate('/reading')}
          style={{
            padding: 20, background: 'var(--ink)', color: '#fff', border: 'none',
            borderRadius: 'var(--radius-lg)', textAlign: 'left', display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
          }}
        >
          <p style={{ fontSize: 14, fontWeight: 700 }}>Start a practice session</p>
          <p style={{ fontSize: 12, opacity: 0.7, marginTop: 6 }}>5 Reading question types available →</p>
        </button>
      </div>

      {chartData.length > 0 && (
        <div style={{ background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', padding: '20px 20px 8px', marginBottom: 28 }}>
          <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--ink)', marginBottom: 12 }}>Accuracy by question type</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--line)" vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: 'var(--text-secondary)' }} />
              <YAxis tick={{ fontSize: 11, fill: 'var(--text-secondary)' }} domain={[0, 100]} />
              <Tooltip formatter={(v) => `${v}%`} />
              <Bar dataKey="accuracy" fill="#2A5CDB" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <div>
        <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--ink)', marginBottom: 12 }}>Recently attempted</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {recent.length === 0 && <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>No attempts yet — start practicing to see history here.</p>}
          {recent.map((q) => (
            <button
              key={q.id}
              onClick={() => navigate(`/practice/${q.id}`)}
              style={{
                textAlign: 'left', padding: '12px 16px', borderRadius: 'var(--radius-md)',
                border: '1px solid var(--line)', background: 'var(--paper-raised)', fontSize: 14,
              }}
            >
              {q.title} <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>· {TYPE_LABELS[q.q_type]}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
