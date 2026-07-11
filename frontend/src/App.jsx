import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Reading from './pages/Reading';
import QuestionBank from './pages/QuestionBank';
import Practice from './pages/Practice';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reading" element={<Reading />} />
          <Route path="/question-bank" element={<QuestionBank />} />
          <Route path="/practice/:id" element={<Practice />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
