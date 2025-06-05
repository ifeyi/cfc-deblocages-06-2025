// ============================
// frontend/src/App.tsx
// ============================
import { Suspense } from 'react'
import { Outlet } from 'react-router-dom'
import { Layout } from '@/components/layout'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { useAuthStore } from '@/stores/auth-store'
import { useEffect } from 'react'

export function App() {
  const { checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  return (
    <Layout>
      <Suspense fallback={<LoadingSpinner />}>
        <Outlet />
      </Suspense>
    </Layout>
  )
}