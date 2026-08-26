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
    decay: 0.91,
    gravity: 0.82,
    origin,
    colors: [...bubbleColors],
    shapes: ['square', 'circle', 'star'],
    zIndex: 45,
    disableForReducedMotion: true,
  }

  void confetti({
    ...sharedOptions,
    particleCount: 38,
    angle: 90,
    spread: 100,
    startVelocity: 42,
    ticks: 160,
    scalar: 0.88,
  })

  void confetti({
    ...sharedOptions,
    particleCount: 14,
    angle: 135,
    spread: 48,
    startVelocity: 34,
    drift: -0.25,
    ticks: 145,
    scalar: 0.7,
  })

  void confetti({
    ...sharedOptions,
    particleCount: 14,
    angle: 45,
    spread: 48,
    startVelocity: 34,
    drift: 0.25,
    ticks: 145,
    scalar: 1.05,
  })
}

defineExpose({ burstFrom })
</script>

<template>
  <span class="hidden" aria-hidden="true" />
</template>
