import { useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Landing from './pages/Landing.jsx'
import Analysis from './pages/Analysis.jsx'
import Dashboard from './pages/Dashboard.jsx'

function App() {
  const [page, setPage] = useState('landing')
  const [selectedZone, setSelectedZone] = useState(null)

  const handleAnalyze = (zone) => {
    setSelectedZone(zone)
    setPage('dashboard')
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
        <Dashboard zone={selectedZone} />
      )}
    </div>
  )
}

export default App