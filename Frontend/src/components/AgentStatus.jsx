function AgentStatus({ data }) {
  const agents = [
    ['Weather Agent', data?.weather],
    ['Ocean Agent', data?.ocean],
    ['Ecosystem Agent', data?.ecosystem],
    ['Risk Agent', data?.risk],
    ['Decision Agent', data?.decision],
  ]

  return (
    <div className="rounded-2xl border border-slate-700 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        AI System
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Agent Status
      </h2>

      <div className="mt-6 space-y-4">
        {agents.map(([name, result]) => (
          <div
            key={name}
            className="flex items-center justify-between rounded-xl border border-slate-800 p-4"
          >
            <span>{name}</span>

            <span
              className={
                result
                  ? 'text-emerald-400'
                  : 'text-slate-500'
              }
            >
              {result ? 'Available' : 'Waiting'}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AgentStatus