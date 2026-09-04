function OceanCard({ data }) {
  const ocean = data || {}

  return (
    <div className="rounded-2xl border border-cyan-500/20 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-cyan-400">
        Oceanographic
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Ocean Conditions
      </h2>

      <div className="mt-8 grid grid-cols-2 gap-8">

        <div>
          <p className="text-sm text-slate-500">
            Sea Surface Temp.
          </p>
          <p className="mt-2 text-3xl font-bold">
            {ocean.sea_surface_temperature ?? '--'}
            <span className="text-sm"> °C</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Wave Height
          </p>
          <p className="mt-2 text-3xl font-bold">
            {ocean.wave_height ?? '--'}
            <span className="text-sm"> m</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Current Speed
          </p>
          <p className="mt-2 text-2xl font-bold">
            {ocean.current_speed ?? '--'}
            <span className="text-sm"> m/s</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Salinity
          </p>
          <p className="mt-2 text-2xl font-bold">
            {ocean.salinity ?? '--'}
            <span className="text-sm"> PSU</span>
          </p>
        </div>

      </div>
    </div>
  )
}

export default OceanCard