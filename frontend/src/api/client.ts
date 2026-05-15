import axios from 'axios'

export const apiClient = axios.create({
  headers: { 'Content-Type': 'application/json' },
})

export interface Item {
  id: number
  name: string
  description: string | null
}

export interface CreateItem {
  name: string
  description?: string
}

export interface HealthStatus {
  status: string
  database: string
}

export const healthApi = {
  check: (): Promise<HealthStatus> =>
    apiClient.get('/health').then((r) => r.data),
}

export const itemsApi = {
  getAll: (): Promise<Item[]> =>
    apiClient.get('/api/v1/items').then((r) => r.data),
  create: (item: CreateItem): Promise<Item> =>
    apiClient.post('/api/v1/items', item).then((r) => r.data),
  delete: (id: number): Promise<void> =>
    apiClient.delete(`/api/v1/items/${id}`).then((r) => r.data),
}
