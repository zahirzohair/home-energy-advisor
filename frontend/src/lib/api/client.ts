import axios from "axios";

const baseURL =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined" ? "http://localhost:8000" : "http://localhost:8000");

export const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});
