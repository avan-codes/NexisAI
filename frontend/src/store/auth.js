import { create } from 'zustand';
import { getMe, loginWithToken } from '../api/auth';
import { storage } from '../utils/storage';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  loading: true,
  token: storage.get('nexis_token'),

  checkAuth: async () => {
    const token = storage.get('nexis_token');
    if (!token) {
      set({ loading: false, isAuthenticated: false });
      return;
    }
    try {
      const user = await getMe();
      set({ user, isAuthenticated: true, loading: false });
    } catch (err) {
      storage.remove('nexis_token');
      set({ user: null, isAuthenticated: false, loading: false });
    }
  },

  setToken: (token) => {
    storage.set('nexis_token', token);
    set({ token, isAuthenticated: true });
  },

  logout: () => {
    storage.remove('nexis_token');
    set({ user: null, isAuthenticated: false, token: null });
  },
}));