<script setup lang="ts">
import type { ISourceOptions } from '@tsparticles/engine'
import { bubbleColors } from '~/utils/sitePalette'

const options: ISourceOptions = {
  fullScreen: {
    enable: false,
  },
  fpsLimit: 60,
  detectRetina: true,
  particles: {
    number: {
      value: 28,
      density: {
        enable: true,
        width: 1200,
        height: 800,
      },
    },
    color: {
      value: [...bubbleColors],
    },
    shape: {
      type: 'circle',
    },
    opacity: {
      value: {
        min: 0.08,
        max: 0.28,
      },
      animation: {
        enable: true,
        speed: 0.18,
        sync: false,
      },
    },
    size: {
      value: {
        min: 8,
        max: 52,
      },
      animation: {
        enable: true,
        speed: 1.4,
        sync: false,
      },
    },
    move: {
      enable: true,
      direction: 'top',
      speed: {
        min: 0.25,
        max: 1.25,
      },
      random: true,
      straight: false,
      outModes: {
        default: 'out',
      },
    },
    links: {
      enable: false,
    },
  },
  interactivity: {
    events: {
      onClick: {
        enable: false,
      },
      onHover: {
        enable: false,
      },
    },
  },
}
</script>

<template>
  <div class="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden="true">
    <ClientOnly>
      <VueParticles
        id="global-floating-bubbles"
        class="h-full w-full"
        :options="options"
      />
    </ClientOnly>
  </div>
</template>

<style scoped>
:deep(#global-floating-bubbles),
:deep(#global-floating-bubbles canvas) {
  width: 100%;
  height: 100%;
}
</style>
