import { useState } from 'react';
import { GripVertical, ChevronUp, ChevronDown } from 'lucide-react';

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export default function Reorder({ content, userAnswer, onChange, result }) {
  const paragraphs = content.paragraphs;
  const byId = Object.fromEntries(paragraphs.map((p) => [p.id, p]));

  const [order, setOrder] = useState(() => userAnswer?.order || shuffle(paragraphs.map((p) => p.id)));
  const [dragIndex, setDragIndex] = useState(null);

  const commit = (next) => {
    setOrder(next);
    onChange({ order: next });
  };

  const move = (index, dir) => {
    const next = [...order];
    const target = index + dir;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    commit(next);
  };

  const onDrop = (index) => {
    if (dragIndex === null || dragIndex === index) return;
    const next = [...order];
    const [moved] = next.splice(dragIndex, 1);
    next.splice(index, 0, moved);
    commit(next);
    setDragIndex(null);
  };

  const correctPairs = new Set(
    (result?.breakdown?.correct_adjacent_pairs || []).map((p) => p.join('>'))
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 6 }}>
        Drag to reorder, or use the arrows. Paragraphs start in random order.
      </p>
      {order.map((id, i) => {
        const p = byId[id];
        const isGoodPairWithNext = i < order.length - 1 && correctPairs.has(`${id}>${order[i + 1]}`);
        return (
          <div
            key={id}
            draggable={!result}
            onDragStart={() => setDragIndex(i)}
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => onDrop(i)}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 10,
              padding: '12px 14px',
              borderRadius: 'var(--radius-sm)',
              border: `1.5px solid ${result ? (isGoodPairWithNext ? 'var(--success)' : 'var(--line)') : 'var(--line)'}`,
              background: 'var(--paper-raised)',
              boxShadow: 'var(--shadow-card)',
            }}
          >
            <GripVertical size={16} color="var(--text-muted)" style={{ marginTop: 2, flexShrink: 0, cursor: 'grab' }} />
            <span style={{ fontSize: 14, color: 'var(--text-primary)', flex: 1, lineHeight: 1.6 }}>{p.text}</span>
            {!result && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 2, flexShrink: 0 }}>
                <button onClick={() => move(i, -1)} style={{ border: 'none', background: 'transparent' }}>
                  <ChevronUp size={16} color="var(--text-secondary)" />
                </button>
                <button onClick={() => move(i, 1)} style={{ border: 'none', background: 'transparent' }}>
                  <ChevronDown size={16} color="var(--text-secondary)" />
                </button>
              </div>
            )}
          </div>
        );
      })}
      {result && (
        <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
          Correct sequence: {result.correct_answer.order.join(' → ')}
        </p>
      )}
    </div>
  );
}
