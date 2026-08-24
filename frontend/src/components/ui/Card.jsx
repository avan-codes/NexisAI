import React from 'react';
import { cn } from '../../utils/classNames';

export default function Card({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'bg-surface border-2 border-border-strong rounded-card shadow-brutal-lg p-6',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, className }) {
  return (
    <div className={cn('pb-4 mb-4 border-b-2 border-dashed border-border-soft', className)}>
      <h3 className="uppercase text-sm tracking-label font-display font-bold">{title}</h3>
    </div>
  );
}