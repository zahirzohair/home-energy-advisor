<script setup lang="ts">
import { useToast } from "@/composables/useToast";
import { cn } from "@/lib/utils";

const { toasts, remove } = useToast();

const typeStyles: Record<string, string> = {
  success: "bg-emerald-50 border-emerald-200 text-emerald-800",
  error: "bg-red-50 border-red-200 text-red-800",
  warning: "bg-amber-50 border-amber-200 text-amber-800",
  info: "bg-sky-50 border-sky-200 text-sky-800",
};
</script>

<template>
  <div
    aria-live="polite"
    aria-atomic="true"
    class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none"
  >
    <div
      v-for="t in toasts"
      :key="t.id"
      role="status"
        :class="
        cn(
          'pointer-events-auto rounded-xl border px-4 py-3 shadow-card transition-shadow duration-200',
          typeStyles[t.type] ?? typeStyles.info
        )
      "
    >
      <div class="flex items-start justify-between gap-3">
        <p class="text-sm font-medium">{{ t.message }}</p>
        <button
          type="button"
          aria-label="Dismiss"
          class="shrink-0 rounded p-1 hover:opacity-70"
          @click="remove(t.id)"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>
