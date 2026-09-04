function EcosystemCard({ data }) {
  const ecosystem = data || {}

  const healthScore =
    typeof ecosystem.health_score === 'number'
      ? ecosystem.health_score
      : 0

  return (
    <div className="rounded-2xl border border-emerald-500/20 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-emerald-400">
        Marine Biology
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Ecosystem Health
      </h2>

      <div className="mt-8">

        <div className="flex justify-between">
          <p className="text-sm text-slate-500">
            Overall Health
          </p>

          <p className="font-bold">
            {ecosystem.overall_health ?? '--'}
          </p>
        </div>

        <div className="mt-4 h-2 rounded-full bg-slate-800">
          <div
            className="h-2 rounded-full bg-emerald-400"
            style={{ width: `${healthScore}%` }}
          />
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4">

          <div className="rounded-xl border border-emerald-500/20 p-5">
            <p className="text-sm text-slate-500">
              Biodiversity
            </p>

            <p className="mt-2 text-2xl font-bold">
              {ecosystem.biodiversity ?? '--'}
            </p>
          </div>

          <div className="rounded-xl border border-emerald-500/20 p-5">
            <p className="text-sm text-slate-500">
              Productivity
            </p>

            <p className="mt-2 text-2xl font-bold">
              {ecosystem.productivity ?? '--'}
            </p>
          </div>

        </div>
      </div>
    </div>
  )
}

export default EcosystemCard