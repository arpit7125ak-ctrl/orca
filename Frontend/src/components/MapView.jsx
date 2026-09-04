import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

function MapView({ zone }) {
  const center = zone
    ? [zone.latitude, zone.longitude]
    : [20.5937, 78.9629]

  return (
    <div className="h-[500px] w-full overflow-hidden rounded-xl border border-slate-800">
      <MapContainer
        center={center}
        zoom={zone ? 6 : 5}
        className="h-full w-full"
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <Marker position={center}>
          <Popup>
            ORCA Marine Analysis Zone
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  )
}

export default MapView