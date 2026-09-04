function AnalysisPanel() {
  return (
    <div className="rounded-2xl border border-violet-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-violet-400/70">
            Intelligence
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Environmental Analysis
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-400/10 text-violet-300">
          ◇
        </div>
      </div>

      <div className="rounded-xl border border-violet-400/10 bg-violet-400/[0.02] p-5">
        <p className="text-[10px] uppercase tracking-[0.2em] text-slate-600">
          Current Assessment
        </p>

        <p className="mt-3 text-sm leading-6 text-slate-400">
          Environmental analysis will appear here after ORCA processes
          the selected marine zone.
        </p>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3">

        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <p className="text-[10px] uppercase tracking-wider text-slate-600">
            Data Quality
          </p>

          <p className="mt-2 text-2xl font-semibold text-violet-200">
            --
          </p>
        </div>

        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <p className="text-[10px] uppercase tracking-wider text-slate-600">
            Confidence
          </p>

          <p className="mt-2 text-2xl font-semibold text-violet-200">
            --
          </p>
        </div>

      </div>

    </div>
  )
}

export default AnalysisPanel