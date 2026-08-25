import { useState } from 'react';
import TTSPlayer from '../TTSPlayer';
import SpeechRecorder from '../SpeechRecorder';

export default function AnswerShortQuestion({ passage, content, onChange, result }) {
  const [audioDone, setAudioDone] = useState(false);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ padding: 18, background: 'var(--paper)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line)', fontSize: 16, lineHeight: 1.6, color: 'var(--ink)', fontWeight: 600 }}>
        {passage}
      </div>

      <TTSPlayer text={passage} rate={1} autoPlay onEnd={() => setAudioDone(true)} />

      {!result && !audioDone && (
        <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>Recording will start automatically once the question finishes playing.</p>
      )}

      {(audioDone || result) && (
        <SpeechRecorder
          disabled={!!result}
          autoStart={audioDone && !result}
          autoStopSeconds={content.record_seconds || 10}
          onResult={onChange}
        />
      )}

      {result && (
        <div style={{ padding: 14, borderRadius: 'var(--radius-sm)', background: result.breakdown.is_correct ? 'var(--success-soft)' : 'var(--error-soft)', border: `1px solid ${result.breakdown.is_correct ? 'var(--success)' : 'var(--error)'}` }}>
          <p style={{ fontSize: 13, fontWeight: 700, color: result.breakdown.is_correct ? 'var(--success)' : 'var(--error)' }}>
            {result.breakdown.is_correct ? 'Correct' : 'Not quite'}
          </p>
        </div>
      )}
    </div>
  );
}
