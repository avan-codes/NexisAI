import React from 'react';
import { cn } from '../../utils/classNames';

const statusStyles = {
  RUNNING: 'bg-accent-secondary text-text-primary border-border-strong',
  SUCCESS: 'bg-success text-text-on-dark border-border-strong',
  FAILED: 'bg-danger text-text-on-dark border-border-strong',
  AWAITING_APPROVAL: 'bg-accent-tertiary text-text-primary border-border-strong',
  PENDING: 'bg-transparent text-text-secondary border-dashed border-border-soft',
};

export default function StatusBadge({ status, className }) {
  const normalized = status?.toUpperCase();
  const showDot = normalized === 'RUNNING' || normalized === 'AWAITING_APPROVAL';
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-2 py-0.5 font-mono text-[11px] uppercase tracking-wider border-2',
        statusStyles[normalized] || statusStyles.PENDING,
        className,
      )}
    >
      {showDot && <span className="w-2 h-2 rounded-full bg-text-primary status-dot" />}
      {status}
    </span>
  );
}