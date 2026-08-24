import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuthStore();
  const location = useLocation();

  if (loading) {
    return <div className="p-8 text-sm font-mono">Loading session...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}