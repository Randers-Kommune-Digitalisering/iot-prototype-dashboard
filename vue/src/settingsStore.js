import { reactive } from 'vue'

const defaultSettings = {
  thresholds: {
    battery: { warning: 20, error: 5 },
    rssi: { warning: -85, error: -100 },
    lastSeen: { warning: 24, offline: 72 } // in hours
  },
  developerMode: true,
  deviceModels: []
}

const state = reactive({
  loaded: false,
  values: defaultSettings
})

async function loadSettingsFromServer(url = '/api/settings') {
  try {
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to load settings')
    const data = await res.json()
    // shallow merge: keep missing defaults
    state.values = { ...defaultSettings, ...data }
  } catch (e) {
    console.warn('Settings load failed, using defaults', e)
  } finally {
    state.loaded = true
  }
}

export function useSettings() {
  return { state, loadSettingsFromServer }
}

export default { state, loadSettingsFromServer }
