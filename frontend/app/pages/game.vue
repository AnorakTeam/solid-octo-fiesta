<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const game = useGameStore()
const auth = useAuthStore()
const syncIntervalSeconds = 30
const secondsUntilSync = ref(syncIntervalSeconds)
const syncProgress = computed(() => (secondsUntilSync.value / syncIntervalSeconds) * 100)
let syncTimer: ReturnType<typeof window.setInterval> | undefined

function syncOnPageExit() {
  // A keepalive request can continue after the document starts unloading.
  void game.sync({ keepalive: true }).catch(() => undefined)
}

async function logout() {
  await game.sync().catch(() => undefined)
  auth.logout()
}

onMounted(async () => {
  await Promise.all([auth.loadUser(), game.load()])
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
  await game.sync().catch(() => undefined)
})

onUnmounted(() => {
  if (syncTimer) clearInterval(syncTimer)
  window.removeEventListener('pagehide', syncOnPageExit)
})
</script>
<template>
  <main class="min-h-screen px-6 py-10 lg:grid lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-center lg:gap-12 lg:px-12">
    <section class="grid min-h-[60vh] place-items-center text-center">
      <div>
        <div class="mb-4 flex items-center justify-center gap-3 text-cyan-100">
          <img v-if="auth.user?.profile_icon" :src="auth.user.profile_icon" alt="Ícono de perfil" class="h-9 w-9 rounded-full object-cover ring-2 ring-cyan-300" />
          <p>Hola, {{ auth.user?.nickname }}</p>
          <NuxtLink class="text-xs font-bold text-cyan-300 hover:text-white" to="/profile">Editar perfil</NuxtLink>
        </div>
        <p class="mb-2 text-sm font-semibold uppercase tracking-[0.24em] text-cyan-300">Puntos</p>
        <p class="mb-8 text-7xl font-black tracking-tight text-white sm:text-8xl">{{ game.score }}</p>
        <button
          class="h-48 w-48 rounded-full bg-cyan-400 text-4xl font-black text-slate-950 shadow-[0_0_45px_rgba(34,211,238,0.45)] transition hover:scale-105 hover:bg-cyan-300 active:scale-95"
          @click="game.click">+1</button>
        <div class="mt-8 flex items-center justify-center gap-4 text-sm font-semibold">
          <NuxtLink class="text-cyan-300 transition hover:text-white" to="/leaderboard">Ver ranking completo</NuxtLink>
          <span class="text-cyan-700">·</span>
          <button class="text-cyan-300 transition hover:text-white" @click="logout">Salir</button>
        </div>
      </div>
    </section>

    <GameTopRankings />

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
