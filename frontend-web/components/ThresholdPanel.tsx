/**
 * ARCHITECTURE: /frontend-web/components/
 * Purpose: Configuration panel for safety thresholds (Red Zones).
 */

import React from 'react';
import { ThresholdSettings } from '../../shared/types';

interface ThresholdPanelProps {
  settings: ThresholdSettings;
  onChange: (settings: ThresholdSettings) => void;
}

const ThresholdPanel: React.FC<ThresholdPanelProps> = ({ settings, onChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    onChange({
      ...settings,
      [name]: parseFloat(value) || 0,
    });
  };

  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
        <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Safety Thresholds (Red Zones)</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Max Flowrate (m³/h)</label>
          <input 
            type="number" 
            name="maxFlowrate" 
            value={settings.maxFlowrate} 
            onChange={handleChange}
            className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-red-500 outline-none transition-all"
          />
        </div>
        <div>
          <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Max Pressure (bar)</label>
          <input 
            type="number" 
            name="maxPressure" 
            value={settings.maxPressure} 
            onChange={handleChange}
            className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-red-500 outline-none transition-all"
          />
        </div>
        <div>
          <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Max Temperature (°C)</label>
          <input 
            type="number" 
            name="maxTemperature" 
            value={settings.maxTemperature} 
            onChange={handleChange}
            className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-red-500 outline-none transition-all"
          />
        </div>
      </div>
      
      <p className="mt-4 text-[9px] text-slate-400 leading-tight italic">
        * Values exceeding these limits will trigger immediate visual alerts across the suite.
      </p>
    </div>
  );
};

export default ThresholdPanel;