import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card, { CardHeader } from '../ui/Card';
import StatusBadge from '../ui/StatusBadge';

export default function LiveActivityFeed({ executions }) {
  const navigate = useNavigate();

  return (
    <Card>
      <CardHeader title="Live Activity Feed" />
      <div className="space-y-2">
        {executions.length === 0 ? (
          <p className="font-mono text-sm text-text-secondary">No executions yet. Run a command above.</p>
        ) : (
          executions.map((exec) => (
            <button
              key={exec._id}
              onClick={() => navigate(`/executions/${exec._id}`)}
              className="w-full text-left p-3 border-b border-dashed border-border-soft hover:bg-[#F0E9D8] transition-colors flex items-center gap-4"
            >
              <span className="font-mono text-xs text-text-secondary truncate flex-1">{exec.repo?.full_name || 'repo'}</span>
              <span className="font-mono text-xs truncate max-w-[200px]">{exec.command?.text || ''}</span>
              <StatusBadge status={exec.status} />
              <span className="font-mono text-[11px] text-text-secondary whitespace-nowrap">
                {new Date(exec.created_at).toLocaleTimeString()}
              </span>
            </button>
          ))
        )}
      </div>
    </Card>
  );
}