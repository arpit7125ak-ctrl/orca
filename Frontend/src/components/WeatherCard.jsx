function WeatherCard({ data }) {
  const weather = data || {}

  return (
    <div className="rounded-2xl border border-amber-400/10 bg-[#111116] p-5 shadow-xl shadow-black/20">

      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-amber-400/70">
            Atmosphere
          </p>

          <h2 className="mt-1 text-lg font-semibold text-white">
            Weather
          </h2>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-amber-400/10 text-amber-300">
          ☀
        </div>
      </div>

      <div className="grid grid-cols-2 gap-x-6 gap-y-5">

        <div>
          <p className="text-xs text-slate-500">
            Temperature
          </p>

          <p className="mt-1 text-2xl font-semibold text-amber-100">
            {weather.temperature ?? '--'}°
            <span className="text-sm text-slate-500"> C</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Wind Speed
          </p>

          <p className="mt-1 text-2xl font-semibold text-white">
            {weather.wind_speed ?? '--'}
            <span className="text-sm text-slate-500"> km/h</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Pressure
          </p>

          <p className="mt-1 text-lg font-semibold text-white">
            {weather.pressure ?? '--'}
            <span className="text-xs text-slate-500"> hPa</span>
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Conditions
          </p>

          <p className="mt-1 text-sm font-medium text-amber-300">
            {weather.conditions ?? 'Awaiting data'}
          </p>
        </div>

      </div>
    </div>
  )
}

export default WeatherCard