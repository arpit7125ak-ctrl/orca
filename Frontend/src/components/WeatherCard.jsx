function WeatherCard({ data }) {
  const weather = data || {}

  return (
    <div className="rounded-2xl border border-amber-500/20 bg-[#111116] p-6">
      <p className="text-sm uppercase tracking-widest text-amber-400">
        Atmosphere
      </p>

      <h2 className="mt-2 text-2xl font-bold">
        Weather
      </h2>

      <div className="mt-8 grid grid-cols-2 gap-8">

        <div>
          <p className="text-sm text-slate-500">
            Temperature
          </p>
          <p className="mt-2 text-3xl font-bold">
            {weather.temperature_2m ?? '--'}
            <span className="text-sm"> °C</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Wind Speed
          </p>
          <p className="mt-2 text-3xl font-bold">
            {weather.wind_speed_10m ?? '--'}
            <span className="text-sm"> km/h</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Pressure
          </p>
          <p className="mt-2 text-2xl font-bold">
            {weather.pressure_msl ?? '--'}
            <span className="text-sm"> hPa</span>
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            Weather Code
          </p>
          <p className="mt-2 text-2xl font-bold">
            {weather.weather_code ?? '--'}
          </p>
        </div>

      </div>
    </div>
  )
}

export default WeatherCard