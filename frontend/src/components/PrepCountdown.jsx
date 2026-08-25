import { useEffect, useState } from 'react';

export default function PrepCountdown({ seconds, onComplete, label = 'Preparation time' }) {
  const [remaining, setRemaining] = useState(seconds);

  useEffect(() => {
    setRemaining(seconds);
    if (seconds <= 0) {
      onComplete();
      return;
    }
    const interval = setInterval(() => {
      setRemaining((r) => {
        if (r <= 1) {
          clearInterval(interval);
          onComplete();
          return 0;
        }
        return r - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seconds]);

  const pct = seconds > 0 ? (remaining / seconds) * 100 : 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10, padding: 18, borderRadius: 'var(--radius-md)', background: 'var(--amber-soft)', border: '1px solid var(--amber)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>{label}</span>
        <span className="mono" style={{ fontSize: 20, fontWeight: 700, color: 'var(--amber)' }}>{remaining}s</span>
      </div>
      <div style={{ height: 6, borderRadius: 999, background: 'rgba(226,166,59,0.25)', overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: 'var(--amber)', transition: 'width 1s linear' }} />
      </div>
      <p style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Recording will start automatically when the timer ends.</p>
    </div>
  );
}
