import { useQuery } from '@tanstack/react-query'
import { healthApi } from '../api/client'

export function HealthCheck() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['health'],
    queryFn: healthApi.check,
    refetchInterval: 30_000,
  })

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">System Health</h2>
        <button
          onClick={() => refetch()}
          className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
        >
          Refresh
        </button>
      </div>

      {isLoading && <p className="text-sm text-gray-400">Checking...</p>}

      {isError && (
        <StatusRow label="API" healthy={false} detail="unreachable" />
      )}

      {data && (
        <div className="space-y-2">
          <StatusRow label="API" healthy={data.status === 'ok'} />
          <StatusRow
            label="Database"
            healthy={data.database === 'healthy'}
            detail={data.database !== 'healthy' ? data.database : undefined}
          />
        </div>
      )}
    </div>
  )
}

function StatusRow({
  label,
  healthy,
  detail,
}: {
  label: string
  healthy: boolean
  detail?: string
}) {
  return (
    <div className="flex items-center gap-3">
      <span
        className={`w-2.5 h-2.5 rounded-full ${healthy ? 'bg-green-500' : 'bg-red-500'}`}
      />
      <span className="text-sm font-medium text-gray-700">{label}</span>
      {detail && <span className="text-xs text-red-500">{detail}</span>}
    </div>
  )
}
