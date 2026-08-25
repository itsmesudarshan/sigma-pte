import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2 } from 'lucide-react';
import { api } from '../api/client';
import Timer from '../components/Timer';
import ScoreGauge from '../components/ScoreGauge';
import MCQSingle from '../components/questionTypes/MCQSingle';
import MCQMulti from '../components/questionTypes/MCQMulti';
import FillBlanks from '../components/questionTypes/FillBlanks';
import RWFillBlanks from '../components/questionTypes/RWFillBlanks';
import Reorder from '../components/questionTypes/Reorder';
import SWT from '../components/questionTypes/SWT';
import Essay from '../components/questionTypes/Essay';
import ReadAloudSpeaking from '../components/questionTypes/ReadAloudSpeaking';
import AnswerShortQuestion from '../components/questionTypes/AnswerShortQuestion';
import DescribeImage from '../components/questionTypes/DescribeImage';
import ListeningMCQ from '../components/questionTypes/ListeningMCQ';
import ListeningFillBlanks from '../components/questionTypes/ListeningFillBlanks';
import WriteFromDictation from '../components/questionTypes/WriteFromDictation';

const WRITING_TYPES = new Set(['swt', 'essay']);
const SPEAKING_TYPES = new Set(['read_aloud', 'repeat_sentence', 'answer_short_question', 'describe_image']);
const LISTENING_TYPES = new Set(['l_mcq_single', 'l_mcq_multi', 'l_fill_blanks', 'highlight_summary', 'select_missing_word', 'write_from_dictation']);

function renderComponent(question, userAnswer, onChange, result) {
  const { q_type, passage, content } = question;
  switch (q_type) {
    case 'mcq_single': return <MCQSingle content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'mcq_multi': return <MCQMulti content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'fill_blanks': return <FillBlanks passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'rw_fill_blanks': return <RWFillBlanks passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'reorder': return <Reorder content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'swt': return <SWT passage={passage} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'essay': return <Essay passage={passage} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'read_aloud': return <ReadAloudSpeaking passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} isRepeat={false} />;
    case 'describe_image': return <DescribeImage content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'repeat_sentence': return <ReadAloudSpeaking passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} isRepeat={true} />;
    case 'answer_short_question': return <AnswerShortQuestion passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'l_mcq_single':
    case 'l_mcq_multi':
    case 'highlight_summary':
    case 'select_missing_word':
      return <ListeningMCQ content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'l_fill_blanks': return <ListeningFillBlanks passage={passage} content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    case 'write_from_dictation': return <WriteFromDictation content={content} userAnswer={userAnswer} onChange={onChange} result={result} />;
    default: return <p>Unsupported question type: {q_type}</p>;
  }
}

export default function Practice() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [question, setQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState({});
  const [result, setResult] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setQuestion(null);
    setUserAnswer({});
    setResult(null);
    setElapsed(0);
    api.getQuestion(id).then(setQuestion);
  }, [id]);

  if (!question) return <p style={{ color: 'var(--text-muted)' }}>Loading…</p>;

  const isWriting = WRITING_TYPES.has(question.q_type);
  const isSpeaking = SPEAKING_TYPES.has(question.q_type);
  const isListening = LISTENING_TYPES.has(question.q_type);

  const submit = async () => {
    setSubmitting(true);
    try {
      const res = await api.submitAttempt({
        question_id: question.id,
        user_id: 'guest',
        user_answer: userAnswer,
        time_taken_seconds: elapsed,
      });
      setResult(res);
    } finally {
      setSubmitting(false);
    }
  };

  const canSubmit = isWriting || isSpeaking
    ? (userAnswer.text || userAnswer.transcript || '').trim().length > 0
    : Object.keys(userAnswer).length > 0;

  const backHref = isWriting ? `/question-bank?module=writing&q_type=${question.q_type}`
    : isSpeaking ? `/question-bank?module=speaking&q_type=${question.q_type}`
    : isListening ? `/question-bank?module=listening&q_type=${question.q_type}`
    : `/question-bank?module=reading&q_type=${question.q_type}`;

  return (
    <div style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Link to="/question-bank" style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--text-secondary)', fontWeight: 600 }}>
          <ArrowLeft size={15} /> Question Bank
        </Link>
        <Timer running={!result} onTick={setElapsed} />
      </div>

      <h2 style={{ fontSize: 22, marginBottom: 4 }}>{question.title}</h2>
      <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 20, textTransform: 'capitalize' }}>
        {question.difficulty} · {(question.tags || []).join(', ')}
      </p>

      <div style={{ background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', padding: 24, boxShadow: 'var(--shadow-card)' }}>
        {renderComponent(question, userAnswer, setUserAnswer, result)}
      </div>

      {!result ? (
        <button
          onClick={submit}
          disabled={submitting || !canSubmit}
          style={{ marginTop: 20, padding: '12px 28px', borderRadius: 999, border: 'none', background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700, opacity: submitting || !canSubmit ? 0.5 : 1 }}
        >
          {submitting ? 'Scoring…' : 'Submit Answer'}
        </button>
      ) : (
        <div style={{ marginTop: 20, display: 'flex', gap: 20, alignItems: 'center', padding: 20, background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)' }}>
          <ScoreGauge accuracy={result.accuracy} label="Accuracy" />
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <CheckCircle2 size={16} color="var(--success)" />
              <span className="mono" style={{ fontSize: 14, fontWeight: 700 }}>{result.score} / {result.max_score} points</span>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6 }}>{result.explanation}</p>
            <button
              onClick={() => navigate(backHref)}
              style={{ marginTop: 14, padding: '9px 18px', borderRadius: 999, border: '1px solid var(--line-strong)', background: 'var(--paper-raised)', fontSize: 13, fontWeight: 600 }}
            >
              Try another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
