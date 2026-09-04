import Sidebar from '../components/Sidebar.jsx'
import MapView from '../components/MapView.jsx'
import WeatherCard from '../components/WeatherCard.jsx'
import OceanCard from '../components/OceanCard.jsx'
import EcosystemCard from '../components/EcosystemCard.jsx'
import RiskCard from '../components/RiskCard.jsx'
import AgentStatus from '../components/AgentStatus.jsx'
import DecisionPanel from '../components/DecisionPanel.jsx'
import AnalysisPanel from '../components/AnalysisPanel.jsx'
import ChatBox from '../components/ChatBox.jsx'

function Dashboard({ zone }) {
  return (
    <div className="flex">
      <Sidebar />

      <main className="flex-1 p-6">

        <div className="mb-6">
          <p className="text-sm uppercase tracking-widest text-cyan-400">
            Marine Intelligence
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Marine Analysis Dashboard
          </h1>

          {zone && (
            <p className="mt-2 text-sm text-cyan-400">
              Analysis Zone: {zone.latitude.toFixed(4)}° N, {zone.longitude.toFixed(4)}° E
            </p>
          )}

          <p className="mt-2 text-slate-400">
            Monitor marine conditions, ecosystem health and risk.
          </p>
        </div>

      <MapView zone={zone} />

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <WeatherCard />
          <OceanCard />
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <EcosystemCard />
          <RiskCard />
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <AgentStatus />
          <DecisionPanel />
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <AnalysisPanel />
          <ChatBox />
        </div>

      </main>
    </div>
  )
}

export default Dashboard