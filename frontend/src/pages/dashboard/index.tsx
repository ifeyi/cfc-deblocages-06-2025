// ============================
// frontend/src/pages/dashboard/index.tsx
// ============================
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { api } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import {
  FileText,
  Users,
  AlertCircle,
  CreditCard,
  TrendingUp,
  Clock,
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface DashboardStats {
  totalClients: number
  activeLoans: number
  pendingDisbursements: number
  activeAlerts: {
    total: number
    red: number
    orange: number
  }
  monthlyDisbursements: {
    month: string
    amount: number
  }[]
}

export default function DashboardPage() {
  const { t } = useTranslation()

  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await api.get<DashboardStats>('/v1/reports/dashboard')
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner />
  }

  const statCards = [
    {
      title: t('dashboard.totalClients'),
      value: stats?.totalClients || 0,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: t('dashboard.activeLoans'),
      value: stats?.activeLoans || 0,
      icon: FileText,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: t('dashboard.pendingDisbursements'),
      value: stats?.pendingDisbursements || 0,
      icon: CreditCard,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: t('dashboard.activeAlerts'),
      value: stats?.activeAlerts?.total || 0,
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
      subtext: `${stats?.activeAlerts?.red || 0} critiques, ${stats?.activeAlerts?.orange || 0} avertissements`,
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{t('dashboard.title')}</h1>
        <p className="text-gray-500">{t('dashboard.subtitle')}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <div className={`rounded-full p-2 ${stat.bgColor}`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              {stat.subtext && (
                <p className="text-xs text-muted-foreground mt-1">
                  {stat.subtext}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.monthlyDisbursements')}</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats?.monthlyDisbursements || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
                <Bar dataKey="amount" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.recentActivity')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Recent activities would be fetched here */}
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-blue-100 p-2">
                  <FileText className="h-4 w-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium">Nouveau prêt approuvé</p>
                  <p className="text-xs text-gray-500">Client: Jean Dupont - 50,000,000 FCFA</p>
                </div>
                <p className="text-xs text-gray-500">Il y a 2h</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}