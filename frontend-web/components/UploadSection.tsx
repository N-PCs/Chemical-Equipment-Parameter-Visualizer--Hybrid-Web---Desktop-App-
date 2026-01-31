
import React, { useRef } from 'react';

interface UploadSectionProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

const UploadSection: React.FC<UploadSectionProps> = ({ onUpload, isLoading }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  const triggerUpload = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm h-full flex flex-col justify-center">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">Import Dataset</h3>
      <p className="text-sm text-slate-500 mb-6 leading-relaxed">
        Upload equipment parameter CSV or Excel files to run analytics and generate visualizations.
      </p>
      
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".csv, .xlsx, .xls"
        className="hidden" 
      />
      
      <button
        onClick={triggerUpload}
        disabled={isLoading}
        className={`w-full py-4 rounded-xl border-2 border-dashed flex flex-col items-center justify-center transition-all ${
          isLoading 
          ? 'bg-slate-50 border-slate-200 cursor-wait' 
          : 'bg-blue-50 border-blue-200 hover:border-blue-400 hover:bg-blue-100 group'
        }`}
      >
        {isLoading ? (
          <div className="flex flex-col items-center">
            <svg className="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="mt-2 text-sm font-medium text-blue-600">Processing Data...</span>
          </div>
        ) : (
          <>
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <span className="text-sm font-bold text-blue-600">Click to Upload File</span>
            <span className="text-xs text-slate-400 mt-1">or drag and drop here</span>
          </>
        )}
      </button>
      
      <div className="mt-4 flex items-center justify-between text-[10px] text-slate-400 font-bold uppercase tracking-widest px-1">
        <span>Max: 10MB</span>
        <span>Format: CSV or Excel</span>
      </div>
    </div>
  );
};

export default UploadSection;
