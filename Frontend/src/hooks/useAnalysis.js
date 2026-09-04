import { useState } from 'react'
import { getAnalysis, runAnalysis } from '../services/api.js'

function useAnalysis() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyze = async (latitude, longitude) => {
    setLoading(true)
    setError(null)
    setData(null)

    try {
      const created = await runAnalysis(latitude, longitude)
      setData(created)

      if (!created?.analysisId) {
        return created
      }

      const terminalStatuses = new Set(['completed', 'partial', 'failed'])
      let latest = created

      for (let attempt = 0; attempt < 30; attempt += 1) {
        if (terminalStatuses.has(String(latest?.status || '').toLowerCase())) {
          break
        }

        await new Promise((resolve) => setTimeout(resolve, 2000))
        latest = await getAnalysis(created.analysisId)
        setData(latest)
      }

      return latest
    } catch (err) {
      setError(err.message || 'Analysis failed.')
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
