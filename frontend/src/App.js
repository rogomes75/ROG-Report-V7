import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';
import axios from 'axios';
import moment from 'moment-timezone';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

console.log('BACKEND_URL:', BACKEND_URL);
console.log('API URL:', API);
console.log('Using full backend URL for API calls');

const formatLATime = (date) => {
  return moment.utc(date).tz('America/Los_Angeles').format('MM/DD/YYYY');
};

const formatLADateTime = (date) => {
  return moment.utc(date).tz('America/Los_Angeles').format('MM/DD/YYYY hh:mm A');
};

const formatLATimeOnly = (date) => {
  return moment.utc(date).tz('America/Los_Angeles').format('hh:mm A');
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount || 0);
};

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

const Navigation = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-2 sm:px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2 sm:space-x-4">
            <h1 className="text-lg sm:text-2xl font-bold text-blue-600">ROG Pool Service</h1>
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase">
              {user?.role}
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-6">
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
              onClick={() => setActiveTab('reports-download')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'reports-download'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Reports
            </button>

            <div className="flex items-center space-x-2">
              <span className="text-gray-700 text-sm">{user?.username}</span>
              <button
                onClick={logout}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition text-sm"
              >
                Logout
              </button>
            </div>
          </div>

          <div className="md:hidden flex items-center space-x-2">
            <span className="text-gray-700 text-sm">{user?.username}</span>
            <button
              onClick={() => setShowMobileMenu(!showMobileMenu)}
              className="text-gray-600 hover:text-blue-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {showMobileMenu && (
          <div className="md:hidden border-t border-gray-200 py-4">
            <div className="flex flex-col space-y-2">
              {['reports', 'completed', 'clients', 'users', 'financial', 'reports-download'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => {
                    setActiveTab(tab);
                    setShowMobileMenu(false);
                  }}
                  className={`px-4 py-2 rounded-lg font-medium transition text-left ${
                    activeTab === tab
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  {tab === 'reports' && 'Services Reported'}
                  {tab === 'completed' && 'Services Completed'}
                  {tab === 'clients' && 'Clients Management'}
                  {tab === 'users' && 'Users'}
                  {tab === 'financial' && 'Financial'}
                  {tab === 'reports-download' && 'Reports'}
                </button>
              ))}
              
              <button
                onClick={logout}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition text-left mt-4"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('reports');
  
  const renderContent = () => {
    return (
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">
          {activeTab === 'reports' && 'Service Reports'}
          {activeTab === 'completed' && 'Services Completed'}
          {activeTab === 'clients' && 'Clients Management'}
          {activeTab === 'users' && 'Users Management'}
          {activeTab === 'financial' && 'Financial Reports'}
          {activeTab === 'reports-download' && 'Reports & Analytics'}
        </h2>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-center py-12">
            <div className="text-6xl mb-4">
              {activeTab === 'reports' && '📋'}
              {activeTab === 'completed' && '✅'}
              {activeTab === 'clients' && '👥'}
              {activeTab === 'users' && '👤'}
              {activeTab === 'financial' && '💰'}
              {activeTab === 'reports-download' && '📊'}
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              {activeTab === 'reports' && 'No service reports yet'}
              {activeTab === 'completed' && 'No completed services'}
              {activeTab === 'clients' && 'No clients yet'}
              {activeTab === 'users' && 'No users configured'}
              {activeTab === 'financial' && 'No financial data'}
              {activeTab === 'reports-download' && 'No reports generated'}
            </h3>
            <p className="text-gray-500">
              {activeTab === 'reports' && 'No service reports have been created yet.'}
              {activeTab === 'completed' && 'Completed services will appear here.'}
              {activeTab === 'clients' && 'Add your first client to get started.'}
              {activeTab === 'users' && 'User management features coming soon.'}
              {activeTab === 'financial' && 'Financial reports will be displayed here.'}
              {activeTab === 'reports-download' && 'Generate and download comprehensive reports.'}
            </p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      {renderContent()}
    </div>
  );
};

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
