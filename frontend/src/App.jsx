import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Reading from './pages/Reading';
import Writing from './pages/Writing';
import Speaking from './pages/Speaking';
import Listening from './pages/Listening';
import QuestionBank from './pages/QuestionBank';
import Practice from './pages/Practice';
import MockTest from './pages/MockTest';
import MockTestRunner from './pages/MockTestRunner';

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/reading" element={<Reading />} />
              <Route path="/writing" element={<Writing />} />
              <Route path="/speaking" element={<Speaking />} />
              <Route path="/listening" element={<Listening />} />
              <Route path="/question-bank" element={<QuestionBank />} />
              <Route path="/practice/:id" element={<Practice />} />
              <Route path="/mock-test" element={<MockTest />} />
              <Route path="/mock-test/run" element={<MockTestRunner />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
