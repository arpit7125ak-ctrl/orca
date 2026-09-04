function EcosystemCard({ data }) {
  const ecosystem = data || {}

  return (
    <div className="rounded-2xl border border-emerald-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-emerald-400/70">
            Marine Biology
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Ecosystem Health
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-400/10 text-emerald-300">
          ◌
        </div>
      </div>

      <div className="space-y-5">

        <div>
          <div className="flex items-center justify-between">
            <p className="text-xs text-slate-500">
              Overall Health
            </p>

            <p className="text-sm font-semibold text-emerald-300">
              {ecosystem.overall_health ?? '--'}
            </p>
          </div>

          <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
            <div
              className="h-full rounded-full bg-gradient-to-r from-emerald-600 to-emerald-300 transition-all"
              style={{
                width: `${ecosystem.health_score ?? 0}%`,
              }}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">

          <div className="rounded-xl border border-emerald-400/10 bg-emerald-400/[0.03] p-4">
            <p className="text-xs text-slate-500">
              Biodiversity
            </p>

            <p className="mt-2 text-xl font-semibold text-emerald-100">
              {ecosystem.biodiversity ?? '--'}
            </p>
          </div>

          <div className="rounded-xl border border-emerald-400/10 bg-emerald-400/[0.03] p-4">
            <p className="text-xs text-slate-500">
              Productivity
            </p>

            <p className="mt-2 text-xl font-semibold text-emerald-100">
              {ecosystem.productivity ?? '--'}
            </p>
          </div>

        </div>

      </div>
    </div>
  )
}

export default EcosystemCard