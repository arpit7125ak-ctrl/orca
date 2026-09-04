function Navbar() {
  return (
    <nav className="border-b border-[#E9E2CC]/25 bg-[#0B2545]">
      <div className="flex min-h-16 items-center justify-between px-5">

        <div className="flex items-center gap-4">

          <div className="relative flex h-9 w-9 items-center justify-center border border-[#E9E2CC]/50 bg-[#1B4965]">
            <span className="text-sm font-bold text-[#E9E2CC]">
              O
            </span>

            <span className="absolute -bottom-1 -right-1 h-2 w-2 bg-[#1E7A4C]" />
          </div>

          <div>
            <h1 className="text-lg font-semibold tracking-wide text-[#E9E2CC]">
              ORCA
            </h1>

            <p className="text-[10px] tracking-wide text-[#E9E2CC]/55">
              MARINE ECOSYSTEM REASONING
            </p>
          </div>

        </div>

        <div className="flex items-center gap-1">

          <button className="border border-[#E9E2CC]/20 bg-[#1B4965] px-4 py-2 text-sm text-[#E9E2CC]">
            Dashboard
          </button>

          <button className="px-4 py-2 text-sm text-[#E9E2CC]/60 hover:text-[#E9E2CC]">
            Analysis
          </button>

          <button className="px-4 py-2 text-sm text-[#E9E2CC]/60 hover:text-[#E9E2CC]">
            About
          </button>

        </div>

      </div>
    </nav>
  )
}

export default Navbar