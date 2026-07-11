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

const TYPE_COMPONENTS = {
  mcq_single: MCQSingle,
  mcq_multi: MCQMulti,
  fill_blanks: FillBlanks,
  rw_fill_blanks: RWFillBlanks,
  reorder: Reorder,
};

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

  const Comp = TYPE_COMPONENTS[question.q_type];

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

      <div
        style={{
          background: 'var(--paper-raised)', border: '1px solid var(--line)',
          borderRadius: 'var(--radius-lg)', padding: 24, boxShadow: 'var(--shadow-card)',
        }}
      >
        <Comp
          passage={question.passage}
          content={question.content}
          userAnswer={userAnswer}
          onChange={setUserAnswer}
          result={result}
        />
      </div>

      {!result ? (
        <button
          onClick={submit}
          disabled={submitting}
          style={{
            marginTop: 20, padding: '12px 28px', borderRadius: 999, border: 'none',
            background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700,
            opacity: submitting ? 0.6 : 1,
          }}
        >
          {submitting ? 'Scoring…' : 'Submit Answer'}
        </button>
      ) : (
        <div
          style={{
            marginTop: 20, display: 'flex', gap: 20, alignItems: 'center', padding: 20,
            background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)',
          }}
        >
          <ScoreGauge accuracy={result.accuracy} label="Accuracy" />
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <CheckCircle2 size={16} color="var(--success)" />
              <span className="mono" style={{ fontSize: 14, fontWeight: 700 }}>
                {result.score} / {result.max_score} points
              </span>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6 }}>{result.explanation}</p>
            <button
              onClick={() => navigate(`/question-bank?q_type=${question.q_type}`)}
              style={{
                marginTop: 14, padding: '9px 18px', borderRadius: 999, border: '1px solid var(--line-strong)',
                background: 'var(--paper-raised)', fontSize: 13, fontWeight: 600,
              }}
            >
              Try another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
