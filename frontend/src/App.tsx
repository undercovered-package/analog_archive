import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { HealthCheck } from './components/HealthCheck'
import { Items } from './components/Items'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold text-gray-900">Darkroom</h1>
          </div>
        </header>
        <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
          <HealthCheck />
          <Items />
        </main>
      </div>
    </QueryClientProvider>
  )
}
