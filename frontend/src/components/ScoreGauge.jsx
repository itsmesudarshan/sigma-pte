export default function ScoreGauge({ accuracy = 0, size = 96, label }) {
  const pct = Math.round(accuracy * 100);
  const radius = size / 2 - 6;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - accuracy);

  const color = pct >= 75 ? 'var(--success)' : pct >= 45 ? 'var(--amber)' : 'var(--error)';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="var(--line)" strokeWidth={7} />
        <circle
          cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={color} strokeWidth={7}
          strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
        <text x="50%" y="50%" textAnchor="middle" dominantBaseline="central" fontFamily="var(--font-mono)" fontWeight="700" fontSize={size * 0.24} fill="var(--ink)">
          {pct}%
        </text>
      </svg>
      {label && <span style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 600 }}>{label}</span>}
    </div>
  );
}
