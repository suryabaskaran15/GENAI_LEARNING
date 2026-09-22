import { useEffect, useState } from 'react'
import apiClient from '../api/client'

function Home() {
  const [status, setStatus] = useState('checking...')
  const [error, setError] = useState(null)

  useEffect(() => {
    apiClient
      .get('/health/')
      .then((res) => setStatus(res.data.message))
      .catch(() => setError('Could not reach backend'))
  }, [])

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-4 bg-white text-center">
      <h1 className="text-4xl font-semibold text-gray-900">Home</h1>
      <p className="text-gray-500">React + Tailwind CSS frontend is up and running.</p>
      <p className={error ? 'text-red-600' : 'text-green-600'}>
        Backend status: {error ?? status}
      </p>
    </div>
  )
}

export default Home
