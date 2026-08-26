<script setup lang="ts">
import type { GameUpgrade } from '~/stores/game'

const game = useGameStore()

const upgradeIcons: Record<GameUpgrade['key'], string> = {
  clicker: 'i-lucide-mouse-pointer-click',
  static: 'i-lucide-zap',
  spammer: 'i-lucide-gauge',
}

const cpsLabel = computed(() => {
  const cps = game.totalClicksPerSecond
  return Number.isInteger(cps) ? cps.toFixed(0) : cps.toFixed(1)
})

function rateLabel(upgrade: GameUpgrade) {
  if (upgrade.key === 'clicker') return '+1 cada 10 s'
  return `+${upgrade.clicks_per_second} por segundo`
}
</script>

<template>
  <aside
    class="upgrades-panel mx-auto max-h-[calc(100vh-9rem)] w-full max-w-sm overflow-y-auto overscroll-contain rounded-3xl border border-cyan-400/30 bg-blue-950/60 p-5 shadow-2xl backdrop-blur lg:mx-0"
  >
    <div class="mb-5 flex items-start justify-between gap-3">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.2em] text-cyan-300">Taller</p>
        <h2 class="mt-1 text-2xl font-black text-white">Upgrades</h2>
      </div>
      <UBadge
        color="info"
        variant="subtle"
        icon="i-lucide-timer"
        :label="`${cpsLabel} C/S`"
      />
    </div>

    <p class="mb-4 rounded-xl bg-cyan-950/65 px-3 py-2 text-sm text-cyan-100">
      Producción actual: <strong class="text-cyan-300">{{ cpsLabel }} clicks/s</strong>
    </p>

    <div v-if="game.upgradesLoading" class="space-y-3" aria-label="Cargando upgrades">
      <div v-for="index in 3" :key="index" class="h-28 animate-pulse rounded-2xl bg-cyan-950" />
    </div>

    <div v-else class="space-y-3">
      <UCard
        v-for="upgrade in game.upgrades"
        :key="upgrade.key"
        class="border border-cyan-400/15 bg-cyan-950/55"
      >
        <div class="flex items-start gap-3">
          <div class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[#023e8a] text-cyan-200">
            <UIcon :name="upgradeIcons[upgrade.key]" class="h-5 w-5" />
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-2">
              <h3 class="font-black text-cyan-50">{{ upgrade.name }}</h3>
              <span class="rounded-full bg-cyan-400/15 px-2 py-0.5 text-xs font-bold text-cyan-300">
                x{{ upgrade.quantity }}
              </span>
            </div>
            <p class="mt-1 text-xs text-cyan-100/70">{{ upgrade.description }}</p>
            <p class="mt-1 text-xs font-bold text-cyan-300">{{ rateLabel(upgrade) }}</p>
          </div>
        </div>

        <UButton
          class="mt-3"
          block
          color="info"
          variant="soft"
          size="sm"
          icon="i-lucide-shopping-cart"
          :label="`Comprar · ${upgrade.cost} puntos`"
          :loading="game.purchasingUpgrade === upgrade.key"
          :disabled="game.score < upgrade.cost || Boolean(game.purchasingUpgrade)"
          @click="game.buyUpgrade(upgrade.key)"
        />
      </UCard>
    </div>

    <p
      v-if="game.upgradeError"
      class="mt-4 rounded-xl bg-red-950/45 px-3 py-2 text-sm text-red-200"
      role="alert"
    >
      {{ game.upgradeError }}
    </p>
  </aside>
</template>

<style scoped>
.upgrades-panel {
  scrollbar-color: rgba(0, 180, 216, 0.65) rgba(3, 4, 94, 0.35);
  scrollbar-width: thin;
}

.upgrades-panel::-webkit-scrollbar {
  width: 7px;
}

.upgrades-panel::-webkit-scrollbar-track {
  background: rgba(3, 4, 94, 0.35);
  border-radius: 999px;
}

.upgrades-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 180, 216, 0.65);
  border-radius: 999px;
}
</style>
