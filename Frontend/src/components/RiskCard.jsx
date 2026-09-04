function RiskCard({ data }) {
  const risk = data || {}

  return (
    <div className="rounded-2xl border border-orange-500/20 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-orange-400">
        Threat Intelligence
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Marine Risk
      </h2>

      <div className="mt-8 rounded-xl border border-orange-500/20 p-6">

        <p className="text-sm text-slate-500">
          Current Risk Level
        </p>

        <div className="mt-2 flex items-center justify-between">
          <p className="text-3xl font-bold">
            {risk.level ?? '--'}
          </p>

          <div className="flex h-16 w-16 items-center justify-center rounded-full border-4 border-orange-500/30">
            <span className="font-bold">
              {risk.score ?? '--'}
            </span>
          </div>
        </div>

      </div>

      <p className="mt-6 text-slate-400">
        {risk.summary ?? '--'}
      </p>

      <div className="mt-6 grid grid-cols-2 gap-6">

        <div>
          <p className="text-sm text-slate-500">
            Risk Score
          </p>

          <p className="mt-2 text-2xl font-bold">
            {risk.score ?? '--'}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Confidence
          </p>

          <p className="mt-2 text-2xl font-bold">
            {risk.confidence ?? '--'}
          </p>
        </div>

      </div>
    </div>
  )
}

export default RiskCard