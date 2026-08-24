import React from 'react';
import { cn } from '../../utils/classNames';

export default function Skeleton({ className, height = 'h-4' }) {
  return (
    <div
      className={cn(
        'w-full rounded-[4px] bg-[#E0D9CC] animate-pulse',
        height,
        className,
      )}
    />
  );
}