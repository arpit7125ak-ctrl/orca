function DecisionPanel({ data }) {
  const decision = data?.decision || data?.overallDecision || null

  return (
    <div className="rounded-2xl border border-purple-900/40 bg-[#020817] p-7">
      <p className="text-sm uppercase tracking-widest text-purple-400">
        Decision Intelligence
      </p>

      <h2 className="mt-3 text-3xl font-bold">
        Recommended Decision
      </h2>

      {decision ? (
        <>
          <p className="mt-6 text-2xl font-semibold text-cyan-400">
            {decision.recommendation || '--'}
          </p>

          {decision.key_reasons?.length > 0 && (
            <div className="mt-5">
              <p className="text-slate-400">Key Reasons</p>

              <ul className="mt-3 space-y-2">
                {decision.key_reasons.map((reason, index) => (
                  <li key={index} className="text-slate-200">
                    • {reason}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-6">
            <p className="text-slate-400">Confidence</p>
            <p className="mt-1 text-xl">
              {decision.confidence ?? '--'}
            </p>
          </div>
        </>
      ) : (
        <p className="mt-6 text-slate-400">
          Decision will appear when AI analysis is available.
        </p>
      )}
    </div>
  )
}

export default DecisionPanel