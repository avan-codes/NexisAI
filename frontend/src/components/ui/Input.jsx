import React from 'react';
import { cn } from '../../utils/classNames';

export default function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        'w-full bg-surface border-2 border-border-strong rounded-none px-3 py-2.5 font-sans text-[14px] placeholder:text-text-secondary focus:outline-none focus:border-focus-ring focus:shadow-[3px_3px_0_#7A8B3A] transition-shadow',
        className,
      )}
      {...props}
    />
  );
}