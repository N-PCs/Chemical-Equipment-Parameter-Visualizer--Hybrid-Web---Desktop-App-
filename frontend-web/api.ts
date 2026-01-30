
/**
 * ARCHITECTURE: /shared/
 * Purpose: This file has been superseded by /frontend-web/services/equipment-service.ts.
 * Removed legacy mock data to comply with 'Zero-Dummy Data' production policy.
 */

// Import the production service and legacy types to create a bridge
import { equipmentService as modernService } from './frontend-web/services/equipment-service';
import { DatasetHistory } from './types';

// Bridge to modern service while maintaining legacy type compatibility for root App.tsx
export const equipmentService = {
  /**
   * Delegates CSV upload to the modern service and maps the result to the legacy summary structure.
   */
  async uploadCsv(file: File): Promise<DatasetHistory> {
    const ds = await modernService.uploadCsv(file);
    return {
      id: ds.id,
      filename: ds.filename,
      timestamp: ds.timestamp,
      data: ds.data,
      summary: {
        total_count: ds.summary.total_count,
        avg_flowrate: ds.summary.flowrate.avg,
        avg_pressure: ds.summary.pressure.avg,
        avg_temperature: ds.summary.temperature.avg,
        type_distribution: ds.summary.type_distribution
      }
    };
  },

  /**
   * Delegates history fetching and maps items to the legacy summary structure.
   */
  async getHistory(): Promise<DatasetHistory[]> {
    const history = await modernService.getHistory();
    return history.map(ds => ({
      id: ds.id,
      filename: ds.filename,
      timestamp: ds.timestamp,
      data: ds.data,
      summary: {
        total_count: ds.summary.total_count,
        avg_flowrate: ds.summary.flowrate.avg,
        avg_pressure: ds.summary.pressure.avg,
        avg_temperature: ds.summary.temperature.avg,
        type_distribution: ds.summary.type_distribution
      }
    }));
  },

  /**
   * Delegates PDF generation to the modern service.
   */
  async generatePdf(dataset: DatasetHistory): Promise<void> {
    // Cast to any to bypass summary field type incompatibility as the implementation only uses filename and data length
    return modernService.generatePdf(dataset as any);
  }
};

export const LEGACY_API_NOTICE = "Redirecting to specialized service layers.";
