import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user, token, loading } = useAuth();

  if (loading) {
    return <div style={{ padding: 40, color: 'var(--text-muted)' }}>Loading…</div>;
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
