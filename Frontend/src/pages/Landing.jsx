function Landing({ onEnter }) {
  return (
    <main className="relative flex min-h-[calc(100vh-4rem)] items-center justify-center overflow-hidden px-6">

      {/* Aurora background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[15%] top-[20%] h-72 w-72 rounded-full bg-violet-600/10 blur-[120px]" />
        <div className="absolute bottom-[10%] right-[15%] h-80 w-80 rounded-full bg-emerald-500/10 blur-[130px]" />
        <div className="absolute left-[45%] top-[35%] h-64 w-64 rounded-full bg-fuchsia-500/5 blur-[110px]" />
      </div>

      <div className="relative z-10 max-w-4xl text-center">

        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-400/5 px-4 py-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />

          <span className="text-xs uppercase tracking-[0.25em] text-violet-300">
            Marine Intelligence Platform
          </span>
        </div>

        <h1 className="bg-gradient-to-r from-white via-violet-200 to-emerald-200 bg-clip-text text-7xl font-black tracking-tight text-transparent md:text-8xl">
          ORCA
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-xl font-medium text-slate-300">
          Marine EcOsystem Reasoning with
          <span className="text-violet-300"> Collaborative Agents</span>
        </p>

        <p className="mx-auto mt-5 max-w-xl text-sm leading-7 text-slate-500">
          Understand marine conditions, ecosystem health and environmental
          risks through coordinated intelligent analysis.
        </p>

        <button
          onClick={onEnter}
          className="mt-10 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-8 py-3.5 font-semibold text-white shadow-xl shadow-violet-500/20 transition duration-300 hover:-translate-y-0.5 hover:from-violet-400 hover:to-fuchsia-400"
        >
          Enter ORCA Dashboard
        </button>

      </div>
    </main>
  )
}

export default Landing