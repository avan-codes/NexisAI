import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import Button from './Button';
import { cn } from '../../utils/classNames';

export default function Modal({ open, onClose, title, children, footer, maxWidth = 'max-w-[600px]' }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-[rgba(26,25,23,0.6)]" onClick={onClose} />
          <motion.div
            className={cn('relative bg-surface border-2 border-border-strong shadow-brutal-lg rounded-card p-6 w-full', maxWidth)}
            initial={{ y: 20, opacity: 0, scale: 0.98 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: 20, opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.2 }}
          >
            <div className="flex items-start justify-between mb-4">
              <h3 className="font-display font-bold text-lg uppercase tracking-label">{title}</h3>
              <button
                onClick={onClose}
                className="p-1 hover:bg-border-soft rounded-sm transition-colors"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>
            <div>{children}</div>
            {footer && <div className="mt-6 flex justify-end gap-3">{footer}</div>}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}