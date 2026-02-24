import { ref } from "vue";

export type ToastType = "success" | "error" | "warning" | "info";

export interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

const toasts = ref<Toast[]>([]);
let nextId = 0;
const DEFAULT_DURATION = 4000;

function addToast(type: ToastType, message: string, duration = DEFAULT_DURATION): void {
  const id = nextId++;
  toasts.value = [...toasts.value, { id, type, message }];
  if (duration > 0) {
    setTimeout(() => {
      toasts.value = toasts.value.filter((t) => t.id !== id);
    }, duration);
  }
}

function removeToast(id: number): void {
  toasts.value = toasts.value.filter((t) => t.id !== id);
}

export function useToast() {
  return {
    toasts,
    showSuccess: (message: string, duration?: number) =>
      addToast("success", message, duration),
    showError: (message: string, duration?: number) =>
      addToast("error", message, duration),
    showWarning: (message: string, duration?: number) =>
      addToast("warning", message, duration),
    showInfo: (message: string, duration?: number) =>
      addToast("info", message, duration),
    remove: removeToast,
  };
}
