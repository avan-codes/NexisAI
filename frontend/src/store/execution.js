import { create } from 'zustand';

export const useExecutionStore = create((set) => ({
  currentExecution: null,
  steps: [],
  logs: {},

  setExecution: (execution) => set({ currentExecution: execution, steps: execution.steps || [] }),
  updateStep: (stepIndex, patch) =>
    set((state) => ({
      steps: state.steps.map((step, i) =>
        i === stepIndex ? { ...step, ...patch } : step,
      ),
    })),
  appendLog: (stepIndex, log) =>
    set((state) => ({
      logs: {
        ...state.logs,
        [stepIndex]: [...(state.logs[stepIndex] || []), log],
      },
    })),
  reset: () => set({ currentExecution: null, steps: [], logs: {} }),
}));