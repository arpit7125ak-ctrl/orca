function ChatBox() {
  return (
    <div className="rounded-2xl border border-fuchsia-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">

        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-fuchsia-400/70">
            ORCA Assistant
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Ask ORCA
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-fuchsia-400/10 text-fuchsia-300">
          ✦
        </div>

      </div>

      <div className="mb-4 h-48 overflow-y-auto rounded-xl border border-white/5 bg-black/20 p-4">

        <div className="max-w-[90%] rounded-xl border border-fuchsia-400/10 bg-fuchsia-400/[0.03] p-4">

          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-fuchsia-400" />

            <p className="text-[10px] font-semibold uppercase tracking-wider text-fuchsia-300">
              ORCA
            </p>
          </div>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Ask me about marine conditions, ecosystem health,
            risks, or recommendations.
          </p>

        </div>

      </div>

      <div className="flex gap-2">

        <input
          type="text"
          placeholder="Ask about this marine zone..."
          className="min-w-0 flex-1 rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-700 focus:border-fuchsia-400/40"
        />

        <button className="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-fuchsia-500/10 transition hover:from-violet-400 hover:to-fuchsia-400">
          Send
        </button>

      </div>

    </div>
  )
}

export default ChatBox