
/**
 * ARCHITECTURE: /frontend-web/services/
 * Purpose: Framework for live SCADA data synchronization.
 * Modified: Removed dummy jitter; in production, this connects to a real WebSocket stream.
 */

import { EquipmentData } from '../../shared/types';

export class LiveSyncService {
  private intervalId: number | null = null;

  /**
   * For production, this function should establish a WebSocket connection.
   * Currently updated to simulate state synchronization without fake random jitter.
   */
  startSimulatedStream(initialData: EquipmentData[], onUpdate: (data: EquipmentData[]) => void) {
    if (this.intervalId) return;

    // Simulation of periodic SCADA polling without random dummy jitter
    // It maintains the current values to demonstrate the auto-update UI reactivity
    this.intervalId = window.setInterval(() => {
      onUpdate([...initialData]);
    }, 5000); 
  }

  stopStream() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  isActive() {
    return this.intervalId !== null;
  }
}

export const liveSyncService = new LiveSyncService();
