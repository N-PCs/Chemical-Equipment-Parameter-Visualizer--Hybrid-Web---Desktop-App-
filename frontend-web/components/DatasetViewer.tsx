/**
 * ARCHITECTURE: /frontend-web/components/
 * Purpose: Responsive detailed viewer for chemical equipment datasets with Alert logic.
 */

import React from 'react';
import { DatasetHistory, CriticalAlert, ThresholdSettings } from '../../shared/types';
import SummaryStats from './SummaryStats';
import EquipmentCharts from './EquipmentCharts';
import EquipmentTable from './EquipmentTable';

interface DatasetViewerProps {
  dataset: DatasetHistory;
  activeAlerts: CriticalAlert[];
  thresholds: ThresholdSettings;
}

const DatasetViewer: React.FC<DatasetViewerProps> = ({ dataset, activeAlerts, thresholds }) => {
  return (
    <div className="space-y-6 sm:space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 fill-mode-forward">
      {/* Alert Banner Section */}
      {activeAlerts.length > 0 && (
        <div className="bg-red-600 text-white p-4 rounded-2xl shadow-xl flex items-center justify-between animate-pulse">
            <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center font-bold text-lg">!</div>
                <div>
                    <h3 className="font-bold text-sm uppercase tracking-widest">Critical Safety Alert</h3>
                    <p className="text-xs opacity-90">{activeAlerts.length} parameters have exceeded configured red zones.</p>
                </div>
            </div>
            <div className="hidden md:block text-right">
                <p className="text-[10px] font-bold uppercase">Immediate Action Required</p>
                <p className="text-[8px] opacity-70">Timestamp: {new Date().toISOString()}</p>
            </div>
        </div>
      )}

      {/* Header Info */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-800 tracking-tight">
            Asset Log: <span className="text-blue-600">{dataset.filename}</span>
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Comprehensive audit of stability metrics and safety correlations.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-white px-3 sm:px-4 py-2 rounded-xl border border-slate-200 shadow-sm self-start md:self-auto">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
          <span className="text-[9px] sm:text-[10px] font-bold text-slate-400 uppercase tracking-widest">
            Last Sync: {new Date(dataset.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <SummaryStats summary={dataset.summary} />

      {/* Visualizations */}
      <div className="w-full">
        <EquipmentCharts data={dataset.data} />
      </div>

      {/* Data Table */}
      <div className="glass-effect rounded-2xl sm:rounded-3xl shadow-lg border border-slate-200 overflow-hidden">
        <div className="px-4 sm:px-6 py-3 sm:py-4 bg-slate-50/50 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Asset Registry</h3>
          <span className={`text-[10px] font-bold px-2 py-1 rounded-md ${activeAlerts.length > 0 ? 'bg-red-100 text-red-600' : 'bg-blue-50 text-blue-600'}`}>
            {dataset.data.length} Tracked Units
          </span>
        </div>
        <EquipmentTable data={dataset.data} thresholds={thresholds} />
      </div>
    </div>
  );
};

export default DatasetViewer;