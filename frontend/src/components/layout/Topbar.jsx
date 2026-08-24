import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Command } from 'lucide-react';
import { useCommandPaletteStore } from '../../store/commandPalette';

export default function Topbar() {
  const location = useLocation();
  const openPalette = useCommandPaletteStore((s) => s.open);
  const navigate = useNavigate();

  const pathSegments = location.pathname.split('/').filter(Boolean);
  const breadcrumb = pathSegments.length ? pathSegments.join(' / ') : 'dashboard';

  return (
    <header className="h-16 border-b-2 border-border-strong bg-bg flex items-center px-6 gap-4">
      <div className="font-mono text-[13px] text-text-secondary">
        nexis / {breadcrumb}
      </div>
      <button
        onClick={openPalette}
        className="ml-auto flex items-center gap-2 h-9 px-3 border-2 border-border-strong shadow-brutal-sm font-mono text-xs hover:shadow-brutal active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all"
      >
        <Command size={14} />
        <kbd>⌘K</kbd>
      </button>
    </header>
  );
}