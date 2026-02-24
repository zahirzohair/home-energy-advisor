<script setup lang="ts">
import { cn } from "@/lib/utils";

interface Props {
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  variant?: "default" | "outline" | "secondary";
  customClass?: string;
}

withDefaults(defineProps<Props>(), {
  type: "button",
  disabled: false,
  variant: "default",
  customClass: "",
});

const variantClasses: Record<string, string> = {
  default:
    "bg-primary text-primary-foreground hover:bg-primary/90 active:bg-primary/95 shadow-soft transition-colors duration-200",
  outline:
    "border border-[hsl(var(--border))] bg-white hover:bg-[hsl(var(--muted))] text-[hsl(var(--foreground))] transition-colors duration-200",
  secondary:
    "bg-[hsl(var(--secondary))] text-[hsl(var(--secondary-foreground))] hover:opacity-90 transition-opacity duration-200",
};
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="
      cn(
        'inline-flex items-center justify-center rounded-xl text-sm font-semibold min-h-[44px] sm:min-h-[44px] px-6 py-2.5 disabled:opacity-50 disabled:pointer-events-none',
        variantClasses[variant] ?? variantClasses.default,
        customClass
      )
    "
  >
    <slot />
  </button>
</template>
