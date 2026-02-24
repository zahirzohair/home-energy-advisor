<script setup lang="ts">
import { cn } from "@/lib/utils";

interface Props {
  forId?: string;
  customClass?: string;
}
defineProps<Props>();
</script>

<template>
  <label
    :for="forId"
    :class="cn('text-sm font-medium text-[hsl(var(--foreground))]', customClass)"
  >
    <slot />
  </label>
</template>
