
/**
 * ARCHITECTURE: /frontend-web/src/
 * Purpose: Main application component and layout orchestration.
 */

import React, { useState, useEffect } from 'react';
import { DatasetHistory, EquipmentData } from './types';
import { equipmentService } from './api';
import Navbar from './components/Navbar';
import SummaryStats from './components/SummaryStats';
import UploadSection from './components/UploadSection';
import EquipmentTable from './components/EquipmentTable';
import EquipmentCharts from './components/EquipmentCharts';

const App: React.FC = () => {
  const [currentDataset, setCurrentDataset] = useState<DatasetHistory | null>(null);
  const [history, setHistory] = useState<DatasetHistory[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Initial load logic
    const loadHistory = async () => {
      try {
        const hist = await equipmentService.getHistory();
        setHistory(hist);
      } catch (err) {
        console.error("Failed to load history", err);
      }
    };
    loadHistory();
  }, []);

  const handleUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await equipmentService.uploadCsv(file);
      setCurrentDataset(result);
      setHistory(prev => {
        // Only add if it's not already the first one (simple mock logic)
        if (prev[0]?.filename === result.filename) return prev;
        return [result, ...prev].slice(0, 5);
      });
    } catch (err) {
      setError("Failed to upload file. Please ensure it is a valid CSV.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!currentDataset || isGeneratingPdf) return;
    
    setIsGeneratingPdf(true);
    try {
      await equipmentService.generatePdf(currentDataset);
    } catch (err) {
      setError("Failed to generate PDF report.");
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar 
        onGenerateReport={handleGenerateReport} 
        canGenerate={!!currentDataset && !isGeneratingPdf} 
      />
      
      {isGeneratingPdf && (
        <div className="fixed top-0 left-0 w-full h-1 bg-blue-100 z-[60]">
          <div className="h-full bg-blue-600 animate-[loading_1.5s_ease-in-out_infinite] w-1/3 origin-left"></div>
          <style>{`
            @keyframes loading {
              0% { transform: translateX(-100%) scaleX(0.5); }
              50% { transform: translateX(50%) scaleX(1); }
              100% { transform: translateX(200%) scaleX(0.5); }
            }
          `}</style>
        </div>
      )}

      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="flex flex-col gap-8">
          {/* Header & Upload */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <UploadSection onUpload={handleUpload} isLoading={isLoading} />
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                  {error}
                </div>
              )}
            </div>
            
            <div className="lg:col-span-2">
              <SummaryStats summary={currentDataset?.summary || null} />
            </div>
          </section>

          {currentDataset ? (
            <>
              {/* Visualizations */}
              <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <EquipmentCharts data={currentDataset.data} />
              </section>

              {/* Data Table */}
              <section className="glass-effect rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-slate-800">Detailed Equipment Parameters</h3>
                  <span className="text-sm text-slate-500">Source: {currentDataset.filename}</span>
                </div>
                <EquipmentTable data={currentDataset.data} />
              </section>
            </>
          ) : (
            <section className="flex flex-col items-center justify-center py-24 text-center">
              <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 className="text-xl font-medium text-slate-600">No Data Uploaded</h2>
              <p className="text-slate-400 mt-2 max-w-xs">Upload a chemical equipment CSV file to see real-time analytics and visualizations.</p>
            </section>
          )}

          {/* History Sidebar/Section */}
          {history.length > 0 && (
            <section className="mt-8 border-t border-slate-200 pt-8">
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Recent Uploads</h3>
              <div className="flex gap-4 overflow-x-auto pb-4">
                {history.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setCurrentDataset(item)}
                    className={`flex-shrink-0 px-4 py-3 rounded-xl border transition-all text-left w-48 ${
                      currentDataset?.id === item.id 
                      ? 'bg-blue-50 border-blue-200 ring-2 ring-blue-500 ring-opacity-50' 
                      : 'bg-white border-slate-200 hover:border-blue-300'
                    }`}
                  >
                    <div className="text-xs font-semibold text-blue-600 mb-1">
                      {new Date(item.timestamp).toLocaleDateString()}
                    </div>
                    <div className="text-sm font-medium text-slate-800 truncate">{item.filename}</div>
                    <div className="text-xs text-slate-500 mt-2">{item.summary.total_count} assets</div>
                  </button>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      <footer className="py-8 bg-white border-t border-slate-200">
        <div className="container mx-auto px-4 text-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} ChemEquip Visualizer. Hybrid Web/Desktop Analytics Suite.
        </div>
      </footer>
    </div>
  );
};

export default App;
