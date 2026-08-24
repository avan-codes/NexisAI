import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../utils/classNames'; // simple className joiner

const variants = {
  primary: 'bg-accent-primary text-text-on-dark border-2 border-border-strong shadow-brutal hover:shadow-brutal-lg hover:-translate-x-0.5 hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-none',
  secondary: 'bg-transparent text-text-primary border-2 border-border-strong shadow-brutal hover:shadow-brutal-lg hover:-translate-x-0.5 hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-none',
  ghost: 'text-accent-primary underline-offset-4 hover:underline bg-transparent border-none shadow-none',
};

export default function Button({ variant = 'primary', size = 'md', className, children, ...props }) {
  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      className={cn(
        'inline-flex items-center justify-center gap-2 font-sans font-bold uppercase tracking-label transition-all duration-150 disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none',
        size === 'md' ? 'h-10 px-4 text-[13px] leading-4' : '',
        size === 'icon' ? 'h-10 w-10 p-0 shadow-brutal-sm border-2 border-border-strong' : '',
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </motion.button>
  );
}