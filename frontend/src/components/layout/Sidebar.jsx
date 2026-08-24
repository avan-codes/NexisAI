import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Workflow, ScrollText, Settings, LogOut } from 'lucide-react';
import { useAuthStore } from '../../store/auth';
import { cn } from '../../utils/classNames';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/executions', label: 'Workflows', icon: Workflow },
  { to: '/audit', label: 'Audit Logs', icon: ScrollText },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ mobileOpen, onClose }) {
  const { user, logout } = useAuthStore();

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div className="fixed inset-0 bg-black/40 z-30 lg:hidden" onClick={onClose} />
      )}
      <aside
        className={cn(
          'fixed lg:static z-40 h-full w-[260px] bg-border-strong text-text-on-dark flex flex-col transition-transform duration-200',
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
        )}
      >
        <div className="p-6 border-b border-text-on-dark/10">
          <h1 className="font-display font-bold text-2xl tracking-tight">
            NEXIS<span className="text-accent-primary">.</span>AI
          </h1>
        </div>
        <nav className="flex-1 py-4">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-3 font-sans uppercase text-[13px] tracking-label hover:bg-[#2B2A26] transition-colors',
                  isActive ? 'bg-accent-primary text-text-primary' : 'text-text-on-dark',
                )
              }
              onClick={onClose}
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-text-on-dark/10">
          <div className="flex items-center gap-3">
            <img
              src={user?.avatar_url || 'https://github.com/github.png'}
              alt=""
              className="w-6 h-6 rounded-full border border-text-on-dark/30"
            />
            <div className="min-w-0">
              <p className="font-mono text-xs truncate">{user?.username || 'user'}</p>
              <p className="font-mono text-[10px] text-text-on-dark/60 truncate">main repo</p>
            </div>
            <button
              onClick={logout}
              className="ml-auto p-1 hover:bg-[#2B2A26] rounded-sm"
              title="Logout"
            >
              <LogOut size={14} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}