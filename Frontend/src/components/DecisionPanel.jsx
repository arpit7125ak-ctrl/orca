function DecisionPanel({ data }) {
  const decision = data || {}

  return (
    <div className="rounded-2xl border border-cyan-500/20 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        Decision Intelligence
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Overall Decision
      </h2>

      <div className="mt-8">
        <p className="text-3xl font-bold">
          {decision.recommendation ?? '--'}
        </p>

        <div className="mt-6">
          <p className="text-sm text-slate-500">
            Key Reasons
          </p>

          {decision.key_reasons?.length ? (
            <ul className="mt-3 space-y-2">
              {decision.key_reasons.map((reason, index) => (
                <li key={index} className="text-slate-300">
                  • {reason}
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-3 text-slate-500">--</p>
          )}
        </div>

        <div className="mt-6">
          <p className="text-sm text-slate-500">
            Confidence
          </p>

          <p className="mt-2 text-2xl font-bold">
            {decision.confidence ?? '--'}
          </p>
        </div>

        {decision.limitations?.length > 0 && (
          <div className="mt-6">
            <p className="text-sm text-slate-500">
              Limitations
            </p>

            <ul className="mt-3 space-y-2">
              {decision.limitations.map((item, index) => (
                <li key={index} className="text-sm text-orange-300">
                  • {item}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default DecisionPanel