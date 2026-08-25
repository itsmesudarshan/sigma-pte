import { useEffect, useRef, useState } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';

export default function TTSPlayer({ text, rate = 0.95, autoPlay = false, onEnd }) {
  const [playing, setPlaying] = useState(false);
  const [hasPlayed, setHasPlayed] = useState(false);
  const [supported] = useState(typeof window !== 'undefined' && 'speechSynthesis' in window);
  const hasAutoPlayedRef = useRef(false);

  useEffect(() => {
    return () => window.speechSynthesis?.cancel();
  }, []);

  const play = () => {
    if (!supported) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.lang = 'en-US';
    utterance.onstart = () => { setPlaying(true); setHasPlayed(true); };
    utterance.onend = () => { setPlaying(false); onEnd?.(); };
    utterance.onerror = () => { setPlaying(false); onEnd?.(); };
    window.speechSynthesis.speak(utterance);
  };

  const pause = () => {
    window.speechSynthesis.pause();
    setPlaying(false);
  };

  useEffect(() => {
    if (autoPlay && supported && !hasAutoPlayedRef.current) {
      hasAutoPlayedRef.current = true;
      play();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoPlay, supported]);

  if (!supported) {
    return (
      <div style={{ padding: 16, borderRadius: 'var(--radius-sm)', background: 'var(--amber-soft)', border: '1px solid var(--amber)', fontSize: 13 }}>
        Your browser doesn't support text-to-speech. Try Chrome or Edge.
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 16, borderRadius: 'var(--radius-md)', background: 'var(--ink)', color: '#fff' }}>
      <button
        onClick={playing ? pause : play}
        style={{ width: 40, height: 40, borderRadius: '50%', border: 'none', background: 'rgba(255,255,255,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', flexShrink: 0 }}
      >
        {playing ? <Pause size={18} fill="#fff" /> : <Play size={18} fill="#fff" style={{ marginLeft: 2 }} />}
      </button>
      <div style={{ flex: 1 }}>
        <p style={{ fontSize: 13, fontWeight: 600 }}>{playing ? 'Playing...' : hasPlayed ? 'Finished' : 'Tap play to listen'}</p>
        <p style={{ fontSize: 11, opacity: 0.6 }}>Text-to-speech audio prompt</p>
      </div>
      {hasPlayed && !playing && (
        <button onClick={play} style={{ background: 'none', border: 'none', color: '#fff', opacity: 0.7, padding: 6 }}>
          <RotateCcw size={16} />
        </button>
      )}
    </div>
  );
}
