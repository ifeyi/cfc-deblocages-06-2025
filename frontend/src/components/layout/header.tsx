// ============================
// frontend/src/components/layout/header.tsx
// ============================
import { useTranslation } from 'react-i18next'
import { Bell, Globe } from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { getInitials } from '@/lib/utils'

export function Header() {
  const { t, i18n } = useTranslation()
  const { user } = useAuthStore()

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng)
  }

  return (
    <header className="h-16 bg-white border-b">
      <div className="flex h-full items-center justify-between px-6">
        {/* Page title will be here */}
        <div className="flex-1" />

        <div className="flex items-center gap-4">
          {/* Language selector */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <Globe className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => changeLanguage('fr')}>
                Français
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => changeLanguage('en')}>
                English
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Notifications */}
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500" />
          </Button>

          {/* User menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-medium">
                  {user ? getInitials(user.full_name) : 'U'}
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium">{user?.full_name}</p>
                  <p className="text-xs text-gray-500">{user?.role}</p>
                </div>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>{t('user.profile')}</DropdownMenuItem>
              <DropdownMenuItem>{t('user.settings')}</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}