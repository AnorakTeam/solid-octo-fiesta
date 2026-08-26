<script setup lang="ts">
import confetti from 'canvas-confetti'
import type { ConfettiOptions } from 'canvas-confetti'
import { bubbleColors } from '~/utils/sitePalette'

function burstFrom(element: HTMLElement) {
  const rect = element.getBoundingClientRect()
  const origin = {
    x: (rect.left + rect.width / 2) / window.innerWidth,
    y: (rect.top + rect.height / 2) / window.innerHeight,
  }
  const sharedOptions: ConfettiOptions = {
    angle: 90,
    spread: 68,
    decay: 0.92,
    gravity: 0.9,
    origin,
    colors: [...bubbleColors],
    shapes: ['square', 'circle'],
    zIndex: 35,
    disableForReducedMotion: true,
  }

  void confetti({
    ...sharedOptions,
    particleCount: 18,
    startVelocity: 32,
    ticks: 125,
    scalar: 0.72,
  })

  void confetti({
    ...sharedOptions,
    particleCount: 8,
    spread: 82,
    startVelocity: 25,
    ticks: 110,
    scalar: 1.05,
  })
}

defineExpose({ burstFrom })
</script>

<template>
  <span class="hidden" aria-hidden="true" />
</template>
