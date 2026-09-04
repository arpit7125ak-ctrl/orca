const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

export async function runAnalysis(latitude, longitude) {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      activity: 'Fishing',
      date: new Date().toISOString().split('T')[0],
      time: '08:00',
      zones: [
        {
          zoneId: 'Z1',
          latitude,
          longitude,
        },
      ],
    }),
  })

  const result = await response.json()

  if (!response.ok) {
    throw new Error(result.message || `Analysis request failed: ${response.status}`)
  }

  return result.data
}