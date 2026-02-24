<script setup lang="ts">
import { cn } from "@/lib/utils";

interface Props {
  id?: string;
  type?: string;
  modelValue?: string | number;
  placeholder?: string;
  disabled?: boolean;
  customClass?: string;
  error?: boolean;
}

withDefaults(defineProps<Props>(), {
  type: "text",
  disabled: false,
  error: false,
});

defineEmits<{
  "update:modelValue": [value: string | number];
  blur: [];
}>();
</script>

<template>
  <input
    :id="id"
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="
      cn(
        'flex w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-[hsl(var(--foreground))] placeholder:text-[hsl(var(--muted-foreground))] min-h-[44px] transition-colors duration-200',
        error
          ? 'border-red-500 focus:border-red-500'
          : 'border-[hsl(var(--input))] hover:border-[hsl(var(--border))]',
        customClass
      )
    "
    @input="
      $emit(
        'update:modelValue',
        ($event.target as HTMLInputElement).value
      )
    "
    @blur="$emit('blur')"
  />
</template>
