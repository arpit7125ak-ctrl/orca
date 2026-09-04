const API_BASE_URL = import.meta.env.VITE_API_URL

export async function runAnalysis(latitude, longitude) {
  const response = await fetch(`${API_BASE_URL}/api/analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      latitude,
      longitude,
    }),
  })

  if (!response.ok) {
    throw new Error(`Analysis request failed: ${response.status}`)
  }

  return response.json()
}