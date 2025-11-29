import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { broadcastService, authService } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [broadcasts, setBroadcasts] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [selectedBroadcast, setSelectedBroadcast] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    loadData();
  }, [navigate]);

  const loadData = async () => {
    try {
      setLoading(true);
      const userRes = await authService.getCurrentUser();
      setUser(userRes.data);

      const broadcastsRes = await broadcastService.listBroadcasts();
      setBroadcasts(broadcastsRes.data.broadcasts);
    } catch (err) {
      setError('Failed to load data');
      if (err.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBroadcast = async (e) => {
    e.preventDefault();
    try {
      const response = await broadcastService.createBroadcast(title, message);
      setBroadcasts([response.data.broadcast, ...broadcasts]);
      setTitle('');
      setMessage('');
      setShowCreateForm(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create broadcast');
    }
  };

  const handleSendBroadcast = async (broadcastId) => {
    try {
      const response = await broadcastService.sendBroadcast(broadcastId);
      setBroadcasts(
        broadcasts.map((b) =>
          b.id === broadcastId ? { ...b, status: 'sent', sent_at: new Date().toISOString() } : b
        )
      );
      alert(`Broadcast sent to ${response.data.send_result.sent_count} user(s)`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send broadcast');
    }
  };

  const handleDeleteBroadcast = async (broadcastId) => {
    if (!window.confirm('Are you sure you want to delete this broadcast?')) return;
    try {
      await broadcastService.deleteBroadcast(broadcastId);
      setBroadcasts(broadcasts.filter((b) => b.id !== broadcastId));
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete broadcast');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (loading) {
    return <div className="dashboard-container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Broadcast Management</h1>
          {user && (
            <div className="user-info">
              <span>Welcome, {user.username}!</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          )}
        </div>
      </header>

      <main className="dashboard-main">
        {error && <div className="error-message">{error}</div>}

        <section className="create-section">
          {!showCreateForm ? (
            <button
              onClick={() => setShowCreateForm(true)}
              className="create-btn"
            >
              + Create New Broadcast
            </button>
          ) : (
            <div className="create-form-container">
              <h2>Create New Broadcast</h2>
              <form onSubmit={handleCreateBroadcast}>
                <input
                  type="text"
                  placeholder="Broadcast Title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
                <textarea
                  placeholder="Broadcast Message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows="6"
                  required
                ></textarea>
                <div className="form-actions">
                  <button type="submit" className="submit-btn">Create Broadcast</button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="cancel-btn"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}
        </section>

        <section className="broadcasts-section">
          <h2>Your Broadcasts</h2>
          {broadcasts.length === 0 ? (
            <p className="no-broadcasts">No broadcasts yet. Create one to get started!</p>
          ) : (
            <div className="broadcasts-grid">
              {broadcasts.map((broadcast) => (
                <div key={broadcast.id} className="broadcast-card">
                  <div className="broadcast-header">
                    <h3>{broadcast.title}</h3>
                    <span className={`status-badge status-${broadcast.status}`}>
                      {broadcast.status}
                    </span>
                  </div>
                  <p className="broadcast-message">{broadcast.message}</p>
                  <div className="broadcast-meta">
                    <small>Created: {new Date(broadcast.created_at).toLocaleString()}</small>
                  </div>
                  <div className="broadcast-actions">
                    {broadcast.status === 'draft' && (
                      <>
                        <button
                          onClick={() => handleSendBroadcast(broadcast.id)}
                          className="send-btn"
                        >
                          Send Broadcast
                        </button>
                        <button
                          onClick={() => handleDeleteBroadcast(broadcast.id)}
                          className="delete-btn"
                        >
                          Delete
                        </button>
                      </>
                    )}
                    {broadcast.status === 'sent' && (
                      <button
                        onClick={() => setSelectedBroadcast(broadcast)}
                        className="view-btn"
                      >
                        View Details
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
