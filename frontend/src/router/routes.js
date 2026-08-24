import Login from '../pages/Login';
import AuthCallback from '../pages/AuthCallback';
import Dashboard from '../pages/Dashboard';
import ExecutionsList from '../pages/ExecutionsList';
import ExecutionDetail from '../pages/ExecutionDetail';
import AuditLogs from '../pages/AuditLogs';
import Settings from '../pages/Settings';

const routes = [
  { path: '/login', element: <Login />, protected: false },
  { path: '/auth/callback', element: <AuthCallback />, protected: false },
  { path: '/dashboard', element: <Dashboard />, protected: true },
  { path: '/executions', element: <ExecutionsList />, protected: true },
  { path: '/executions/:id', element: <ExecutionDetail />, protected: true },
  { path: '/audit', element: <AuditLogs />, protected: true },
  { path: '/settings', element: <Settings />, protected: true },
];

export default routes;