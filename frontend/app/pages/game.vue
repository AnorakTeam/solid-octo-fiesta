<script setup lang="ts">
import { motion } from 'motion-v'

definePageMeta({ middleware: 'auth' })

const game = useGameStore()
const auth = useAuthStore()
const syncIntervalSeconds = 30
const secondsUntilSync = ref(syncIntervalSeconds)
const scoreShakeTick = ref(0)
const hasIncrementedScore = ref(false)
const syncProgress = computed(() => (secondsUntilSync.value / syncIntervalSeconds) * 100)
const scoreShakeAnimation = computed(() => {
  if (!hasIncrementedScore.value) {
    return { x: 0, y: 0, rotate: 0, scale: 1 }
  }

  const direction = scoreShakeTick.value % 2 === 0 ? 1 : -1

  return {
    x: [0, -7 * direction, 6 * direction, -4 * direction, 3 * direction, 0],
    y: [0, 2, -2, 1, -1, 0],
    rotate: [0, -2 * direction, 2 * direction, -1 * direction, direction, 0],
    scale: [1, 1.12, 0.98, 1.06, 1.01, 1],
  }
})
const numberSpawner = ref<{
  spawn: (options?: {
    x?: number
    y?: number
    text?: string
    duration?: number
    rise?: number
    fontSize?: number
    color?: string
    opacity?: number
  }) => void
} | null>(null)
const milestoneConfetti = ref<{
  burstFrom: (element: HTMLElement) => void
} | null>(null)
const scoreButton = ref<HTMLButtonElement | null>(null)
const scoreEffectsReady = ref(false)
let syncTimer: ReturnType<typeof window.setInterval> | undefined

watch(() => game.score, (newScore, previousScore) => {
  if (!scoreEffectsReady.value || newScore <= previousScore) return

  hasIncrementedScore.value = true
  scoreShakeTick.value++

  if (
    Math.floor(newScore / 100) > Math.floor(previousScore / 100)
    && scoreButton.value
  ) {
    milestoneConfetti.value?.burstFrom(scoreButton.value)
  }
})

function handleGameClick(event: MouseEvent) {
  game.click()
  numberSpawner.value?.spawn({
    x: event.clientX,
    y: event.clientY,
    text: '+1',
    duration: 1_800,
    rise: 130,
    fontSize: 34,
    color: '#00b4d8',
    opacity: 1,
  })
}

function syncOnPageExit() {
  // A keepalive request can continue after the document starts unloading.
  void game.sync({ keepalive: true }).catch(() => undefined)
}

async function logout() {
  game.stopPassiveIncome()
  await game.sync().catch(() => undefined)
  auth.logout()
}

onMounted(async () => {
  await Promise.all([auth.loadUser(), game.load()])
  scoreEffectsReady.value = true
  game.startPassiveIncome()
  syncTimer = window.setInterval(() => {
    if (secondsUntilSync.value <= 1) {
      secondsUntilSync.value = syncIntervalSeconds
      void game.sync().catch(() => undefined)
      return
    }

    secondsUntilSync.value--
  }, 1_000)
  window.addEventListener('pagehide', syncOnPageExit)
})

onBeforeRouteLeave(async () => {
  game.stopPassiveIncome()
  await game.sync().catch(() => undefined)
})

onUnmounted(() => {
  game.stopPassiveIncome()
  if (syncTimer) clearInterval(syncTimer)
  window.removeEventListener('pagehide', syncOnPageExit)
})
</script>
<template>
  <main class="min-h-screen px-6 py-10 lg:grid lg:grid-cols-[18rem_minmax(13rem,1fr)_20rem] lg:items-center lg:gap-6 lg:px-8 xl:grid-cols-[20rem_minmax(14rem,1fr)_22rem] xl:gap-10 xl:px-12">
    <section class="grid min-h-[60vh] place-items-center text-center lg:col-start-2 lg:row-start-1">
      <div>
        <div class="mb-4 flex items-center justify-center gap-3 text-cyan-100">
          <img v-if="auth.user?.profile_icon" :src="auth.user.profile_icon" alt="Ícono de perfil" class="h-9 w-9 rounded-full object-cover ring-2 ring-cyan-300" />
          <p>Hola, {{ auth.user?.nickname }}</p>
          <NuxtLink class="text-xs font-bold text-cyan-300 hover:text-white" to="/profile">Editar perfil</NuxtLink>
        </div>
        <p class="mb-2 text-sm font-semibold uppercase tracking-[0.24em] text-cyan-300">Puntos</p>
        <motion.p
          class="mb-8 text-7xl font-black tracking-tight text-white sm:text-8xl"
          :animate="scoreShakeAnimation"
          :transition="{
            duration: 0.3,
            ease: 'linear',
            times: [0, 0.16, 0.34, 0.52, 0.72, 1],
          }"
        >
          {{ game.score }}
        </motion.p>
        <ScoreMilestoneConfetti ref="milestoneConfetti" />
        <button
          ref="scoreButton"
          class="h-48 w-48 rounded-full bg-cyan-400 text-4xl font-black text-slate-950 shadow-[0_0_45px_rgba(34,211,238,0.45)] transition hover:scale-105 hover:bg-cyan-300 active:scale-95"
          @click.stop="handleGameClick">+1</button>
        <div class="mt-8 flex items-center justify-center gap-4 text-sm font-semibold">
          <NuxtLink class="text-cyan-300 transition hover:text-white" to="/leaderboard">Ver ranking completo</NuxtLink>
          <span class="text-cyan-700">·</span>
          <button class="text-cyan-300 transition hover:text-white" @click="logout">Salir</button>
        </div>
      </div>
    </section>

    <GameUpgradesPanel class="mt-8 lg:col-start-1 lg:row-start-1 lg:mt-0" />
    <GameTopRankings class="mt-8 lg:col-start-3 lg:row-start-1 lg:mt-0" />
    <FloatingNumberSpawner ref="numberSpawner" />

    <div class="fixed inset-x-0 bottom-0 z-10 border-t border-cyan-400/20 bg-[#03045e]/90 px-6 py-3 backdrop-blur">
      <div class="mx-auto flex w-full max-w-5xl items-center gap-4">
        <div class="shrink-0">
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-cyan-300">Sincronización</p>
          <p class="text-sm text-cyan-50">Próximo guardado en {{ secondsUntilSync }} s</p>
        </div>
        <div
          class="h-2 flex-1 overflow-hidden rounded-full bg-cyan-950 ring-1 ring-cyan-400/20"
          role="progressbar"
          aria-label="Tiempo restante para la siguiente sincronización"
          :aria-valuenow="secondsUntilSync"
          :aria-valuemin="0"
          :aria-valuemax="syncIntervalSeconds"
        >
          <div
            class="h-full rounded-full bg-cyan-400 shadow-[0_0_14px_rgba(34,211,238,0.95)] transition-[width] duration-1000 ease-linear"
            :style="{ width: `${syncProgress}%` }"
          />
        </div>
      </div>
    </div>
  </main>
</template>
