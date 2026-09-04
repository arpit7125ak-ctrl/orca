function DecisionPanel() {
  return (
    <div className="rounded-2xl border border-amber-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-amber-400/70">
            Intelligence Output
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Final Decision
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-amber-400/10 text-amber-300">
          ✦
        </div>
      </div>

      <div className="relative overflow-hidden rounded-xl border border-amber-400/10 bg-gradient-to-br from-amber-400/[0.06] to-transparent p-6">

        <div className="absolute right-0 top-0 h-32 w-32 rounded-full bg-amber-400/5 blur-3xl" />

        <div className="relative">
          <p className="text-[10px] uppercase tracking-[0.2em] text-slate-600">
            Recommendation
          </p>

          <p className="mt-3 text-2xl font-bold text-amber-100">
            Awaiting Analysis
          </p>

          <p className="mt-3 max-w-md text-sm leading-6 text-slate-500">
            The collaborative agents will generate a recommendation
            after environmental and ecosystem data are analyzed.
          </p>

          <div className="mt-6 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-slate-600" />

            <span className="text-xs text-slate-600">
              Decision engine idle
            </span>
          </div>
        </div>

      </div>

    </div>
  )
}

export default DecisionPanel