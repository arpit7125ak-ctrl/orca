import { useState } from 'react'
import { runAnalysis } from '../services/api.js'

function useAnalysis() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyze = async (latitude, longitude) => {
    setLoading(true)
    setError(null)

    try {
      const result = await runAnalysis(latitude, longitude)
      setData(result)
      return result
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    data,
    loading,
    error,
    analyze,
  }
}

export default useAnalysis