import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { CheckCircle2, XCircle, AlertTriangle, X } from 'lucide-react';
import { useToastStore } from '../../store/toasts';

const icons = {
  success: <CheckCircle2 size={16} />,
  error: <XCircle size={16} />,
  warning: <AlertTriangle size={16} />,
};

export default function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const removeToast = useToastStore((s) => s.removeToast);

  return (
    <div className="fixed top-4 right-4 z-[100] flex flex-col gap-3 w-[360px] max-w-[calc(100vw-2rem)]">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            layout
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 50, opacity: 0 }}
            className="bg-surface border-2 border-border-strong shadow-brutal p-4 rounded-card"
          >
            <div className="flex items-start gap-3">
              <div className="text-accent-primary">{icons[toast.type] || icons.info}</div>
              <div className="flex-1 min-w-0">
                <p className="font-sans font-bold uppercase text-[11px] tracking-label">{toast.title}</p>
                <p className="font-sans text-[14px] text-text-primary mt-1">{toast.message}</p>
              </div>
              <button
                onClick={() => removeToast(toast.id)}
                className="text-text-secondary hover:text-text-primary"
              >
                <X size={14} />
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}