function Sidebar() {
  return (
    <aside className="hidden min-h-[calc(100vh-4rem)] w-64 shrink-0 border-r border-white/10 bg-[#0b0b10]/80 p-4 backdrop-blur-xl lg:block">

      <div className="mb-7 px-3">
        <p className="text-[10px] font-semibold uppercase tracking-[0.25em] text-slate-600">
          Workspace
        </p>
      </div>

      <nav className="space-y-1">

        <button className="group flex w-full items-center gap-3 rounded-xl border border-violet-400/10 bg-violet-500/10 px-4 py-3 text-left">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-500/15 text-violet-300">
            ◈
          </span>

          <div>
            <p className="text-sm font-medium text-white">
              Dashboard
            </p>

            <p className="text-[10px] text-violet-300/60">
              Overview
            </p>
          </div>
        </button>

        <button className="group flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left transition hover:bg-white/[0.04]">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-400/10 text-teal-300">
            ◉
          </span>

          <div>
            <p className="text-sm font-medium text-slate-300">
              Marine Analysis
            </p>

            <p className="text-[10px] text-slate-600">
              Environmental data
            </p>
          </div>
        </button>

        <button className="group flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left transition hover:bg-white/[0.04]">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-400/10 text-orange-300">
            !
          </span>

          <div>
            <p className="text-sm font-medium text-slate-300">
              Risk Assessment
            </p>

            <p className="text-[10px] text-slate-600">
              Threat analysis
            </p>
          </div>
        </button>

        <button className="group flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left transition hover:bg-white/[0.04]">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-400/10 text-emerald-300">
            ◌
          </span>

          <div>
            <p className="text-sm font-medium text-slate-300">
              Ecosystem
            </p>

            <p className="text-[10px] text-slate-600">
              Marine health
            </p>
          </div>
        </button>

        <button className="group flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left transition hover:bg-white/[0.04]">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-fuchsia-400/10 text-fuchsia-300">
            ✦
          </span>

          <div>
            <p className="text-sm font-medium text-slate-300">
              AI Agents
            </p>

            <p className="text-[10px] text-slate-600">
              Collaborative reasoning
            </p>
          </div>
        </button>

      </nav>

      <div className="mt-auto pt-10">
        <div className="rounded-xl border border-white/5 bg-white/[0.02] p-4">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/50" />

            <span className="text-xs font-medium text-slate-300">
              ORCA System
            </span>
          </div>

          <p className="mt-2 text-[10px] leading-5 text-slate-600">
            Collaborative marine intelligence
          </p>
        </div>
      </div>

    </aside>
  )
}

export default Sidebar