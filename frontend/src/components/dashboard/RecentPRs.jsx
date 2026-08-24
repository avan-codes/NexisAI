import React from 'react';
import { ExternalLink } from 'lucide-react';
import Card, { CardHeader } from '../ui/Card';

const mockPRs = [
  { title: 'Nexis: update frontend dark mode', branch: 'nexis/update_frontend-1716000000', status: 'open' },
  { title: 'Nexis: fix checkout bug', branch: 'nexis/fix_bug-1715950000', status: 'merged' },
];

export default function RecentPRs() {
  return (
    <Card>
      <CardHeader title="Recent PRs" />
      <div className="space-y-3">
        {mockPRs.map((pr, i) => (
          <a
            key={i}
            href="#"
            className="block p-3 border-2 border-border-strong shadow-brutal-sm hover:shadow-brutal transition-all group"
          >
            <div className="flex items-start justify-between gap-2">
              <p className="font-mono text-sm font-medium text-text-primary">{pr.title}</p>
              <ExternalLink size={14} className="text-text-secondary group-hover:text-accent-primary" />
            </div>
            <p className="font-mono text-xs text-text-secondary mt-1">{pr.branch}</p>
            <span className={`inline-block mt-2 px-2 py-0.5 font-mono text-[10px] uppercase border border-border-strong ${pr.status === 'open' ? 'bg-accent-secondary text-text-primary' : 'bg-success text-text-on-dark'}`}>
              {pr.status}
            </span>
          </a>
        ))}
      </div>
    </Card>
  );
}