export const HEATING_TYPES = [
  "GAS",
  "OIL",
  "ELECTRIC",
  "HEAT_PUMP",
  "DISTRICT",
] as const;

export const INSULATION_LEVELS = [
  "NONE",
  "PARTIAL",
  "GOOD",
  "EXCELLENT",
] as const;

export type HeatingType = (typeof HEATING_TYPES)[number];
export type InsulationLevel = (typeof INSULATION_LEVELS)[number];

export interface HomeCreate {
  size_sqm: number;
  year_built?: number | null;
  heating_type: HeatingType;
  insulation?: InsulationLevel | null;
  notes?: string | null;
}

export interface Home {
  id: number;
  size_sqm: number;
  year_built: number | null;
  heating_type: HeatingType;
  insulation: InsulationLevel | null;
  notes: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface AdviceResponse {
  recommendations: string[];
}
