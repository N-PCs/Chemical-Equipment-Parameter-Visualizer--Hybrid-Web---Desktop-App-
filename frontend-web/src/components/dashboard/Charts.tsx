import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { Card } from '../common/Card';
import type { SummaryStats } from '../../services/api';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface ChartsProps {
  stats: SummaryStats;
}

export const Charts: React.FC<ChartsProps> = ({ stats }) => {
  const barData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Parameters',
        data: [stats.averages.flowrate, stats.averages.pressure, stats.averages.temperature],
        backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.7)'],
        borderColor: ['rgba(59, 130, 246, 1)', 'rgba(16, 185, 129, 1)', 'rgba(239, 68, 68, 1)'],
        borderWidth: 1,
      },
    ],
  };

  const pieData = {
    labels: stats.type_distribution.map((d) => d.equipment_type),
    datasets: [
      {
        data: stats.type_distribution.map((d) => d.count),
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: { color: '#94a3b8' }
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        ticks: { color: '#94a3b8' },
        grid: { color: '#334155' }
      },
      x: {
        ticks: { color: '#94a3b8' },
        grid: { display: false }
      }
    }
  };
  
  const pieOptions = {
      responsive: true,
      plugins: {
        legend: {
            position: 'right' as const,
            labels: { color: '#94a3b8' }
        }
      }
  }

  return (
    <div className="charts-grid">
      <Card title="Parameter Averages" className="chart-card">
        <Bar data={barData} options={options} />
      </Card>
      <Card title="Equipment Distribution" className="chart-card">
        <div className="pie-container">
            <Pie data={pieData} options={pieOptions} />
        </div>
      </Card>
    </div>
  );
};
