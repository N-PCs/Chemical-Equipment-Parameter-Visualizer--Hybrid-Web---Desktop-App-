import React, { useState, useEffect } from 'react';
import { UploadForm } from '../equipment/UploadForm';
import { EquipmentTable } from '../equipment/EquipmentTable';
import { SummaryStats } from './SummaryStats';
import { Charts } from './Charts';
import { getSummaryStats, downloadReport } from '../../services/api';
import type { SummaryStats as SummaryStatsType } from '../../services/api';
import './Dashboard.css';
import { Button } from '../common/Button';

export const Dashboard: React.FC = () => {
  const [currentUploadId, setCurrentUploadId] = useState<number | undefined>(undefined);
  const [stats, setStats] = useState<SummaryStatsType | null>(null);
  const [loading, setLoading] = useState(false);
  const [reportLoading, setReportLoading] = useState(false);

  useEffect(() => {
    if (currentUploadId) {
      loadData(currentUploadId);
    }
  }, [currentUploadId]);

  const loadData = async (id: number) => {
    setLoading(true);
    try {
      const s = await getSummaryStats(id);
      setStats(s);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (id: number) => {
    setCurrentUploadId(id);
  };

  const handleDownloadReport = async () => {
      if (!currentUploadId) return;
      setReportLoading(true);
      try {
          await downloadReport(currentUploadId);
      } catch (err) {
          console.error("Failed to download report", err);
          alert("Failed to download report");
      } finally {
          setReportLoading(false);
      }
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
         <h2>Dashboard</h2>
         {currentUploadId && (
             <Button 
                onClick={handleDownloadReport} 
                variant="secondary" 
                isLoading={reportLoading}
             >
                 Download PDF Report
             </Button>
         )}
      </div>
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
          
          <EquipmentTable uploadId={currentUploadId} />
        </>
      )}

      {loading && !stats && <div className="loading-state">Loading analysis...</div>}
    </div>
  );
};
