<script setup lang="ts">
import { reactive, watch } from "vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Label from "@/components/ui/Label.vue";
import Card from "@/components/ui/Card.vue";
import { HEATING_TYPES, INSULATION_LEVELS } from "@/types/home";
import type { HeatingType, InsulationLevel } from "@/types/home";

export interface HomeFormValues {
  size_sqm: number;
  year_built?: number;
  heating_type: HeatingType;
  insulation?: InsulationLevel | "";
  notes?: string;
}

withDefaults(
  defineProps<{
    isSubmitting?: boolean;
    error?: string | null;
  }>(),
  { isSubmitting: false, error: null }
);

const emit = defineEmits<{
  submit: [values: HomeFormValues];
}>();

const form = reactive<{
  size_sqm: number;
  year_built: string;
  heating_type: HeatingType;
  insulation: InsulationLevel | "";
  notes: string;
}>({
  size_sqm: 0,
  year_built: "",
  heating_type: "GAS",
  insulation: "",
  notes: "",
});

const errors = reactive<Record<string, string>>({});

function validateField(
  field: "size_sqm" | "year_built" | "notes",
  value: unknown
): string | null {
  if (field === "size_sqm") {
    const n = Number(value);
    if (Number.isNaN(n) || n < 1 || n > 10000)
      return "Enter living area between 1 and 10000 m²";
  }
  if (field === "year_built" && value !== "" && value !== undefined) {
    const y = Number(value);
    if (Number.isNaN(y) || y < 1800 || y > 2026)
      return "Year must be between 1800 and 2026";
  }
  if (field === "notes" && typeof value === "string" && value.length > 2000)
    return "Notes must be at most 2000 characters";
  return null;
}

function validate(): boolean {
  const e: Record<string, string> = {};
  const sqmErr = validateField("size_sqm", form.size_sqm);
  if (sqmErr) e.size_sqm = sqmErr;
  const yearErr = validateField("year_built", form.year_built);
  if (yearErr) e.year_built = yearErr;
  const notesErr = validateField("notes", form.notes);
  if (notesErr) e.notes = notesErr;
  Object.assign(errors, e);
  return Object.keys(e).length === 0;
}

watch(
  () => form.size_sqm,
  () => {
    if (errors.size_sqm) errors.size_sqm = validateField("size_sqm", form.size_sqm) ?? "";
  }
);
watch(
  () => form.year_built,
  () => {
    if (errors.year_built) errors.year_built = validateField("year_built", form.year_built) ?? "";
  }
);
watch(
  () => form.notes,
  () => {
    if (errors.notes) errors.notes = validateField("notes", form.notes) ?? "";
  }
);

function onBlurSizeSqm() {
  const msg = validateField("size_sqm", form.size_sqm);
  errors.size_sqm = msg ?? "";
}
function onBlurYearBuilt() {
  const msg = validateField("year_built", form.year_built);
  errors.year_built = msg ?? "";
}
function onBlurNotes() {
  const msg = validateField("notes", form.notes);
  errors.notes = msg ?? "";
}

function onSubmit() {
  if (!validate()) return;
  const year_built = form.year_built ? Number(form.year_built) : undefined;
  if (year_built !== undefined && (Number.isNaN(year_built) || year_built < 1800 || year_built > 2026)) {
    return;
  }
  emit("submit", {
    size_sqm: form.size_sqm,
    year_built,
    heating_type: form.heating_type,
    insulation: form.insulation || undefined,
    notes: form.notes || undefined,
  });
}

const inputClass =
  "flex w-full rounded-xl border bg-white px-4 py-2.5 text-sm text-[hsl(var(--foreground))] min-h-[44px] transition-colors duration-200 border-[hsl(var(--input))] hover:border-[hsl(var(--border))]";
</script>

<template>
  <Card custom-class="w-full max-w-xl overflow-hidden">
    <div class="px-6 pt-6 pb-1">
      <h2 class="text-lg font-semibold tracking-tight text-[hsl(var(--foreground))]">
        Your home details
      </h2>
      <p class="mt-1 text-sm text-[hsl(var(--muted-foreground))]">
        We'll use this to suggest the best energy-saving steps for your home.
      </p>
    </div>
    <div class="p-6 pt-5">
      <form @submit.prevent="onSubmit" class="space-y-5">
        <div class="grid gap-5 sm:grid-cols-2">
          <div class="space-y-2">
            <Label for-id="size_sqm">Living area (m²) *</Label>
            <Input
              id="size_sqm"
              type="number"
              v-model.number="form.size_sqm"
              placeholder="e.g. 120"
              :error="!!errors.size_sqm"
              @blur="onBlurSizeSqm"
            />
            <p v-if="errors.size_sqm" class="text-sm text-red-600">
              {{ errors.size_sqm }}
            </p>
          </div>
          <div class="space-y-2">
            <Label for-id="year_built">Year built</Label>
            <Input
              id="year_built"
              type="number"
              v-model="form.year_built"
              placeholder="e.g. 1995"
              :error="!!errors.year_built"
              @blur="onBlurYearBuilt"
            />
            <p v-if="errors.year_built" class="text-sm text-red-600">
              {{ errors.year_built }}
            </p>
          </div>
        </div>

        <div class="grid gap-5 sm:grid-cols-2">
          <div class="space-y-2">
            <Label for-id="heating_type">Heating type *</Label>
            <select
              id="heating_type"
              v-model="form.heating_type"
              :class="inputClass"
            >
              <option v-for="t in HEATING_TYPES" :key="t" :value="t">
                {{ t.replace("_", " ") }}
              </option>
            </select>
          </div>
          <div class="space-y-2">
            <Label for-id="insulation">Insulation level</Label>
            <select
              id="insulation"
              v-model="form.insulation"
              :class="inputClass"
            >
              <option value="">Not specified</option>
              <option v-for="l in INSULATION_LEVELS" :key="l" :value="l">
                {{ l }}
              </option>
            </select>
          </div>
        </div>

        <div class="space-y-2">
          <Label for-id="notes">Additional notes</Label>
          <textarea
            id="notes"
            v-model="form.notes"
            rows="3"
            placeholder="e.g. Single family home, drafty windows"
            :class="[inputClass, 'min-h-[88px] resize-y placeholder:text-[hsl(var(--muted-foreground))]']"
            @blur="onBlurNotes"
          />
          <p v-if="errors.notes" class="text-sm text-red-600">
            {{ errors.notes }}
          </p>
        </div>

        <p
          v-if="error"
          role="alert"
          class="text-sm text-red-600"
        >
          {{ error }}
        </p>

        <div class="pt-2">
          <Button
            type="submit"
            :disabled="isSubmitting"
            :aria-busy="isSubmitting"
            class="w-full sm:w-auto min-w-[200px]"
          >
            {{ isSubmitting ? "Getting recommendations…" : "Get recommendations" }}
          </Button>
        </div>
      </form>
    </div>
  </Card>
</template>
