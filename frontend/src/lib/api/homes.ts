import { apiClient } from "@/lib/api/client";
import type { Home, HomeCreate, AdviceResponse } from "@/types/home";

export async function createHome(data: HomeCreate): Promise<Home> {
  const { data: home } = await apiClient.post<Home>("/api/homes", data);
  return home;
}

export async function getHome(id: number): Promise<Home> {
  const { data } = await apiClient.get<Home>(`/api/homes/${id}`);
  return data;
}

export async function getAdvice(homeId: number): Promise<AdviceResponse> {
  const { data } = await apiClient.post<AdviceResponse>(
    `/api/homes/${homeId}/advice`
  );
  return data;
}
