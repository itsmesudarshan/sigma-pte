import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Search, Star, ArrowRight } from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

const TYPE_LABELS = {
  rw_fill_blanks: 'R&W Fill in the Blanks',
  fill_blanks: 'Fill in the Blanks',
  reorder: 'Re-order Paragraphs',
  mcq_single: 'MCQ (Single)',
  mcq_multi: 'MCQ (Multiple)',
  swt: 'Summarize Written Text',
  essay: 'Write Essay',
  read_aloud: 'Read Aloud',
  repeat_sentence: 'Repeat Sentence',
  answer_short_question: 'Answer Short Question',
  describe_image: 'Describe Image',
  l_mcq_single: 'Listening MCQ',
  l_mcq_multi: 'Listening MCQ (Multiple)',
  l_fill_blanks: 'Listening Fill in the Blanks',
  highlight_summary: 'Highlight Correct Summary',
  select_missing_word: 'Select Missing Word',
  write_from_dictation: 'Write From Dictation',
};

export default function QuestionBank() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [questions, setQuestions] = useState([]);
  const [search, setSearch] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const { user } = useAuth();
  const [favoritesOnly, setFavoritesOnly] = useState(false);
  const [favIds, setFavIds] = useState(new Set());
  const navigate = useNavigate();

  const q_type = searchParams.get('q_type') || '';
  const module = searchParams.get('module') || '';

  const load = () => {
    api.listQuestions({
      module: module || undefined,
      q_type: q_type || undefined,
      difficulty: difficulty || undefined,
      search: search || undefined,
      favorites_only: favoritesOnly || undefined,
      user_id: user.email,
    }).then(setQuestions);
  };

  useEffect(() => { load(); }, [q_type, module, difficulty, favoritesOnly]);

  const toggleFav = async (id, e) => {
    e.stopPropagation();
    await api.toggleFavorite(user.email, id);
    setFavIds((s) => {
      const next = new Set(s);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>Question Bank</h1>

      <div style={{ display: 'flex', gap: 10, marginBottom: 20, flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: '1 1 240px' }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: 11, color: 'var(--text-muted)' }} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && load()}
            placeholder="Search titles or passages..."
            style={{ width: '100%', padding: '9px 12px 9px 34px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 13, background: 'var(--paper-raised)' }}
          />
        </div>

        <select
          value={module}
          onChange={(e) => setSearchParams(e.target.value ? { module: e.target.value } : {})}
          style={{ padding: '9px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 13 }}
        >
          <option value="">All modules</option>
          <option value="reading">Reading</option>
          <option value="writing">Writing</option>
          <option value="speaking">Speaking</option>
          <option value="listening">Listening</option>
        </select>

        <select
          value={q_type}
          onChange={(e) => setSearchParams({ ...(module ? { module } : {}), ...(e.target.value ? { q_type: e.target.value } : {}) })}
          style={{ padding: '9px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 13 }}
        >
          <option value="">All types</option>
          {Object.entries(TYPE_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          style={{ padding: '9px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 13 }}
        >
          <option value="">All difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        <button
          onClick={() => setFavoritesOnly((v) => !v)}
          style={{
            display: 'flex', alignItems: 'center', gap: 6, padding: '9px 14px', borderRadius: 'var(--radius-sm)',
            border: `1px solid ${favoritesOnly ? 'var(--amber)' : 'var(--line-strong)'}`,
            background: favoritesOnly ? 'var(--amber-soft)' : 'var(--paper-raised)',
            fontSize: 13, fontWeight: 600, color: favoritesOnly ? 'var(--amber)' : 'var(--text-secondary)',
          }}
        >
          <Star size={14} fill={favoritesOnly ? 'var(--amber)' : 'none'} />
          Favorites
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {questions.map((q) => (
          <button
            key={q.id}
            onClick={() => navigate(`/practice/${q.id}`)}
            style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '14px 16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--line)', background: 'var(--paper-raised)', textAlign: 'left' }}
          >
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 4 }}>
                <span className="mono" style={{ fontSize: 11, fontWeight: 700, color: 'var(--focus)', background: 'var(--focus-soft)', padding: '2px 7px', borderRadius: 999 }}>
                  {TYPE_LABELS[q.q_type] || q.q_type}
                </span>
                <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'capitalize' }}>{q.difficulty}</span>
              </div>
              <h4 style={{ fontSize: 15 }}>{q.title}</h4>
            </div>
            <button onClick={(e) => toggleFav(q.id, e)} style={{ background: 'none', border: 'none', padding: 6 }}>
              <Star size={17} color="var(--amber)" fill={favIds.has(q.id) ? 'var(--amber)' : 'none'} />
            </button>
            <ArrowRight size={16} color="var(--text-muted)" />
          </button>
        ))}
        {questions.length === 0 && <p style={{ color: 'var(--text-muted)', fontSize: 14, padding: '20px 0' }}>No questions match these filters.</p>}
      </div>
    </div>
  );
}
