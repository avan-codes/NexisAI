import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCommand } from '../../api/commands';
import { useToastStore } from '../../store/toasts';
import { useAuthStore } from '../../store/auth';

export default function TerminalCommandBar({ repoId }) {
  const [command, setCommand] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const addToast = useToastStore((s) => s.addToast);
  const { user } = useAuthStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!command.trim()) return;
    setLoading(true);
    try {
      const res = await createCommand(repoId, command);
      addToast({
        type: 'success',
        title: 'Execution Started',
        message: `#${res.data.execution_id}`,
      });
      navigate(`/executions/${res.data.execution_id}`);
    } catch (err) {
      addToast({
        type: 'error',
        title: 'Command Failed',
        message: err.response?.data?.detail || 'Unknown error',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full">
      <div className="flex items-center bg-code-bg border-2 border-border-strong rounded-none px-4 py-3">
        <span className="font-mono text-[14px] text-accent-secondary whitespace-nowrap">
          nexis:~$
        </span>
        <input
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder='e.g. /updatefrontend "Add dark mode"'
          className="flex-1 ml-3 bg-transparent border-none outline-none font-mono text-[14px] text-code-text placeholder:text-text-secondary caret-accent-primary"
          autoFocus
        />
        <span className="terminal-caret ml-1" />
      </div>
      <button
        type="submit"
        className="absolute right-2 top-1/2 -translate-y-1/2 h-8 px-3 bg-accent-primary text-text-on-dark font-sans font-bold uppercase text-[11px] tracking-label border border-border-strong hover:shadow-brutal-sm active:translate-y-[calc(-50%+1px)] transition-all"
      >
        Run
      </button>
    </form>
  );
}