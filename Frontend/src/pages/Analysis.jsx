import { useState } from 'react'

function Analysis({ onAnalyze }) {
  const [latitude, setLatitude] = useState('')
  const [longitude, setLongitude] = useState('')

  const handleAnalyze = () => {
    if (!latitude || !longitude) {
      alert('Please enter both latitude and longitude.')
      return
    }

    onAnalyze({
      latitude: Number(latitude),
      longitude: Number(longitude),
    })
  }

  return (
    <main className="min-h-[calc(100vh-4rem)] p-6">
      <div className="mx-auto max-w-6xl">

        <div className="mb-8">
          <p className="text-sm uppercase tracking-widest text-cyan-400">
            ORCA Analysis
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Start Marine Analysis
          </h1>

          <p className="mt-2 text-slate-400">
            Select a marine zone and provide the information required
            for collaborative environmental analysis.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">

          <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
            <p className="text-xs uppercase tracking-widest text-slate-500">
              Analysis Zone
            </p>

            <h2 className="mt-2 text-xl font-semibold">
              Select Location
            </h2>

            <div className="mt-6 space-y-4">

              <div>
                <label className="mb-2 block text-sm text-slate-400">
                  Latitude
                </label>

                <input
                  type="number"
                  value={latitude}
                  onChange={(e) => setLatitude(e.target.value)}
                  placeholder="e.g. 15.0000"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-400">
                  Longitude
                </label>

                <input
                  type="number"
                  value={longitude}
                  onChange={(e) => setLongitude(e.target.value)}
                  placeholder="e.g. 72.0000"
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-cyan-500"
                />
              </div>

              <button
                onClick={handleAnalyze}
                className="w-full rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
              >
                Analyze Marine Zone
              </button>

            </div>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
            <p className="text-xs uppercase tracking-widest text-slate-500">
              Analysis Workflow
            </p>

            <h2 className="mt-2 text-xl font-semibold">
              Collaborative Intelligence
            </h2>

            <div className="mt-6 space-y-3">

              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
                <p className="font-medium">01 — Weather Agent</p>
                <p className="mt-1 text-xs text-slate-500">
                  Atmospheric conditions
                </p>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
                <p className="font-medium">02 — Ocean Agent</p>
                <p className="mt-1 text-xs text-slate-500">
                  Oceanographic conditions
                </p>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
                <p className="font-medium">03 — Ecosystem Agent</p>
                <p className="mt-1 text-xs text-slate-500">
                  Ecosystem health
                </p>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
                <p className="font-medium">04 — Risk Agent</p>
                <p className="mt-1 text-xs text-slate-500">
                  Marine risk assessment
                </p>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
                <p className="font-medium">05 — Decision Agent</p>
                <p className="mt-1 text-xs text-slate-500">
                  Final recommendation
                </p>
              </div>

            </div>
          </div>

        </div>
      </div>
    </main>
  )
}

export default Analysis