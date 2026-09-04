function AnalysisPanel({ data }) {
  const quality = data?.dataQuality
  const trace = data?.agentTrace

  return (
    <div className="rounded-2xl border border-slate-700 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        Analysis
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Intelligence Assessment
      </h2>

      <p className="mt-6 text-slate-400">
        {data?.decision?.recommendation ??
          'Assessment will appear when analysis results are available.'}
      </p>

      <div className="mt-8 grid grid-cols-2 gap-6">
        <div>
          <p className="text-sm text-slate-500">
            Data Quality
          </p>

          <p className="mt-2 text-xl font-bold">
            {quality ?? '--'}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Confidence
          </p>

          <p className="mt-2 text-xl font-bold">
            {data?.decision?.confidence ?? '--'}
          </p>
        </div>
      </div>

      {trace && (
        <div className="mt-6">
          <p className="text-sm text-slate-500">
            Agent Trace
          </p>

          <p className="mt-2 text-sm text-slate-400">
            Analysis reasoning trace available.
          </p>
        </div>
      )}
    </div>
  )
}

export default AnalysisPanel