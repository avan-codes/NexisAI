import { create } from 'zustand';

let id = 0;

export const useToastStore = create((set) => ({
  toasts: [],
  addToast: (toast) => {
    const toastId = ++id;
    set((state) => ({ toasts: [...state.toasts, { id: toastId, ...toast }] }));
    setTimeout(() => {
      set((state) => ({ toasts: state.toasts.filter((t) => t.id !== toastId) }));
    }, toast.duration || 5000);
  },
  removeToast: (toastId) =>
    set((state) => ({ toasts: state.toasts.filter((t) => t.id !== toastId) })),
}));