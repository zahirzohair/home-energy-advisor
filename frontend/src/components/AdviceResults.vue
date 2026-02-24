<script setup lang="ts">
defineProps<{
  recommendations: string[];
}>();

function priorityLabel(index: number): string {
  if (index === 0) return "Top priority";
  if (index <= 2) return "High priority";
  return "";
}
</script>

<template>
  <div
    class="w-full max-w-xl rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] text-[hsl(var(--card-foreground))] shadow-card"
    aria-live="polite"
    aria-atomic="true"
    role="region"
    aria-label="Energy-saving recommendations"
  >
    <div class="px-6 pt-6 pb-1">
      <div class="flex items-center gap-3">
        <span
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary"
          aria-hidden="true"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5">
            <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
          </svg>
        </span>
        <div>
          <h3 class="text-lg font-semibold tracking-tight">
            Your energy-saving recommendations
          </h3>
          <p v-if="recommendations.length" class="text-sm text-[hsl(var(--muted-foreground))] mt-0.5">
            Ordered by priority — start from the top for the biggest impact.
          </p>
        </div>
      </div>
    </div>
    <div v-if="recommendations.length" class="p-6 pt-4">
      <ol class="space-y-3" role="list">
        <li
          v-for="(rec, i) in recommendations"
          :key="i"
          class="rounded-xl border transition-colors duration-200"
          :class="
            i < 3
              ? 'border-primary/30 bg-primary/[0.04]'
              : 'border-[hsl(var(--border))] bg-[hsl(var(--muted))]/30'
          "
        >
          <div class="flex gap-3 p-4">
            <span
              class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-semibold"
              :class="
                i === 0
                  ? 'bg-primary text-primary-foreground'
                  : i <= 2
                    ? 'bg-primary/20 text-primary'
                    : 'bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]'
              "
              aria-hidden="true"
            >
              {{ i + 1 }}
            </span>
            <div class="min-w-0 flex-1">
              <div
                v-if="priorityLabel(i)"
                class="mb-1.5 text-xs font-medium uppercase tracking-wide text-primary"
              >
                {{ priorityLabel(i) }}
              </div>
              <p class="text-sm leading-relaxed text-[hsl(var(--card-foreground))]">
                {{ rec }}
              </p>
            </div>
          </div>
        </li>
      </ol>
    </div>
  </div>
</template>
