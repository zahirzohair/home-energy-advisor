<script setup lang="ts">
import { cn } from "@/lib/utils";

interface Props {
  customClass?: string;
}
defineProps<Props>();
</script>

<template>
  <div
    :class="
      cn(
        'rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] text-[hsl(var(--card-foreground))] shadow-card transition-shadow duration-200',
        customClass ?? ''
      )
    "
  >
    <slot />
  </div>
</template>
