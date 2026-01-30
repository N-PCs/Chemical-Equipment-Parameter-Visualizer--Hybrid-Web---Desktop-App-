
/**
 * ARCHITECTURE: /shared/types/
 * Purpose: Shared data models between frontend and backend.
 */

export interface EquipmentData {
  id?: number;
  equipment_name: string;
  type: string;
  flowrate: number;
  pressure: number;
  temperature: number;
}

export interface EquipmentSummary {
  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;
  type_distribution: Record<string, number>;
}

export interface DatasetHistory {
  id: string;
  filename: string;
  timestamp: string;
  summary: EquipmentSummary;
  data: EquipmentData[];
}

export enum ParameterType {
  FLOWRATE = 'flowrate',
  PRESSURE = 'pressure',
  TEMPERATURE = 'temperature'
}
