import React from 'react';
import { Card } from '../common/Card';
import type { SummaryStats as SummaryStatsType } from '../../services/api';
import './SummaryStats.css';

interface SummaryStatsProps {
  stats: SummaryStatsType;
}

export const SummaryStats: React.FC<SummaryStatsProps> = ({ stats }) => {
  return (
    <div className="stats-grid">
      <Card className="stat-card">
        <h3>Total Equipment</h3>
        <div className="stat-value">{stats.total_count}</div>
      </Card>
      <Card className="stat-card">
        <h3>Avg Flowrate</h3>
        <div className="stat-value">{stats.averages.flowrate}<span className="unit">m³/h</span></div>
      </Card>
      <Card className="stat-card">
        <h3>Avg Pressure</h3>
        <div className="stat-value">{stats.averages.pressure}<span className="unit">atm</span></div>
      </Card>
      <Card className="stat-card">
        <h3>Avg Temperat.</h3>
        <div className="stat-value">{stats.averages.temperature}<span className="unit">°C</span></div>
      </Card>
    </div>
  );
};
