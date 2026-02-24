<script setup lang="ts">
import { ref } from "vue";
import HomeForm from "@/components/HomeForm.vue";
import AdviceResults from "@/components/AdviceResults.vue";
import ToastContainer from "@/components/ToastContainer.vue";
import { createHome, getAdvice } from "@/lib/api/homes";
import type { HomeFormValues } from "@/components/HomeForm.vue";
import type { AxiosError } from "axios";
import { useToast } from "@/composables/useToast";

const { showSuccess, showError } = useToast();
const recommendations = ref<string[]>([]);
const isSubmitting = ref(false);
const error = ref<string | null>(null);

function getErrorMessage(err: unknown): string {
  const axiosErr = err as AxiosError<{ detail?: string }>;
  const detail = axiosErr.response?.data?.detail;
  if (typeof detail === "string") return detail;
  return "Something went wrong. Please try again.";
}

async function handleSubmit(values: HomeFormValues) {
  isSubmitting.value = true;
  error.value = null;
  try {
    const home = await createHome({
      size_sqm: values.size_sqm,
      year_built: values.year_built ?? undefined,
      heating_type: values.heating_type,
      insulation: values.insulation ?? undefined,
      notes: values.notes ?? undefined,
    });
    const { recommendations: recs } = await getAdvice(home.id);
    recommendations.value = recs;
    showSuccess("Recommendations ready.");
  } catch (err) {
    const message = getErrorMessage(err);
    error.value = message;
    showError(message);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <ToastContainer />
  <main class="min-h-screen bg-[hsl(var(--background))]">
    <div class="container mx-auto px-4 py-8 sm:py-14 md:py-16">
      <header class="mb-10 sm:mb-14 text-center max-w-xl mx-auto">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary/10 text-primary mb-6" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="w-7 h-7">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
            <path d="M9 22V12h6v10" />
          </svg>
        </div>
        <h1 class="text-3xl font-semibold tracking-tight text-[hsl(var(--foreground))] sm:text-4xl">
          Home Energy Advisor
        </h1>
        <p class="mt-3 text-base text-[hsl(var(--muted-foreground))] leading-relaxed">
          Enter your home details to get personalized, AI-generated energy efficiency tips.
        </p>
      </header>

      <div class="mx-auto flex max-w-2xl flex-col items-center gap-10 sm:gap-12">
        <HomeForm
          :is-submitting="isSubmitting"
          :error="error"
          @submit="handleSubmit"
        />

        <div v-if="recommendations.length > 0" class="w-full max-w-xl recommendations-enter">
          <AdviceResults :recommendations="recommendations" />
        </div>
      </div>
    </div>
  </main>
</template>
