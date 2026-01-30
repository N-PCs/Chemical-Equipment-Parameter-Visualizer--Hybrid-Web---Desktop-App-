
/**
 * ARCHITECTURE: /frontend-web/src/components/
 * Purpose: Interactive data visualization using Chart.js.
 */

import React, { useEffect, useRef } from 'react';
import { EquipmentData } from '../types';

interface EquipmentChartsProps {
  data: EquipmentData[];
}

const EquipmentCharts: React.FC<EquipmentChartsProps> = ({ data }) => {
  const barChartRef = useRef<HTMLCanvasElement>(null);
  const pieChartRef = useRef<HTMLCanvasElement>(null);
  const chartInstances = useRef<{ bar?: any, pie?: any }>({});

  useEffect(() => {
    if (!data.length) return;

    // Helper to cleanup charts
    const cleanup = () => {
      if (chartInstances.current.bar) chartInstances.current.bar.destroy();
      if (chartInstances.current.pie) chartInstances.current.pie.destroy();
    };

    cleanup();

    // Prepare Data for Comparison Bar Chart
    const labels = data.map(d => d.equipment_name);
    const flowData = data.map(d => d.flowrate);
    const pressureData = data.map(d => d.pressure);

    if (barChartRef.current) {
      chartInstances.current.bar = new (window as any).Chart(barChartRef.current, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Flowrate (m³/h)',
              data: flowData,
              backgroundColor: 'rgba(59, 130, 246, 0.7)',
              borderRadius: 4,
            },
            {
              label: 'Pressure (bar)',
              data: pressureData,
              backgroundColor: 'rgba(99, 102, 241, 0.7)',
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' as const },
            title: { display: true, text: 'Flowrate vs Pressure Comparison' }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }

    // Prepare Data for Type Distribution Pie Chart
    const dist: Record<string, number> = {};
    data.forEach(item => {
      dist[item.type] = (dist[item.type] || 0) + 1;
    });

    if (pieChartRef.current) {
      chartInstances.current.pie = new (window as any).Chart(pieChartRef.current, {
        type: 'doughnut',
        data: {
          labels: Object.keys(dist),
          datasets: [{
            data: Object.values(dist),
            backgroundColor: [
              'rgba(59, 130, 246, 0.8)',
              'rgba(16, 185, 129, 0.8)',
              'rgba(245, 158, 11, 0.8)',
              'rgba(139, 92, 246, 0.8)',
              'rgba(239, 68, 68, 0.8)',
            ],
            hoverOffset: 10
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' as const },
            title: { display: true, text: 'Equipment Type Distribution' }
          },
          cutout: '60%'
        }
      });
    }

    return cleanup;
  }, [data]);

  return (
    <>
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm h-[400px]">
        <canvas ref={barChartRef} />
      </div>
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm h-[400px]">
        <canvas ref={pieChartRef} />
      </div>
    </>
  );
};

export default EquipmentCharts;
