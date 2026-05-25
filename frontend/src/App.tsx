import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function App() {
  const [sources, setSources] = useState<any[]>([]);
  const [activities, setActivities] = useState<any[]>([]);
  const [selectedSource, setSelectedSource] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchSources();
    fetchActivities();
  }, []);

  const fetchSources = async () => {
    try {
      const res = await fetch(`${API_BASE}/sources/`);
      const data = await res.json();
      setSources(data);
      if (data.length > 0) setSelectedSource(data[0].id);
    } catch (e) {
      console.error('Failed to fetch sources', e);
    }
  };

  const fetchActivities = async () => {
    try {
      const res = await fetch(`${API_BASE}/activities/`);
      const data = await res.json();
      setActivities(data);
    } catch (e) {
      console.error('Failed to fetch activities', e);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !selectedSource) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('data_source_id', selectedSource);

    try {
      const res = await fetch(`${API_BASE}/uploads/upload/`, {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        alert('Upload successful');
        setFile(null);
        fetchActivities();
      } else {
        alert('Upload failed');
      }
    } catch (e) {
      console.error(e);
      alert('Upload error');
    } finally {
      setUploading(false);
    }
  };

  const handleAction = async (id: string, action: 'approve' | 'reject') => {
    try {
      const res = await fetch(`${API_BASE}/activities/${id}/${action}/`, {
        method: 'POST',
      });
      if (res.ok) {
        fetchActivities();
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Breathe ESG - Analyst Dashboard</h1>
      </header>

      <div className="card">
        <h2 className="card-title">Ingest Data</h2>
        <form onSubmit={handleUpload}>
          <div className="form-group">
            <label>Data Source</label>
            <select
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
            >
              {sources.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.source_type})
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>File (CSV)</label>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </div>
          <button type="submit" disabled={!file || uploading}>
            {uploading ? 'Uploading...' : 'Upload & Normalize'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2 className="card-title">Review & Approve Data</h2>
        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Scope</th>
                <th>Date Start</th>
                <th>Date End</th>
                <th>Normalized Qty</th>
                <th>Unit</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((act) => (
                <tr key={act.id}>
                  <td>{act.activity_type}</td>
                  <td>{act.scope}</td>
                  <td>{act.date_start}</td>
                  <td>{act.date_end}</td>
                  <td>
                    {act.normalized_quantity !== null
                      ? act.normalized_quantity.toFixed(2)
                      : 'N/A'}
                  </td>
                  <td>{act.normalized_unit}</td>
                  <td>
                    <span
                      className={`status-badge status-${act.status
                        .toLowerCase()
                        .replace('_review', '')}`}
                    >
                      {act.status}
                    </span>
                    {act.validation_errors && (
                      <span className="error-text">
                        Error parsing raw row
                      </span>
                    )}
                  </td>
                  <td>
                    {act.status === 'PENDING_REVIEW' && (
                      <>
                        <button
                          className="action-btn btn-approve"
                          onClick={() => handleAction(act.id, 'approve')}
                        >
                          Approve
                        </button>
                        <button
                          className="action-btn btn-reject"
                          onClick={() => handleAction(act.id, 'reject')}
                        >
                          Reject
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
              {activities.length === 0 && (
                <tr>
                  <td colSpan={8} style={{ textAlign: 'center' }}>
                    No activity data available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
