function AgentStatus() {
  const agents = [
    {
      name: 'Weather Agent',
      description: 'Atmospheric conditions',
      color: 'amber',
      icon: '☀',
    },
    {
      name: 'Ocean Agent',
      description: 'Oceanographic conditions',
      color: 'teal',
      icon: '≋',
    },
    {
      name: 'Ecosystem Agent',
      description: 'Marine ecosystem health',
      color: 'emerald',
      icon: '◌',
    },
    {
      name: 'Risk Agent',
      description: 'Threat assessment',
      color: 'orange',
      icon: '!',
    },
    {
      name: 'Decision Agent',
      description: 'Final recommendation',
      color: 'violet',
      icon: '✦',
    },
  ]

  return (
    <div className="rounded-2xl border border-violet-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-violet-400/70">
            Multi-Agent System
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Collaborative Agents
          </h2>
        </div>

        <div className="rounded-lg border border-violet-400/10 bg-violet-400/5 px-3 py-2">
          <span className="text-xs text-violet-300">
            5 Agents
          </span>
        </div>
      </div>

      <div className="space-y-2">
        {agents.map((agent, index) => (
          <div
            key={agent.name}
            className="flex items-center gap-3 rounded-xl border border-white/5 bg-white/[0.02] p-3"
          >

            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-violet-400/10 text-sm text-violet-300">
              {agent.icon}
            </div>

            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium text-slate-200">
                {agent.name}
              </p>

              <p className="mt-0.5 text-[10px] text-slate-600">
                {agent.description}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-slate-600" />

              <span className="text-[10px] text-slate-600">
                Waiting
              </span>
            </div>

            <span className="text-[10px] text-slate-700">
              0{index + 1}
            </span>

          </div>
        ))}
      </div>

    </div>
  )
}

export default AgentStatus