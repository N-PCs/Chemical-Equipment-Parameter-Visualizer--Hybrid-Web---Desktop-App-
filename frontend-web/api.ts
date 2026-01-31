
/**
 * ARCHITECTURE: /shared/
 * Purpose: This file has been superseded by /frontend-web/services/equipment-service.ts.
 * Removed legacy mock data to comply with 'Zero-Dummy Data' production policy.
 */

// Import the production service and legacy types to create a bridge
import { equipmentService as modernService } from './services/equipment-service';
import { DatasetHistory } from './types';

// Bridge to modern service while maintaining legacy interface for root App.tsx
export const equipmentService = {
  /**
   * Delegates file upload (CSV/Excel) to the modern service.
   */
  async uploadFile(file: File): Promise<DatasetHistory> {
    return await modernService.uploadFile(file);
  },

  /**
   * Delegates history fetching.
   */
  async getHistory(): Promise<DatasetHistory[]> {
    return await modernService.getHistory();
  },

  /**
   * Delegates PDF generation to the modern service.
   */
  async generatePdf(dataset: DatasetHistory): Promise<void> {
    return modernService.generatePdf(dataset);
  }
};

export const LEGACY_API_NOTICE = "Redirecting to specialized service layers.";
