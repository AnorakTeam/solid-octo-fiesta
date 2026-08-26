export const useGameStore = defineStore('game', () => {
  const score = ref(0)
  const api = useRuntimeConfig().public.apiBase
  const auth = useAuthStore()

  async function load() {
    const data: any = await auth.apiFetch('/game/state')
    score.value = data.score
  }

  async function sync({ keepalive = false } = {}) {
    if (!keepalive) {
      await auth.apiFetch('/game/sync', { method: 'POST', body: { score: score.value } })
      return
    }

    // Durante pagehide no hay tiempo fiable para renovar un token; se intenta
    // guardar con el access token vigente.
    const response = await fetch(`${api}/game/sync`, {
      method: 'POST',
      keepalive,
      headers: {
        Authorization: `Bearer ${auth.access}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ score: score.value }),
    })

    if (!response.ok) {
      throw new Error(`Unable to sync game progress: ${response.status}`)
    }
  }

  function click() {
    score.value++
  }

  return { score, load, sync, click }
})
