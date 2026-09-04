import { useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Landing from './pages/Landing.jsx'
import Analysis from './pages/Analysis.jsx'
import Dashboard from './pages/Dashboard.jsx'
import useAnalysis from './hooks/useAnalysis.js'

function App() {
  const [page, setPage] = useState('landing')
  const [selectedZone, setSelectedZone] = useState(null)

  const {
    data: analysisData,
    loading,
    error,
    analyze,
  } = useAnalysis()

  const handleAnalyze = async (zone) => {
    setSelectedZone(zone)
    setPage('dashboard')

    try {
      await analyze(zone.latitude, zone.longitude)
    } catch (err) {
      console.error('Analysis failed:', err)
    }
  }

  return (
    <div className="min-h-screen text-[#E9E2CC]">
      <Navbar />

      {page === 'landing' && (
        <Landing onEnter={() => setPage('analysis')} />
      )}

      {page === 'analysis' && (
        <Analysis onAnalyze={handleAnalyze} />
      )}

      {page === 'dashboard' && (
        <Dashboard
          zone={selectedZone}
          data={analysisData}
          loading={loading}
          error={error}
        />
      )}
    </div>
  )
}

export default App