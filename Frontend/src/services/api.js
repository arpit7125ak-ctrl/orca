const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

async function requestJson(url, options = {}) {
  const response = await fetch(url, options)

  let result = null
  try {
    result = await response.json()
  } catch {
    result = null
  }

  if (!response.ok) {
    throw new Error(
      result?.message ||
      result?.error?.message ||
      `Request failed: ${response.status}`
    )
  }

  return result
}

export async function runAnalysis(latitude, longitude) {
  const result = await requestJson(`${API_BASE_URL}/api/v1/analysis`, {
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

  return result?.data || result
}

export async function getAnalysis(analysisId) {
  const result = await requestJson(
    `${API_BASE_URL}/api/v1/analysis/${encodeURIComponent(analysisId)}`
  )

  return result?.data || result
}
