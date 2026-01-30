
import React from 'react';
import { EquipmentSummary } from '../types';

interface SummaryStatsProps {
  summary: EquipmentSummary | null;
}

const SummaryStats: React.FC<SummaryStatsProps> = ({ summary }) => {
  const stats = [
    { 
      label: 'Flowrate', 
      value: summary ? `${summary.avg_flowrate.toFixed(1)} m³/h` : '--', 
      sub: 'System Average',
      color: 'blue' 
    },
    { 
      label: 'Pressure', 
      value: summary ? `${summary.avg_pressure.toFixed(1)} bar` : '--', 
      sub: 'Operating Mean',
      color: 'indigo' 
    },
    { 
      label: 'Temperature', 
      value: summary ? `${summary.avg_temperature.toFixed(0)} °C` : '--', 
      sub: 'Process Temp',
      color: 'orange' 
    },
    { 
      label: 'Equipment', 
      value: summary ? summary.total_count : '--', 
      sub: 'Total Assets',
      color: 'slate' 
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, i) => (
        <div key={i} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{stat.label}</p>
          <h4 className="text-2xl font-bold text-slate-800 mt-1">{stat.value}</h4>
          <p className="text-xs text-slate-500 mt-1">{stat.sub}</p>
        </div>
      ))}
    </div>
  );
};

export default SummaryStats;
