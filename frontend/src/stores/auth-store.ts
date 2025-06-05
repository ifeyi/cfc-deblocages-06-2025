// ============================
// frontend/src/stores/auth-store.ts
// ============================
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '@/lib/api'

interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: string
  agency?: string
  preferred_language: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (username, password) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/v1/auth/login', {
            username,
            password,
          })
          
          const { access_token, user } = response.data
          
          set({
            token: access_token,
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      checkAuth: () => {
        const state = get()
        if (state.token && state.user) {
          set({ isAuthenticated: true })
        } else {
          set({ isAuthenticated: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
      }),
    }
  )
)