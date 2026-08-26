import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, RotateCcw } from 'lucide-react';
import { api } from '../api/client';
import ScoreGauge from '../components/ScoreGauge';
import { renderQuestionComponent, canSubmitAnswer } from '../lib/questionRenderer';

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const MODULE_LABELS = { reading: 'Reading', writing: 'Writing', speaking: 'Speaking', listening: 'Listening' };

async function buildQuestionSet(scope) {
  if (scope === 'full') {
    const modules = ['reading', 'writing', 'speaking', 'listening'];
    const perModule = await Promise.all(
      modules.map((m) => api.listQuestions({ module: m }).then((qs) => shuffle(qs).slice(0, 2)))
    );
    return shuffle(perModule.flat());
  }
  const count = scope === 'writing' ? 3 : 5;
  const qs = await api.listQuestions({ module: scope });
  return shuffle(qs).slice(0, count);
}

export default function MockTestRunner() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const scope = searchParams.get('scope') || 'full';

  const [questions, setQuestions] = useState(null);
  const [index, setIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState({});
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState([]);
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    buildQuestionSet(scope).then(setQuestions);
  }, [scope]);

  if (!questions) return <p style={{ color: 'var(--text-muted)' }}>Preparing your test…</p>;
  if (questions.length === 0) return <p style={{ color: 'var(--text-muted)' }}>No questions available for this test yet.</p>;

  if (finished) {
    const totalScore = results.reduce((s, r) => s + r.score, 0);
    const totalMax = results.reduce((s, r) => s + r.max_score, 0);
    const overallAccuracy = totalMax ? totalScore / totalMax : 0;

    return (
      <div style={{ maxWidth: 700 }}>
        <h1 style={{ fontSize: 26, marginBottom: 20 }}>Test Complete</h1>

        <div style={{ display: 'flex', gap: 24, alignItems: 'center', padding: 24, background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', marginBottom: 24 }}>
          <ScoreGauge accuracy={overallAccuracy} size={100} label="Overall" />
          <div>
            <p className="mono" style={{ fontSize: 26, fontWeight: 700, color: 'var(--ink)' }}>{totalScore} / {totalMax}</p>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{results.length} questions completed</p>
          </div>
        </div>

        <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 12 }}>
          Question breakdown
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 24 }}>
          {results.map((r, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--line)', background: 'var(--paper-raised)' }}>
              <div>
                <span className="mono" style={{ fontSize: 11, fontWeight: 700, color: 'var(--focus)', background: 'var(--focus-soft)', padding: '2px 7px', borderRadius: 999, marginRight: 8 }}>
                  {MODULE_LABELS[r.module]}
                </span>
                <span style={{ fontSize: 14 }}>{r.title}</span>
              </div>
              <span className="mono" style={{ fontSize: 13, fontWeight: 700, color: 'var(--ink)' }}>{r.score}/{r.max_score}</span>
            </div>
          ))}
        </div>

        <div style={{ display: 'flex', gap: 10 }}>
          <button onClick={() => navigate('/mock-test')} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '12px 24px', borderRadius: 999, border: 'none', background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700 }}>
            <RotateCcw size={15} /> Take another test
          </button>
          <button onClick={() => navigate('/')} style={{ padding: '12px 24px', borderRadius: 999, border: '1px solid var(--line-strong)', background: 'var(--paper-raised)', fontSize: 14, fontWeight: 600 }}>
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const question = questions[index];
  const isLast = index === questions.length - 1;

  const submit = async () => {
    setSubmitting(true);
    try {
      const res = await api.submitAttempt({
        question_id: question.id,
        user_id: 'guest',
        user_answer: userAnswer,
        time_taken_seconds: 0,
      });
      setResult(res);
      setResults((prev) => [...prev, { module: question.module, title: question.title, score: res.score, max_score: res.max_score }]);
    } finally {
      setSubmitting(false);
    }
  };

  const next = () => {
    if (isLast) {
      setFinished(true);
      return;
    }
    setIndex((i) => i + 1);
    setUserAnswer({});
    setResult(null);
  };

  return (
    <div style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Link to="/mock-test" style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--text-secondary)', fontWeight: 600 }}>
          <ArrowLeft size={15} /> Exit test
        </Link>
        <span className="mono" style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-secondary)' }}>
          Question {index + 1} of {questions.length}
        </span>
      </div>

      <div style={{ height: 4, borderRadius: 999, background: 'var(--line)', marginBottom: 20, overflow: 'hidden' }}>
        <div style={{ width: `${((index + (result ? 1 : 0)) / questions.length) * 100}%`, height: '100%', background: 'var(--focus)', transition: 'width 0.3s ease' }} />
      </div>

      <h2 style={{ fontSize: 22, marginBottom: 4 }}>{question.title}</h2>
      <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 20, textTransform: 'capitalize' }}>
        {MODULE_LABELS[question.module]} · {question.difficulty}
      </p>

      <div style={{ background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', padding: 24, boxShadow: 'var(--shadow-card)' }}>
        {renderQuestionComponent(question, userAnswer, setUserAnswer, result)}
      </div>

      {!result ? (
        <button
          onClick={submit}
          disabled={submitting || !canSubmitAnswer(question.q_type, userAnswer)}
          style={{ marginTop: 20, padding: '12px 28px', borderRadius: 999, border: 'none', background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700, opacity: submitting || !canSubmitAnswer(question.q_type, userAnswer) ? 0.5 : 1 }}
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
              onClick={next}
              style={{ marginTop: 14, padding: '9px 18px', borderRadius: 999, border: 'none', background: 'var(--ink)', color: '#fff', fontSize: 13, fontWeight: 700 }}
            >
              {isLast ? 'Finish Test' : 'Next Question'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
