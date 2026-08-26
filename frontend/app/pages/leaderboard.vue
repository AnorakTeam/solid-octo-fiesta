<script setup lang="ts">
interface RankingEntry {
  position: number
  nickname: string
  score: number
  profile_icon: string | null
}

const api = useRuntimeConfig().public.apiBase
const { data: rows, status, error, refresh } = await useFetch<RankingEntry[]>(
  `${api}/game/leaderboard`,
  { default: () => [] },
)

function positionClasses(position: number) {
  if (position === 1) return 'bg-cyan-300 text-blue-950 shadow-[0_0_18px_rgba(103,232,249,0.45)]'
  if (position === 2) return 'bg-cyan-100 text-blue-950'
  if (position === 3) return 'bg-[#00b4d8] text-blue-950'
  return 'bg-[#023e8a] text-cyan-50'
}
</script>

<template>
  <main class="mx-auto min-h-screen w-full max-w-3xl px-5 pb-16 pt-14 sm:px-8 sm:pt-40">
    <header class="mb-8 text-center">
      <UBadge
        color="info"
        variant="subtle"
        icon="i-lucide-trophy"
        label="Salón de fama"
        class="mb-3"
      />
      <h1 class="text-4xl font-black text-white sm:text-5xl">Leaderboard</h1>
      <p class="mx-auto mt-3 max-w-lg text-cyan-100/80">
        Los jugadores que han llevado su puntuación más lejos.
      </p>
    </header>

    <div v-if="status === 'pending'" class="space-y-4" aria-label="Cargando leaderboard">
      <UCard
        v-for="index in 5"
        :key="index"
        class="border border-cyan-400/15 bg-blue-950/55"
      >
        <div class="flex items-center gap-4">
          <USkeleton class="h-11 w-11 rounded-full bg-cyan-900" />
          <USkeleton class="h-14 w-14 rounded-full bg-cyan-900" />
          <USkeleton class="h-5 flex-1 bg-cyan-900" />
          <USkeleton class="h-8 w-20 bg-cyan-900" />
        </div>
      </UCard>
    </div>

    <UAlert
      v-else-if="error"
      color="error"
      variant="subtle"
      icon="i-lucide-circle-alert"
      title="No pudimos cargar el leaderboard"
      description="Inténtalo nuevamente en unos segundos."
      :actions="[{ label: 'Reintentar', onClick: () => refresh() }]"
    />

    <ol v-else-if="rows.length" class="space-y-4">
      <li v-for="row in rows" :key="row.position">
        <UCard
          class="border border-cyan-400/20 bg-blue-950/65 shadow-[0_14px_35px_rgba(0,0,0,0.18)] backdrop-blur"
        >
          <div class="flex items-center gap-3 sm:gap-5">
            <span
              class="grid h-11 w-11 shrink-0 place-items-center rounded-full text-lg font-black sm:h-12 sm:w-12"
              :class="positionClasses(row.position)"
              :aria-label="`Posición ${row.position}`"
            >
              {{ row.position }}
            </span>

            <UAvatar
              :src="row.profile_icon || undefined"
              :alt="`Avatar de ${row.nickname}`"
              icon="i-lucide-user-round"
              size="xl"
              class="shrink-0 bg-[#023e8a] text-cyan-100 ring-2 ring-cyan-400/30"
            />

            <div class="min-w-0 flex-1 text-left">
              <p class="truncate text-lg font-black text-cyan-50 sm:text-xl">
                {{ row.nickname }}
              </p>
              <p class="text-xs uppercase tracking-[0.16em] text-cyan-300/75">
                Puesto #{{ row.position }}
              </p>
            </div>

            <div class="shrink-0 rounded-2xl bg-cyan-950/75 px-3 py-2 text-right sm:px-5">
              <strong class="block text-xl text-cyan-300 sm:text-2xl">{{ row.score }}</strong>
              <span class="text-xs uppercase tracking-wider text-cyan-100/65">puntos</span>
            </div>
          </div>
        </UCard>
      </li>
    </ol>

    <UCard v-else class="border border-cyan-400/20 bg-blue-950/65 text-center">
      <UIcon name="i-lucide-users-round" class="mx-auto mb-3 h-8 w-8 text-cyan-300" />
      <p class="text-cyan-100">Aún no hay jugadores en el leaderboard.</p>
    </UCard>

    <div class="mt-8 flex justify-center">
      <UButton
        to="/game"
        color="info"
        variant="soft"
        size="lg"
        icon="i-lucide-gamepad-2"
        label="Volver al juego"
      />
    </div>
  </main>
</template>
