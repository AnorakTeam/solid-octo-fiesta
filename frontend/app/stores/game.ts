export interface GameUpgrade {
  key: 'clicker' | 'static' | 'spammer'
  name: string
  description: string
  cost: number
  clicks_per_second: number
  quantity: number
}

interface UpgradeState {
  upgrades: GameUpgrade[]
  total_clicks_per_second: number
}

interface UpgradePurchaseState extends UpgradeState {
  score: number
}

export const useGameStore = defineStore('game', () => {
  const score = ref(0)
  const upgrades = ref<GameUpgrade[]>([])
  const upgradesLoading = ref(false)
  const purchasingUpgrade = ref<string | null>(null)
  const upgradeError = ref('')
  const api = useRuntimeConfig().public.apiBase
  const auth = useAuthStore()
  const totalClicksPerSecond = computed(() => upgrades.value.reduce(
    (total, upgrade) => total + upgrade.clicks_per_second * upgrade.quantity,
    0,
  ))
  let passiveTimer: ReturnType<typeof window.setInterval> | undefined
  let passiveRemainder = 0
  let lastPassiveTick = 0

  async function load() {
    upgradesLoading.value = true

    try {
      const [state, upgradeState] = await Promise.all([
        auth.apiFetch<{ score: number }>('/game/state'),
        auth.apiFetch<UpgradeState>('/game/upgrades'),
      ])
      score.value = state.score
      upgrades.value = upgradeState.upgrades
    } finally {
      upgradesLoading.value = false
    }
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

  function applyPassiveIncome() {
    const now = performance.now()
    const elapsedSeconds = (now - lastPassiveTick) / 1_000
    lastPassiveTick = now
    passiveRemainder += elapsedSeconds * totalClicksPerSecond.value

    const wholeClicks = Math.floor(passiveRemainder + Number.EPSILON)
    if (wholeClicks < 1) return

    passiveRemainder -= wholeClicks
    score.value += wholeClicks
  }

  function startPassiveIncome() {
    stopPassiveIncome()
    lastPassiveTick = performance.now()
    passiveTimer = window.setInterval(applyPassiveIncome, 250)
  }

  function stopPassiveIncome() {
    if (passiveTimer) window.clearInterval(passiveTimer)
    passiveTimer = undefined
  }

  async function buyUpgrade(upgradeKey: GameUpgrade['key']) {
    if (purchasingUpgrade.value) return false

    purchasingUpgrade.value = upgradeKey
    upgradeError.value = ''
    const scoreBeforeRequest = score.value

    try {
      await sync()
      const data = await auth.apiFetch<UpgradePurchaseState>(
        `/game/upgrades/${upgradeKey}/purchase`,
        { method: 'POST' },
      )
      const pointsEarnedDuringRequest = Math.max(0, score.value - scoreBeforeRequest)
      score.value = data.score + pointsEarnedDuringRequest
      upgrades.value = data.upgrades
      return true
    } catch (error: any) {
      upgradeError.value = error?.data?.detail
        ?? error?.response?._data?.detail
        ?? 'No fue posible comprar el upgrade.'
      return false
    } finally {
      purchasingUpgrade.value = null
    }
  }

  return {
    score,
    upgrades,
    upgradesLoading,
    purchasingUpgrade,
    upgradeError,
    totalClicksPerSecond,
    load,
    sync,
    click,
    buyUpgrade,
    startPassiveIncome,
    stopPassiveIncome,
  }
})
