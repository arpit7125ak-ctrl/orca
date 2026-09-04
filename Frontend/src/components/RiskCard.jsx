function RiskCard({ data }) {
  const risk = data || {}

  const riskLevel = risk.level ?? 'UNKNOWN'

  return (
    <div className="rounded-2xl border border-orange-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">

        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-orange-400/70">
            Threat Intelligence
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Marine Risk
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-orange-400/10 text-orange-300">
          !
        </div>

      </div>

      <div className="flex items-center justify-between rounded-xl border border-orange-400/10 bg-orange-400/[0.03] p-5">

        <div>
          <p className="text-xs text-slate-500">
            Current Risk Level
          </p>

          <p className="mt-2 text-3xl font-bold text-orange-200">
            {riskLevel}
          </p>
        </div>

        <div className="flex h-14 w-14 items-center justify-center rounded-full border-4 border-orange-400/20">
          <span className="text-sm font-bold text-orange-300">
            {risk.score ?? '--'}
          </span>
        </div>

      </div>

      <p className="mt-4 text-sm leading-6 text-slate-500">
        {risk.summary ??
          'Risk assessment will appear here once environmental and ecosystem data are available.'}
      </p>

      <div className="mt-5 grid grid-cols-2 gap-4">

        <div>
          <p className="text-xs text-slate-500">
            Risk Score
          </p>

          <p className="mt-1 text-lg font-semibold text-white">
            {risk.score ?? '--'}
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Confidence
          </p>

          <p className="mt-1 text-lg font-semibold text-white">
            {risk.confidence ?? '--'}
          </p>
        </div>

      </div>

    </div>
  )
}

export default RiskCard