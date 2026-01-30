
import React from 'react';
import { EquipmentData } from '../types';

interface EquipmentTableProps {
  data: EquipmentData[];
}

const EquipmentTable: React.FC<EquipmentTableProps> = ({ data }) => {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-100">
            <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Name</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Type</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider text-right">Flow (m³/h)</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider text-right">Pressure (bar)</th>
            <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-wider text-right">Temp (°C)</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {data.map((item, index) => (
            <tr key={index} className="hover:bg-slate-50 transition-colors">
              <td className="px-6 py-4 font-medium text-slate-800">{item.equipment_name}</td>
              <td className="px-6 py-4">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
                  {item.type}
                </span>
              </td>
              <td className="px-6 py-4 text-right tabular-nums text-slate-600">{item.flowrate.toFixed(2)}</td>
              <td className="px-6 py-4 text-right tabular-nums text-slate-600">{item.pressure.toFixed(2)}</td>
              <td className="px-6 py-4 text-right tabular-nums text-slate-600 font-semibold text-blue-600">{item.temperature.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EquipmentTable;
