function AnalysisPanel({ data }) {
  const decision = data?.overallDecision

  return (
    <div className="rounded-2xl border border-slate-700 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        Analysis
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Intelligence Assessment
      </h2>

      <p className="mt-6 text-slate-400">
        {decision?.recommendation ?? '--'}
      </p>

      <div className="mt-8 grid grid-cols-2 gap-6">
        <div>
          <p className="text-sm text-slate-500">
            Data Quality
          </p>

          <p className="mt-2 text-xl font-bold">
            {data?.dataQuality ?? '--'}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Confidence
          </p>

          <p className="mt-2 text-xl font-bold">
            {decision?.confidence ?? '--'}
          </p>
        </div>
      </div>
    </div>
  )
}

export default AnalysisPanel