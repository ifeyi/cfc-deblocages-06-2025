// ============================
// frontend/src/pages/alerts/index.tsx
// ============================
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Alert, AlertStatus } from '@/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { formatDate, getRelativeTime } from '@/lib/utils'
import { AlertCircle, CheckCircle, Clock } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AlertsPage() {
  const { t } = useTranslation()
  const queryClient = useQueryClient()

  const { data: alerts, isLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const response = await api.get<Alert[]>('/v1/alerts')
      return response.data
    },
  })

  const acknowledgeMutation = useMutation({
    mutationFn: async (alertId: number) => {
      await api.put(`/v1/alerts/${alertId}/acknowledge`)
    },
    onSuccess: () => {
      toast.success(t('alerts.acknowledged'))
      queryClient.invalidateQueries(['alerts'])
    },
  })

  const resolveMutation = useMutation({
    mutationFn: async (alertId: number) => {
      await api.put(`/v1/alerts/${alertId}/resolve`)
    },
    onSuccess: () => {
      toast.success(t('alerts.resolved'))
      queryClient.invalidateQueries(['alerts'])
    },
  })

  const getSeverityIcon = (severity: string) => {
    if (severity === 'RED') {
      return <AlertCircle className="h-5 w-5 text-red-500" />
    }
    return <Clock className="h-5 w-5 text-orange-500" />
  }

  const getStatusBadge = (status: AlertStatus) => {
    const variants: Record<AlertStatus, 'default' | 'secondary' | 'success' | 'warning'> = {
      [AlertStatus.PENDING]: 'warning',
      [AlertStatus.ACKNOWLEDGED]: 'secondary',
      [AlertStatus.RESOLVED]: 'success',
      [AlertStatus.ESCALATED]: 'destructive',
    }

    return (
      <Badge variant={variants[status]}>
        {t(`alert.status.${status}`)}
      </Badge>
    )
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  const pendingAlerts = alerts?.filter(a => a.status === AlertStatus.PENDING) || []
  const otherAlerts = alerts?.filter(a => a.status !== AlertStatus.PENDING) || []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{t('alerts.title')}</h1>
        <p className="text-gray-500">{t('alerts.subtitle')}</p>
      </div>

      {/* Alert Summary */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">
              {t('alerts.pendingCount')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pendingAlerts.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">
              {t('alerts.criticalCount')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {pendingAlerts.filter(a => a.severity === 'RED').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">
              {t('alerts.warningCount')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {pendingAlerts.filter(a => a.severity === 'ORANGE').length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Pending Alerts */}
      {pendingAlerts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">{t('alerts.pending')}</h2>
          {pendingAlerts.map((alert) => (
            <Card key={alert.id} className="border-l-4 border-l-red-500">
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex gap-3">
                    {getSeverityIcon(alert.severity)}
                    <div className="space-y-1">
                      <p className="font-medium">{alert.message}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{t(`alert.type.${alert.alert_type}`)}</span>
                        <span>{getRelativeTime(alert.triggered_at)}</span>
                        {alert.loan && (
                          <span>Prêt: {alert.loan.loan_number}</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {getStatusBadge(alert.status)}
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => acknowledgeMutation.mutate(alert.id)}
                    >
                      {t('alerts.acknowledge')}
                    </Button>
                    <Button
                      size="sm"
                      onClick={() => resolveMutation.mutate(alert.id)}
                    >
                      {t('alerts.resolve')}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Other Alerts */}
      {otherAlerts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">{t('alerts.history')}</h2>
          {otherAlerts.map((alert) => (
            <Card key={alert.id} className="opacity-75">
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div className="space-y-1">
                      <p className="font-medium">{alert.message}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{t(`alert.type.${alert.alert_type}`)}</span>
                        <span>{formatDate(alert.triggered_at)}</span>
                        {alert.resolved_at && (
                          <span>
                            {t('alerts.resolvedAt')}: {formatDate(alert.resolved_at)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div>{getStatusBadge(alert.status)}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}