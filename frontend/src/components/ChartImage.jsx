export default function ChartImage({ type, data, title }) {
  const width = 480;
  const height = 300;
  const padding = 48;

  const colors = ['#2A5CDB', '#2F9E5B', '#E2A63B', '#D64545', '#8B5CF6', '#14B8A6'];

  if (type === 'bar') {
    const maxVal = Math.max(...data.map((d) => d.value));
    const barWidth = (width - padding * 2) / data.length - 16;
    return (
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ background: '#fff', borderRadius: 8 }}>
        {title && <text x={width / 2} y={22} textAnchor="middle" fontSize="14" fontWeight="700" fill="#14213D">{title}</text>}
        {data.map((d, i) => {
          const barHeight = (d.value / maxVal) * (height - padding - 50);
          const x = padding + i * ((width - padding * 2) / data.length) + 8;
          const y = height - padding - barHeight;
          return (
            <g key={i}>
              <rect x={x} y={y} width={barWidth} height={barHeight} fill={colors[i % colors.length]} rx={3} />
              <text x={x + barWidth / 2} y={y - 6} textAnchor="middle" fontSize="12" fontWeight="700" fill="#14213D">{d.value}</text>
              <text x={x + barWidth / 2} y={height - padding + 18} textAnchor="middle" fontSize="11" fill="#5B6472">{d.label}</text>
            </g>
          );
        })}
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#CCC7B8" strokeWidth="1.5" />
      </svg>
    );
  }

  if (type === 'line') {
    const maxVal = Math.max(...data.map((d) => d.value));
    const stepX = (width - padding * 2) / (data.length - 1);
    const points = data.map((d, i) => {
      const x = padding + i * stepX;
      const y = height - padding - (d.value / maxVal) * (height - padding - 50);
      return { x, y, ...d };
    });
    const pathD = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
    return (
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ background: '#fff', borderRadius: 8 }}>
        {title && <text x={width / 2} y={22} textAnchor="middle" fontSize="14" fontWeight="700" fill="#14213D">{title}</text>}
        <path d={pathD} fill="none" stroke="#2A5CDB" strokeWidth="2.5" />
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="4" fill="#2A5CDB" />
            <text x={p.x} y={p.y - 12} textAnchor="middle" fontSize="12" fontWeight="700" fill="#14213D">{p.value}</text>
            <text x={p.x} y={height - padding + 18} textAnchor="middle" fontSize="11" fill="#5B6472">{p.label}</text>
          </g>
        ))}
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#CCC7B8" strokeWidth="1.5" />
      </svg>
    );
  }

  if (type === 'pie') {
    const total = data.reduce((sum, d) => sum + d.value, 0);
    const cx = width / 2;
    const cy = height / 2 + 10;
    const r = 90;
    let angleStart = -90;
    const slices = data.map((d, i) => {
      const angle = (d.value / total) * 360;
      const angleEnd = angleStart + angle;
      const largeArc = angle > 180 ? 1 : 0;
      const x1 = cx + r * Math.cos((Math.PI * angleStart) / 180);
      const y1 = cy + r * Math.sin((Math.PI * angleStart) / 180);
      const x2 = cx + r * Math.cos((Math.PI * angleEnd) / 180);
      const y2 = cy + r * Math.sin((Math.PI * angleEnd) / 180);
      const path = `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} Z`;
      const midAngle = (angleStart + angleEnd) / 2;
      const labelX = cx + (r + 28) * Math.cos((Math.PI * midAngle) / 180);
      const labelY = cy + (r + 28) * Math.sin((Math.PI * midAngle) / 180);
      angleStart = angleEnd;
      return { path, color: colors[i % colors.length], labelX, labelY, ...d, pct: Math.round((d.value / total) * 100) };
    });
    return (
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ background: '#fff', borderRadius: 8 }}>
        {title && <text x={width / 2} y={22} textAnchor="middle" fontSize="14" fontWeight="700" fill="#14213D">{title}</text>}
        {slices.map((s, i) => <path key={i} d={s.path} fill={s.color} stroke="#fff" strokeWidth="2" />)}
        {slices.map((s, i) => (
          <text key={i} x={s.labelX} y={s.labelY} textAnchor="middle" fontSize="11" fontWeight="700" fill="#14213D">{s.label} ({s.pct}%)</text>
        ))}
      </svg>
    );
  }

  return null;
}
