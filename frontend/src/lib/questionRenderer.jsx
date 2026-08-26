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

export const WRITING_TYPES = new Set(['swt', 'essay']);
export const SPEAKING_TYPES = new Set(['read_aloud', 'repeat_sentence', 'answer_short_question', 'describe_image']);
export const LISTENING_TYPES = new Set(['l_mcq_single', 'l_mcq_multi', 'l_fill_blanks', 'highlight_summary', 'select_missing_word', 'write_from_dictation']);

export function getModuleForType(q_type) {
  if (WRITING_TYPES.has(q_type)) return 'writing';
  if (SPEAKING_TYPES.has(q_type)) return 'speaking';
  if (LISTENING_TYPES.has(q_type)) return 'listening';
  return 'reading';
}

export function canSubmitAnswer(q_type, userAnswer) {
  if (WRITING_TYPES.has(q_type) || SPEAKING_TYPES.has(q_type)) {
    return (userAnswer.text || userAnswer.transcript || '').trim().length > 0;
  }
  return Object.keys(userAnswer).length > 0;
}

export function renderQuestionComponent(question, userAnswer, onChange, result) {
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
