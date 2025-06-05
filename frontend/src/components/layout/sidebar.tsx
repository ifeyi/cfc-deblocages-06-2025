// ============================
// frontend/src/components/layout/sidebar.tsx
// ============================
import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Users,
  FileText,
  CreditCard,
  AlertCircle,
  BarChart3,
  Settings,
  LogOut,
} from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'

const navItems = [
  {
    to: '/dashboard',
    icon: LayoutDashboard,
    label: 'dashboard',
  },
  {
    to: '/clients',
    icon: Users,
    label: 'clients',
  },
  {
    to: '/loans',
    icon: FileText,
    label: 'loans',
  },
  {
    to: '/disbursements',
    icon: CreditCard,
    label: 'disbursements',
  },
  {
    to: '/alerts',
    icon: AlertCircle,
    label: 'alerts',
  },
  {
    to: '/reports',
    icon: BarChart3,
    label: 'reports',
  },
  {
    to: '/settings',
    icon: Settings,
    label: 'settings',
  },
]

export function Sidebar() {
  const { t } = useTranslation()
  const { logout } = useAuthStore()

  return (
    <aside className="w-64 bg-white shadow-md">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex items-center justify-center h-16 border-b">
          <h1 className="text-xl font-bold text-primary">CFC Déblocages</h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-gray-700 hover:bg-gray-100'
                    )
                  }
                >
                  <item.icon className="h-5 w-5" />
                  {t(`navigation.${item.label}`)}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Logout */}
        <div className="border-t p-4">
          <button
            onClick={logout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
          >
            <LogOut className="h-5 w-5" />
            {t('navigation.logout')}
          </button>
        </div>
      </div>
    </aside>
  )
}

