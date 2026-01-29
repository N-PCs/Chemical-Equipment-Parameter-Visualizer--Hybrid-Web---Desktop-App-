import React, { useState, useRef } from 'react';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { uploadFile } from '../../services/api';
import './UploadForm.css';

interface UploadFormProps {
  onUploadSuccess: (uploadId: number) => void;
}

export const UploadForm: React.FC<UploadFormProps> = ({ onUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      setError('Please upload a valid CSV file.');
      return;
    }
    setError(null);
    setFile(file);
  };

  const handleSubmit = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const response = await uploadFile(file);
      onUploadSuccess(response.id);
      setFile(null); // Reset after success
    } catch (err) {
      setError('Failed to upload file. Please try again.');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card title="Upload Dataset" className="upload-card">
       <div 
        className={`drop-zone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <input 
          ref={inputRef}
          type="file" 
          accept=".csv"
          onChange={handleChange} 
          hidden 
        />
        
        <div className="drop-zone-content">
          <div className="upload-icon">
            {file ? '📄' : '☁️'}
          </div>
          {file ? (
            <div className="file-info">
              <p className="file-name">{file.name}</p>
              <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          ) : (
            <>
              <p className="drop-text">Drag & Drop your CSV file here</p>
              <p className="or-text">or click to browse</p>
            </>
          )}
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="upload-actions">
        {file && (
          <Button 
            onClick={(e) => { e.stopPropagation(); handleSubmit(); }} 
            isLoading={uploading}
            className="w-full"
          >
            {uploading ? 'Processing...' : 'Analyze Data'}
          </Button>
        )}
      </div>
    </Card>
  );
};
