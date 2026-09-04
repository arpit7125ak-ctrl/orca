function AgentStatus({ data, loading }) {
  const zone = data?.zones?.[0]

  const agents = [
    {
      name: 'Weather Agent',
      status: zone?.weather ? 'Completed' : loading ? 'Processing' : 'Waiting',
    },
    {
      name: 'Ocean Agent',
      status: zone?.ocean ? 'Completed' : loading ? 'Processing' : 'Waiting',
    },
    {
      name: 'Ecosystem Agent',
      status: zone?.ecosystem ? 'Completed' : loading ? 'Processing' : 'Waiting',
    },
    {
      name: 'Risk Agent',
      status: zone?.risk ? 'Completed' : loading ? 'Processing' : 'Waiting',
    },
    {
      name: 'Decision Agent',
      status: data?.decision ? 'Completed' : loading ? 'Processing' : 'Waiting',
    },
  ]

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
      <p className="text-sm uppercase tracking-widest text-purple-400">
        AI Agents
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Agent Status
      </h2>

      <div className="mt-6 space-y-3">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className="flex items-center justify-between rounded-lg border border-slate-800 p-4"
          >
            <span className="text-slate-200">
              {agent.name}
            </span>

            <span
              className={
                agent.status === 'Completed'
                  ? 'text-green-400'
                  : agent.status === 'Processing'
                    ? 'text-yellow-400'
                    : 'text-slate-500'
              }
            >
              {agent.status}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

export default AgentStatus