import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { itemsApi, type CreateItem } from '../api/client'

export function Items() {
  const queryClient = useQueryClient()
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const { data: items, isLoading } = useQuery({
    queryKey: ['items'],
    queryFn: itemsApi.getAll,
  })

  const createMutation = useMutation({
    mutationFn: (item: CreateItem) => itemsApi.create(item),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] })
      setName('')
      setDescription('')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: itemsApi.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['items'] }),
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    createMutation.mutate({
      name: name.trim(),
      description: description.trim() || undefined,
    })
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Items</h2>

      <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Item name"
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={createMutation.isPending || !name.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          Add
        </button>
      </form>

      {isLoading && <p className="text-sm text-gray-400">Loading...</p>}

      {!isLoading && items?.length === 0 && (
        <p className="text-sm text-gray-400">No items yet. Add one above.</p>
      )}

      <ul className="space-y-2">
        {items?.map((item) => (
          <li
            key={item.id}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
          >
            <div>
              <p className="text-sm font-medium text-gray-800">{item.name}</p>
              {item.description && (
                <p className="text-xs text-gray-500">{item.description}</p>
              )}
            </div>
            <button
              onClick={() => deleteMutation.mutate(item.id)}
              disabled={deleteMutation.isPending}
              className="text-sm text-red-500 hover:text-red-700 transition-colors disabled:opacity-50"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
