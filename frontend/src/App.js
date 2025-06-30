import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';
import axios from 'axios';
import moment from 'moment-timezone';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

// Debug logging
console.log('BACKEND_URL:', BACKEND_URL);
console.log('API URL:', API);

// Utility function to format LA time
const formatLATime = (date) => {
  return moment.utc(date).tz('America/Los_Angeles').format('MM/DD/YYYY');
};

const formatLADateTime = (date) => {
  return moment.utc(date).tz('America/Los_Angeles').format('MM/DD/YYYY hh:mm A');
};

// Format currency
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount || 0);
};

// Auth Context
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      logout();
    }
  };

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, { username, password });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Login Component
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const success = await login(username, password);
    if (!success) {
      setError('Invalid username or password');
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-blue-600 mb-4">ROG Pool Service</h1>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="Enter your username"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="Enter your password"
              required
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition duration-200 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Please contact your administrator for login credentials</p>
        </div>
      </div>
    </div>
  );
};

// Navigation Component  
const Navigation = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-blue-600">ROG Pool Service</h1>
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase">
              {user?.role}
            </span>
          </div>

          <div className="flex items-center space-x-6">
            <button
              onClick={() => setActiveTab('reports')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'reports'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Services Reported
            </button>
            <button
              onClick={() => setActiveTab('completed')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'completed'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Services Completed
            </button>
            <button
              onClick={() => setActiveTab('clients')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'clients'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Clients Management
            </button>
            <button
              onClick={() => setActiveTab('users')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'users'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Users
            </button>
            <button
              onClick={() => setActiveTab('financial')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'financial'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Financial
            </button>
            <button
              onClick={() => setActiveTab('reports-tab')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'reports-tab'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Reports
            </button>
            <span className="text-gray-600">{user?.username}</span>
            <button
              onClick={logout}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

// Main Dashboard Component
const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('reports');
  const [clients, setClients] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [clientsRes, reportsRes] = await Promise.all([
        axios.get(`${API}/clients`),
        axios.get(`${API}/reports`)
      ]);
      setClients(clientsRes.data);
      setReports(reportsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="text-lg text-gray-600">Loading...</div>
        </div>
      );
    }

    switch (activeTab) {
      case 'reports':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-800">Service Reports</h2>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                Add Report
              </button>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-center">Period: No reports</div>
              <div className="flex space-x-4 mt-4">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">Scheduled: 0</span>
                <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">In Progress: 0</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Reported: {reports.length}</span>
                <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">Late: 0</span>
              </div>
              
              <div className="mt-8">
                <select className="border border-gray-300 rounded px-3 py-2 mb-4">
                  <option>All Users</option>
                </select>
                
                {reports.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="text-6xl mb-4">📋</div>
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">No service reports yet</h3>
                    <p className="text-gray-500">No service reports have been created yet.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {reports.map(report => (
                      <div key={report.id} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="font-semibold">{report.title}</h4>
                            <p className="text-gray-600">{report.description}</p>
                            <span className="inline-block bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs mt-2">
                              {report.priority}
                            </span>
                          </div>
                          <div className="text-right text-sm text-gray-500">
                            <div>Created: {formatLADateTime(report.created_at)}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        );
        
      case 'completed':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800">Services Completed</h2>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-center py-12">
                <div className="text-6xl mb-4">✅</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">No completed services</h3>
                <p className="text-gray-500">Completed services will appear here.</p>
              </div>
            </div>
          </div>
        );
        
      case 'clients':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-800">Clients Management</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                Add Client
              </button>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              {clients.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">👥</div>
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">No clients yet</h3>
                  <p className="text-gray-500">Add your first client to get started.</p>
                </div>
              ) : (
                <div className="grid gap-4">
                  {clients.map(client => (
                    <div key={client.id} className="border rounded-lg p-4">
                      <h4 className="font-semibold text-lg">{client.name}</h4>
                      <p className="text-gray-600">{client.address}</p>
                      <div className="mt-2 space-x-4">
                        {client.phone && <span className="text-sm text-gray-500">📞 {client.phone}</span>}
                        {client.email && <span className="text-sm text-gray-500">✉️ {client.email}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
        
      default:
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold text-gray-700 mb-2">{activeTab} Section</h3>
              <p className="text-gray-500">This section is under development.</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="max-w-7xl mx-auto px-4 py-6">
        {renderContent()}
      </div>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

const AppContent = () => {
  const { user } = useAuth();
  
  if (!user) {
    return <Login />;
  }
  
  return <Dashboard />;
};

export default App;
