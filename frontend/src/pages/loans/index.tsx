// ============================
// frontend/src/pages/loans/index.tsx
// ============================
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { Loan, LoanStatus } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Plus, Search, Filter } from 'lucide-react'

export default function LoansPage() {
  const { t } = useTranslation()
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<LoanStatus | 'ALL'>('ALL')

  const { data: loans, isLoading } = useQuery({
    queryKey: ['loans', searchTerm, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'ALL') params.append('status', statusFilter)
      
      const response = await api.get<Loan[]>(`/v1/loans?${params}`)
      return response.data
    },
  })

  const getStatusBadge = (status: LoanStatus) => {
    const variants: Record<LoanStatus, 'default' | 'secondary' | 'success' | 'warning' | 'destructive'> = {
      [LoanStatus.DRAFT]: 'secondary',
      [LoanStatus.APPROVED]: 'default',
      [LoanStatus.IN_PROGRESS]: 'warning',
      [LoanStatus.DISBURSING]: 'warning',
      [LoanStatus.COMPLETED]: 'success',
      [LoanStatus.CANCELLED]: 'destructive',
      [LoanStatus.SUSPENDED]: 'destructive',
    }

    return (
      <Badge variant={variants[status]}>
        {t(`loan.status.${status}`)}
      </Badge>
    )
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{t('loans.title')}</h1>
          <p className="text-gray-500">{t('loans.subtitle')}</p>
        </div>
        <Button asChild>
          <Link to="/loans/new">
            <Plus className="mr-2 h-4 w-4" />
            {t('loans.new')}
          </Link>
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>{t('common.filters')}</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <Input
                placeholder={t('loans.searchPlaceholder')}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <select
            className="rounded-md border px-3 py-2"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as LoanStatus | 'ALL')}
          >
            <option value="ALL">{t('common.allStatuses')}</option>
            {Object.values(LoanStatus).map((status) => (
              <option key={status} value={status}>
                {t(`loan.status.${status}`)}
              </option>
            ))}
          </select>
        </CardContent>
      </Card>

      {/* Loans List */}
      <div className="grid gap-4">
        {loans?.map((loan) => (
          <Card key={loan.id}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold">{loan.loan_number}</h3>
                    {getStatusBadge(loan.status)}
                  </div>
                  <p className="text-sm text-gray-500">
                    {loan.client?.name} - {t(`loan.type.${loan.loan_type}`)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {t('loan.created')}: {formatDate(loan.created_at)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold">
                    {formatCurrency(loan.amount)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {loan.duration_months} {t('common.months')}
                  </p>
                  <Button asChild variant="outline" size="sm" className="mt-2">
                    <Link to={`/loans/${loan.id}`}>
                      {t('common.viewDetails')}
                    </Link>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
