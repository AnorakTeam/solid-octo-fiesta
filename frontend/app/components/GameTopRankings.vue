<script setup lang="ts">
import { motion } from 'motion-v'

interface RankingEntry {
  position: number
  nickname: string
  score: number
}

const api = useRuntimeConfig().public.apiBase
const rankings = ref<RankingEntry[]>([])
const rankingsLoading = ref(true)
const loadedAt = ref<Date | null>(null)

const loadedAtLabel = computed(() => {
  if (!loadedAt.value) return ''

  const date = new Intl.DateTimeFormat('es-CO', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(loadedAt.value)
  const time = new Intl.DateTimeFormat('es-CO', {
    hour: 'numeric',
    minute: '2-digit',
  }).format(loadedAt.value)

  return `${date} · ${time}`
})

async function loadRankings() {
  rankingsLoading.value = true

  try {
    const rows = await $fetch<RankingEntry[]>(`${api}/game/leaderboard`)
    rankings.value = rows.slice(0, 5)
    loadedAt.value = new Date()
  } catch {
    rankings.value = []
  } finally {
    rankingsLoading.value = false
  }
}

onMounted(loadRankings)
</script>

<template>
  <motion.aside
    layout
    :transition="{ layout: { duration: 0.35, ease: 'easeOut' } }"
    class="mx-auto w-full max-w-sm rounded-3xl border border-cyan-400/30 bg-blue-950/60 p-6 shadow-2xl backdrop-blur lg:mx-0"
  >
    <div class="mb-5 flex items-center justify-between">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.2em] text-cyan-300">Salón de fama</p>
        <h2 class="mt-1 text-2xl font-black text-white">Top 5</h2>
      </div>
      <div class="flex items-center gap-2">
        <button
          class="grid h-9 w-9 place-items-center rounded-full text-cyan-300 transition hover:bg-cyan-400/15 hover:text-white disabled:cursor-wait disabled:opacity-60"
          type="button"
          aria-label="Actualizar leaderboard"
          title="Actualizar leaderboard"
          :disabled="rankingsLoading"
          @click="loadRankings"
        >
          <svg class="h-5 w-5" :class="{ 'animate-spin': rankingsLoading }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m14.836 2A7.5 7.5 0 0 0 5.582 9M4.582 9H9m11 11v-5h-.581m0 0A7.5 7.5 0 0 1 5.582 15M15 15h4.418" />
          </svg>
        </button>
        <span class="text-2xl" aria-hidden="true">🏆</span>
      </div>
    </div>

    <div v-if="rankingsLoading" class="space-y-3" aria-label="Cargando ranking">
      <div v-for="index in 5" :key="index" class="h-12 animate-pulse rounded-xl bg-cyan-950" />
    </div>
    <ol v-else-if="rankings.length" class="space-y-2">
      <li v-for="row in rankings" :key="row.position" class="flex items-center gap-3 rounded-xl bg-cyan-950/60 px-3 py-3">
        <span class="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-cyan-400 font-black text-slate-950">{{ row.position }}</span>
        <span class="min-w-0 flex-1 truncate font-semibold text-cyan-50">{{ row.nickname }}</span>
        <strong class="text-cyan-300">{{ row.score }}</strong>
      </li>
    </ol>
    <p v-else class="rounded-xl bg-cyan-950/60 px-4 py-5 text-center text-sm text-cyan-100">Aún no hay puntajes para mostrar.</p>
    <p v-if="loadedAtLabel" class="mt-5 text-center text-xs text-cyan-300/80">Actualizado: {{ loadedAtLabel }}</p>
  </motion.aside>
</template>
