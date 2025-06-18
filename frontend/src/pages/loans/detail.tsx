import { useParams } from 'react-router-dom'

export default function LoanDetailPage() {
  const { id } = useParams()

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Détail Prêt #{id}</h1>
      <p>Informations détaillées du prêt</p>
    </div>
  )
}