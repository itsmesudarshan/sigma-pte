import { useEffect, useRef, useState } from 'react';
import { Mic, Square, RotateCcw } from 'lucide-react';

const SpeechRecognitionAPI = typeof window !== 'undefined'
  ? (window.SpeechRecognition || window.webkitSpeechRecognition)
  : null;

export default function SpeechRecorder({ onResult, disabled, autoStopSeconds = 30, autoStart = false }) {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [supported] = useState(!!SpeechRecognitionAPI);
  const recognitionRef = useRef(null);
  const transcriptRef = useRef('');
  const confidenceSumRef = useRef(0);
  const confidenceCountRef = useRef(0);
  const startTimeRef = useRef(null);
  const timeoutRef = useRef(null);
  const hasAutoStartedRef = useRef(false);

  useEffect(() => {
    if (!SpeechRecognitionAPI) return;
    const recognition = new SpeechRecognitionAPI();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let combined = '';
      for (let i = 0; i < event.results.length; i++) {
        combined += event.results[i][0].transcript;
        // Chrome/Edge expose a per-result confidence (0-1) on final results —
        // a genuine speech-recognition confidence signal, not a guess.
        if (event.results[i].isFinal && typeof event.results[i][0].confidence === 'number' && event.results[i][0].confidence > 0) {
          confidenceSumRef.current += event.results[i][0].confidence;
          confidenceCountRef.current += 1;
        }
      }
      transcriptRef.current = combined.trim();
      setTranscript(combined.trim());
    };

    recognition.onerror = () => setRecording(false);
    recognition.onend = () => setRecording(false);

    recognitionRef.current = recognition;
    return () => recognition.stop();
  }, []);

  const start = () => {
    if (!recognitionRef.current || disabled) return;
    transcriptRef.current = '';
    setTranscript('');
    confidenceSumRef.current = 0;
    confidenceCountRef.current = 0;
    startTimeRef.current = Date.now();
    recognitionRef.current.start();
    setRecording(true);
    timeoutRef.current = setTimeout(() => stop(), autoStopSeconds * 1000);
  };

  const stop = () => {
    if (!recognitionRef.current) return;
    recognitionRef.current.stop();
    setRecording(false);
    clearTimeout(timeoutRef.current);
    const durationSeconds = startTimeRef.current ? (Date.now() - startTimeRef.current) / 1000 : 0;
    const avgConfidence = confidenceCountRef.current > 0 ? confidenceSumRef.current / confidenceCountRef.current : null;
    onResult({ transcript: transcriptRef.current, duration_seconds: Math.round(durationSeconds), confidence: avgConfidence });
  };

  const reset = () => {
    transcriptRef.current = '';
    setTranscript('');
    onResult({ transcript: '', duration_seconds: 0 });
  };

  useEffect(() => {
    if (autoStart && supported && !disabled && !hasAutoStartedRef.current) {
      hasAutoStartedRef.current = true;
      start();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoStart, supported, disabled]);

  if (!supported) {
    return (
      <div style={{ padding: 16, borderRadius: 'var(--radius-sm)', background: 'var(--amber-soft)', border: '1px solid var(--amber)', fontSize: 13, color: 'var(--text-primary)' }}>
        Your browser doesn't support speech recognition. Try Chrome or Edge for the Speaking module.
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        {!recording ? (
          <button
            onClick={start}
            disabled={disabled}
            style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 20px', borderRadius: 999, border: 'none', background: disabled ? 'var(--line-strong)' : 'var(--error)', color: '#fff', fontSize: 13, fontWeight: 700 }}
          >
            <Mic size={16} /> {transcript ? 'Record Again' : 'Start Recording'}
          </button>
        ) : (
          <button onClick={stop} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 20px', borderRadius: 999, border: 'none', background: 'var(--ink)', color: '#fff', fontSize: 13, fontWeight: 700 }}>
            <Square size={14} fill="#fff" /> Stop
          </button>
        )}
        {transcript && !recording && (
          <button onClick={reset} style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '10px 14px', borderRadius: 999, border: '1px solid var(--line-strong)', background: 'var(--paper-raised)', fontSize: 13, fontWeight: 600 }}>
            <RotateCcw size={14} /> Clear
          </button>
        )}
        {recording && (
          <span style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--error)', fontWeight: 700 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--error)', animation: 'pulse 1s infinite' }} />
            Listening...
          </span>
        )}
      </div>

      <div style={{ minHeight: 60, padding: 14, borderRadius: 'var(--radius-sm)', border: '1px solid var(--line)', background: 'var(--paper)', fontSize: 14, color: transcript ? 'var(--text-primary)' : 'var(--text-muted)' }}>
        {transcript || 'Your speech will be transcribed here as you talk...'}
      </div>

      <style>{`@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }`}</style>
    </div>
  );
}
