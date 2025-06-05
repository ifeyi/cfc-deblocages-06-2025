// ============================
// frontend/src/router.tsx
// ============================
import { createBrowserRouter, Navigate } from 'react-router-dom'
import { App } from './App'
import { ProtectedRoute } from '@/components/auth/protected-route'

// Lazy load pages
import { lazy } from 'react'

const LoginPage = lazy(() => import('@/pages/auth/login'))
const DashboardPage = lazy(() => import('@/pages/dashboard'))
const ClientsPage = lazy(() => import('@/pages/clients'))
const ClientDetailPage = lazy(() => import('@/pages/clients/[id]'))
const LoansPage = lazy(() => import('@/pages/loans'))
const LoanDetailPage = lazy(() => import('@/pages/loans/[id]'))
const DisbursementsPage = lazy(() => import('@/pages/disbursements'))
const AlertsPage = lazy(() => import('@/pages/alerts'))
const ReportsPage = lazy(() => import('@/pages/reports'))
const SettingsPage = lazy(() => import('@/pages/settings'))

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: (
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'clients',
        children: [
          {
            index: true,
            element: (
              <ProtectedRoute>
                <ClientsPage />
              </ProtectedRoute>
            ),
          },
          {
            path: ':id',
            element: (
              <ProtectedRoute>
                <ClientDetailPage />
              </ProtectedRoute>
            ),
          },
        ],
      },
      {
        path: 'loans',
        children: [
          {
            index: true,
            element: (
              <ProtectedRoute>
                <LoansPage />
              </ProtectedRoute>
            ),
          },
          {
            path: ':id',
            element: (
              <ProtectedRoute>
                <LoanDetailPage />
              </ProtectedRoute>
            ),
          },
        ],
      },
      {
        path: 'disbursements',
        element: (
          <ProtectedRoute>
            <DisbursementsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'alerts',
        element: (
          <ProtectedRoute>
            <AlertsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'reports',
        element: (
          <ProtectedRoute>
            <ReportsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: 'settings',
        element: (
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        ),
      },
    ],
  },
])
