import { useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from './store/auth';
import { useToastStore } from './store/toasts';
import ToastContainer from './components/ui/Toast';
import ProtectedRoute from './router/ProtectedRoute';
import routes from './router/routes';

export default function App() {
  const { checkAuth, isAuthenticated } = useAuthStore();
  const toasts = useToastStore((s) => s.toasts);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <>
      <Routes>
        {routes.map(({ path, element, protected: isProtected }) =>
          isProtected ? (
            <Route
              key={path}
              path={path}
              element={<ProtectedRoute>{element}</ProtectedRoute>}
            />
          ) : (
            <Route key={path} path={path} element={element} />
          ),
        )}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
      <ToastContainer toasts={toasts} />
    </>
  );
}