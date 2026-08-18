import { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';

export default function Timer({ seconds = 0, running = true, onTick }) {
  const [elapsed, setElapsed] = useState(seconds);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => {
      setElapsed((e) => {
        const next = e + 1;
        onTick?.(next);
        return next;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [running]);

  const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const secs = String(elapsed % 60).padStart(2, '0');

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '6px 12px', borderRadius: 999, background: 'var(--paper-raised)', border: '1px solid var(--line)' }}>
      <Clock size={14} color="var(--text-secondary)" />
      <span className="mono" style={{ fontSize: 13, fontWeight: 700, color: 'var(--ink)' }}>{mins}:{secs}</span>
    </div>
  );
}
