import React, { useState, useEffect } from 'react';
import { UploadForm } from '../equipment/UploadForm';
import { EquipmentTable } from '../equipment/EquipmentTable';
import { SummaryStats } from './SummaryStats';
import { Charts } from './Charts';
import { getSummaryStats } from '../../services/api';
import type { SummaryStats as SummaryStatsType } from '../../services/api';
import './Dashboard.css';

export const Dashboard: React.FC = () => {
  const [uploadId, setUploadId] = useState<number | undefined>(undefined);
  const [stats, setStats] = useState<SummaryStatsType | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (uploadId) {
      fetchStats(uploadId);
    }
  }, [uploadId]);

  const fetchStats = async (id: number) => {
    setLoading(true);
    try {
      const data = await getSummaryStats(id);
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (id: number) => {
    setUploadId(id);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-section">
        <UploadForm onUploadSuccess={handleUploadSuccess} />
      </div>

      {stats && (
        <>
          <div className="dashboard-header">
            <h2>Analysis Results</h2>
            <p>Overview of the uploaded equipment data</p>
          </div>

          <SummaryStats stats={stats} />
          
          <Charts stats={stats} />
          
          <EquipmentTable uploadId={uploadId} />
        </>
      )}

      {loading && !stats && <div className="loading-state">Loading analysis...</div>}
    </div>
  );
};
