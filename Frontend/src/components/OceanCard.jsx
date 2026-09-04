function OceanCard({ data }) {
  const ocean = data || {}

  return (
    <div className="rounded-2xl border border-teal-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-teal-400/70">
            Oceanographic
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Ocean Conditions
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-400/10 text-teal-300">
          ≋
        </div>
      </div>

      <div className="grid grid-cols-2 gap-x-6 gap-y-5">

        <div>
          <p className="text-xs text-slate-500">
            Sea Surface Temp.
          </p>

          <p className="mt-1 text-2xl font-semibold text-teal-100">
            {ocean.sea_surface_temperature ?? '--'}
            <span className="text-sm text-slate-500"> °C</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Wave Height
          </p>

          <p className="mt-1 text-2xl font-semibold text-white">
            {ocean.wave_height ?? '--'}
            <span className="text-sm text-slate-500"> m</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Current Speed
          </p>

          <p className="mt-1 text-lg font-semibold text-white">
            {ocean.current_speed ?? '--'}
            <span className="text-xs text-slate-500"> m/s</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Salinity
          </p>

          <p className="mt-1 text-lg font-semibold text-white">
            {ocean.salinity ?? '--'}
            <span className="text-xs text-slate-500"> PSU</span>
          </p>
        </div>

      </div>
    </div>
  )
}

export default OceanCard