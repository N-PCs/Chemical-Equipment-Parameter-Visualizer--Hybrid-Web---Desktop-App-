import React, { useEffect, useState } from 'react';
import { Card } from '../common/Card';
import { getEquipmentList } from '../../services/api';
import type { Equipment } from '../../services/api';
import './EquipmentTable.css';

interface EquipmentTableProps {
  uploadId?: number;
}

export const EquipmentTable: React.FC<EquipmentTableProps> = ({ uploadId }) => {
  const [data, setData] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (uploadId) {
      fetchData();
    }
  }, [uploadId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const result = await getEquipmentList(uploadId);
      setData(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!uploadId) return null;

  return (
    <Card title="Equipment Data" className="table-card">
      <div className="table-responsive">
        <table className="equipment-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate (m³/h)</th>
              <th>Pressure (atm)</th>
              <th>Temperature (°C)</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="text-center">Loading...</td></tr>
            ) : data.length === 0 ? (
              <tr><td colSpan={5} className="text-center">No data available</td></tr>
            ) : (
              data.map((item) => (
                <tr key={item.id}>
                  <td>{item.equipment_name}</td>
                  <td><span className="badge-type">{item.equipment_type}</span></td>
                  <td>{item.flowrate}</td>
                  <td>{item.pressure}</td>
                  <td>{item.temperature}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
};
