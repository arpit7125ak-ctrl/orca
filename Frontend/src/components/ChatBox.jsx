import { useState } from 'react'

function ChatBox() {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!message.trim()) return

    setMessage('')
  }

  return (
    <div className="rounded-2xl border border-slate-700 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        ORCA Assistant
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Marine Intelligence Chat
      </h2>

      <div className="mt-6 rounded-xl border border-slate-800 p-4">
        <p className="text-sm text-slate-300">
          ORCA is ready to answer questions about the current marine analysis.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 flex gap-3">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about this analysis..."
          className="flex-1 rounded-xl border border-slate-700 bg-[#0b0b10] px-4 py-3 text-white outline-none"
        />

        <button
          type="submit"
          className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-black"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatBox