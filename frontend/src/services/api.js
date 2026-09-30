const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const KEY = import.meta.env.VITE_API_KEY || 'dev-plant-api-key'
async function request(path, options={}) {
  const headers = {'Content-Type':'application/json', ...(options.method && options.method !== 'GET' ? {'X-API-Key':KEY}:{}), ...(options.headers||{})}
  const res = await fetch(`${API}${path}`, {...options, headers})
  const data = await res.json().catch(()=>({detail:'Invalid server response'}))
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`)
  return data
}
export const api = {
  latest: id => request(`/api/devices/${id}/latest`),
  history: id => request(`/api/devices/${id}/history?limit=60`),
  alerts: id => request(`/api/alerts?device_id=${encodeURIComponent(id)}`),
  events: id => request(`/api/devices/${id}/watering-history`),
  analytics: id => request(`/api/analytics/${id}`),
  automation: (id,enabled) => request(`/api/devices/${id}/automation`, {method:'PUT',body:JSON.stringify({enabled})}),
  threshold: (id,value) => request(`/api/devices/${id}/threshold`, {method:'PUT',body:JSON.stringify({moisture_threshold:value})}),
  water: (id,duration=5) => request(`/api/devices/${id}/water`, {method:'POST',body:JSON.stringify({duration_seconds:duration})}),
  acknowledge: id => request(`/api/alerts/${id}/acknowledge`, {method:'PUT'})
}
