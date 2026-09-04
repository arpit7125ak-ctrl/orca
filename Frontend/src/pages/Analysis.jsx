import { useState } from 'react'

function Analysis({ onAnalyze, loading, error }) {
  const [latitude, setLatitude] = useState('')
  const [longitude, setLongitude] = useState('')

  const handleAnalyze = (event) => {
    event.preventDefault()

    const lat = Number(latitude)
    const lon = Number(longitude)

    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      return
    }

    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      return
    }

    onAnalyze({
      latitude: lat,
      longitude: lon,
    })
  }

  return (
    <main className="relative flex min-h-[calc(100vh-4rem)] items-center justify-center overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[15%] top-[20%] h-72 w-72 rounded-full bg-violet-600/10 blur-[120px]" />
        <div className="absolute bottom-[10%] right-[15%] h-80 w-80 rounded-full bg-emerald-500/10 blur-[130px]" />
      </div>

      <section className="relative z-10 w-full max-w-2xl rounded-2xl border border-white/10 bg-[#0b0b10]/80 p-8 shadow-2xl backdrop-blur-xl">
        <p className="text-sm uppercase tracking-widest text-cyan-400">
          Marine Analysis
        </p>

        <h1 className="mt-3 text-4xl font-bold">
          Analyze Marine Zone
        </h1>

        <p className="mt-3 text-slate-400">
          Enter the coordinates of the marine zone you want ORCA to analyze.
        </p>

        <form onSubmit={handleAnalyze} className="mt-8 space-y-5">
          <div>
            <label className="mb-2 block text-sm text-slate-400">
              Latitude
            </label>
            <input
              type="number"
              step="any"
              min="-90"
              max="90"
              value={latitude}
              onChange={(event) => setLatitude(event.target.value)}
              placeholder="e.g. 15.5000"
              className="w-full rounded-xl border border-slate-700 bg-[#0b0b10] px-4 py-3 text-white outline-none"
              required
            />
          </div>

          <div>
            <label className="mb-2 block text-sm text-slate-400">
              Longitude
            </label>
            <input
              type="number"
              step="any"
              min="-180"
              max="180"
              value={longitude}
              onChange={(event) => setLongitude(event.target.value)}
              placeholder="e.g. 72.5000"
              className="w-full rounded-xl border border-slate-700 bg-[#0b0b10] px-4 py-3 text-white outline-none"
              required
            />
          </div>

          {error && (
            <p className="text-sm text-orange-400">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-8 py-3.5 font-semibold text-white shadow-xl shadow-violet-500/20 transition duration-300 hover:-translate-y-0.5 disabled:translate-y-0 disabled:opacity-60"
          >
            {loading ? 'Analyzing Marine Zone...' : 'Analyze Marine Zone'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default Analysis
