import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';
import axios from 'axios';
import moment from 'moment-timezone';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Utility function to format LA time
const formatLATime = (date) => {
  return moment(date).tz('America/Los_Angeles').format('MM/DD/YYYY');
};

const formatLADateTime = (date) => {
  return moment(date).tz('America/Los_Angeles').format('MM/DD/YYYY hh:mm A');
};

const formatLATimeOnly = (date) => {
  return moment(date).tz('America/Los_Angeles').format('hh:mm A');
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
          <div className="flex justify-center mb-4">
            <img 
              src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDQwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9IjgwIiBjeT0iNzUiIHI9IjUwIiBzdHJva2U9IiMzMTc0QkIiIHN0cm9rZS13aWR0aD0iNiIgZmlsbD0ibm9uZSIvPgo8cGF0aCBkPSJNNDUgNzVDNDUgNzUgNTUgNjAgNzAgNjBDODUgNjAgOTUgNzUgOTUgNzVDOTUgNzUgODUgOTAgNzAgOTBDNTUgOTAgNDUgNzUgNDUgNzVaIiBmaWxsPSIjMzE3NEJCIi8+CjxwYXRoIGQ9Ik02MCA2NUM2MCA2NSA2NSA1NSA3NSA1NUM4NSA1NSA5MCA2NSA5MCA2NSIgc3Ryb2tlPSIjMzE3NEJCIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9Im5vbmUiLz4KPHBhdGggZD0iTTYwIDg1QzYwIDg1IDY1IDk1IDc1IDk1Qzg1IDk1IDkwIDg1IDkwIDg1IiBzdHJva2U9IiMzMTc0QkIiIHN0cm9rZS13aWR0aD0iMyIgZmlsbD0ibm9uZSIvPgo8dGV4dCB4PSIxMzAiIHk9IjY1IiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iNDgiIGZvbnQtd2VpZ2h0PSJib2xkIiBmaWxsPSIjMzE3NEJCIj5ST0c8L3RleHQ+Cjx0ZXh0IHg9IjEzMCIgeT0iOTUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzMxNzRCQiI+UG9vbCBTZXJ2aWNlPC90ZXh0Pgo8L3N2Zz4=" 
              alt="ROG Pool Service" 
              className="h-16 w-auto"
            />
          </div>
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
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-2 sm:px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2 sm:space-x-4">
            <img 
              src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDQwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9IjgwIiBjeT0iNzUiIHI9IjUwIiBzdHJva2U9IiMzMTc0QkIiIHN0cm9rZS13aWR0aD0iNiIgZmlsbD0ibm9uZSIvPgo8cGF0aCBkPSJNNDUgNzVDNDUgNzUgNTUgNjAgNzAgNjBDODUgNjAgOTUgNzUgOTUgNzVDOTUgNzUgODUgOTAgNzAgOTBDNTUgOTAgNDUgNzUgNDUgNzVaIiBmaWxsPSIjMzE3NEJCIi8+CjxwYXRoIGQ9Ik02MCA2NUM2MCA2NSA2NSA1NSA3NSA1NUM4NSA1NSA5MCA2NSA5MCA2NSIgc3Ryb2tlPSIjMzE3NEJCIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9Im5vbmUiLz4KPHBhdGggZD0iTTYwIDg1QzYwIDg1IDY1IDk1IDc1IDk1Qzg1IDk1IDkwIDg1IDkwIDg1IiBzdHJva2U9IiMzMTc0QkIiIHN0cm9rZS13aWR0aD0iMyIgZmlsbD0ibm9uZSIvPgo8dGV4dCB4PSIxMzAiIHk9IjY1IiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iNDgiIGZvbnQtd2VpZ2h0PSJib2xkIiBmaWxsPSIjMzE3NEJCIj5ST0c8L3RleHQ+Cjx0ZXh0IHg9IjEzMCIgeT0iOTUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzMxNzRCQiI+UG9vbCBTZXJ2aWNlPC90ZXh0Pgo8L3N2Zz4=" 
              alt="ROG Pool Service" 
              className="h-8 w-auto sm:h-10"
            />
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full uppercase">
              {user?.role}
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <button
              onClick={() => setActiveTab('reports')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'reports'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Reports
            </button>
            
            <button
              onClick={() => setActiveTab('completed')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'completed'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              Completed
            </button>
            
            {user?.role === 'admin' && (
              <>
                <button
                  onClick={() => setActiveTab('clients')}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    activeTab === 'clients'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Clients
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
              </>
            )}

            <div className="flex items-center space-x-2">
              <span className="text-gray-700 text-sm">{user?.username}</span>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition text-sm"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Mobile Menu Button */}
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

        {/* Mobile Menu */}
        {showMobileMenu && (
          <div className="md:hidden border-t border-gray-200 py-4">
            <div className="flex flex-col space-y-2">
              <button
                onClick={() => {
                  setActiveTab('reports');
                  setShowMobileMenu(false);
                }}
                className={`px-4 py-2 rounded-lg font-medium transition text-left ${
                  activeTab === 'reports'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-blue-600'
                }`}
              >
                Reports
              </button>
              
              <button
                onClick={() => {
                  setActiveTab('completed');
                  setShowMobileMenu(false);
                }}
                className={`px-4 py-2 rounded-lg font-medium transition text-left ${
                  activeTab === 'completed'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-blue-600'
                }`}
              >
                Completed
              </button>
              
              {user?.role === 'admin' && (
                <>
                  <button
                    onClick={() => {
                      setActiveTab('clients');
                      setShowMobileMenu(false);
                    }}
                    className={`px-4 py-2 rounded-lg font-medium transition text-left ${
                      activeTab === 'clients'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-600 hover:text-blue-600'
                    }`}
                  >
                    Clients
                  </button>
                  <button
                    onClick={() => {
                      setActiveTab('users');
                      setShowMobileMenu(false);
                    }}
                    className={`px-4 py-2 rounded-lg font-medium transition text-left ${
                      activeTab === 'users'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-600 hover:text-blue-600'
                    }`}
                  >
                    Users
                  </button>
                </>
              )}
              
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition text-left mt-4"
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

// Service Reports Component
const ServiceReports = () => {
  const { user } = useAuth();
  const [reports, setReports] = useState([]);
  const [filteredReports, setFilteredReports] = useState([]);
  const [clients, setClients] = useState([]);
  const [users, setUsers] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingReport, setEditingReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedUserFilter, setSelectedUserFilter] = useState('');

  // Form states
  const [selectedClient, setSelectedClient] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('SAME WEEK');
  const [photos, setPhotos] = useState([]);
  const [employeeNotes, setEmployeeNotes] = useState('');
  const [adminNotes, setAdminNotes] = useState('');
  const [totalCost, setTotalCost] = useState('');
  const [partsCost, setPartsCost] = useState('');
  const [grossProfit, setGrossProfit] = useState('');

  useEffect(() => {
    fetchReports();
    fetchClients();
    if (user?.role === 'admin') {
      fetchUsers();
    }
  }, []);

  useEffect(() => {
    filterReports();
  }, [reports, selectedUserFilter]);

  const filterReports = () => {
    let filtered = reports;
    
    if (selectedUserFilter) {
      filtered = filtered.filter(report => report.employee_id === selectedUserFilter);
    }
    
    setFilteredReports(filtered);
  };

  const fetchReports = async () => {
    try {
      const response = await axios.get(`${API}/reports`);
      // Filter out completed reports - they should only appear in Completed tab
      const activeReports = response.data.filter(report => report.status !== 'completed');
      setReports(activeReports);
    } catch (error) {
      console.error('Failed to fetch reports:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/users`);
      setUsers(response.data.filter(u => u.role === 'employee'));
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Failed to fetch clients:', error);
    }
  };

  const handlePhotoUpload = (e) => {
    const files = Array.from(e.target.files);
    if (photos.length + files.length > 5) {
      alert('Maximum 5 photos allowed');
      return;
    }

    files.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        setPhotos(prev => [...prev, event.target.result]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removePhoto = (index) => {
    setPhotos(prev => prev.filter((_, i) => i !== index));
  };

  const resetForm = () => {
    setSelectedClient('');
    setDescription('');
    setPriority('SAME WEEK');
    setPhotos([]);
    setEmployeeNotes('');
    setAdminNotes('');
    setTotalCost('');
    setPartsCost('');
    setGrossProfit('');
    setEditingReport(null);
  };

  const handleCreateReport = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await axios.post(`${API}/reports`, {
        client_id: selectedClient,
        description,
        priority,
        photos
      });

      setShowCreateForm(false);
      resetForm();
      fetchReports();
    } catch (error) {
      console.error('Failed to create report:', error);
      alert('Failed to create report');
    }
    setIsLoading(false);
  };

  const handleEditReport = (report) => {
    setEditingReport(report);
    setSelectedClient(report.client_id);
    setDescription(report.description);
    setPriority(report.priority);
    setPhotos(report.photos || []);
    setEmployeeNotes(report.employee_notes || '');
    setAdminNotes(report.admin_notes || '');
    setTotalCost(report.total_cost?.toString() || '');
    setPartsCost(report.parts_cost?.toString() || '');
    setGrossProfit(report.gross_profit?.toString() || '');
    setShowEditForm(true);
  };

  const handleUpdateReport = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const updateData = {
        description,
        priority,
        photos,
        employee_notes: employeeNotes
      };

      if (user?.role === 'admin') {
        updateData.admin_notes = adminNotes;
        if (totalCost) updateData.total_cost = parseFloat(totalCost);
        if (partsCost) updateData.parts_cost = parseFloat(partsCost);
        if (totalCost && partsCost) {
          updateData.gross_profit = parseFloat(totalCost) - parseFloat(partsCost);
        }
      }

      await axios.put(`${API}/reports/${editingReport.id}`, updateData);

      setShowEditForm(false);
      resetForm();
      fetchReports();
    } catch (error) {
      console.error('Failed to update report:', error);
      alert('Failed to update report');
    }
    setIsLoading(false);
  };

  const updateReportStatus = async (reportId, status, notes = '', completionDate = null) => {
    try {
      await axios.put(`${API}/reports/${reportId}`, {
        status,
        admin_notes: notes,
        completion_date: completionDate
      });
      fetchReports();
    } catch (error) {
      console.error('Failed to update report:', error);
    }
  };
  const updateFinancialField = async (reportId, field, value) => {
    try {
      await axios.put(`${API}/reports/${reportId}`, {
        [field]: value
      });
      fetchReports();
    } catch (error) {
      console.error(`Failed to update ${field}:`, error);
    }
  };


  const updateAdminNotes = async (reportId, notes) => {
    try {
      await axios.put(`${API}/reports/${reportId}`, {
        admin_notes: notes
      });
      fetchReports();
    } catch (error) {
      console.error('Failed to update admin notes:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'reported': 'bg-yellow-100 text-yellow-800',
      'scheduled': 'bg-blue-100 text-blue-800',
      'in_progress': 'bg-orange-100 text-orange-800',
      'completed': 'bg-green-100 text-green-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'URGENT': 'bg-red-100 text-red-800',
      'SAME WEEK': 'bg-orange-100 text-orange-800',
      'NEXT WEEK': 'bg-blue-100 text-blue-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-7xl mx-auto px-2 sm:px-4 py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">Service Reports</h2>
          <div className="mt-2 flex flex-wrap gap-4 text-sm">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
              Scheduled: {reports.filter(r => r.status === 'scheduled').length}
            </span>
            <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full">
              In Progress: {reports.filter(r => r.status === 'in_progress').length}
            </span>
            <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full">
              Reported: {reports.filter(r => r.status === 'reported').length}
            </span>
          </div>
        </div>
        {user?.role === 'employee' && (
          <button
            onClick={() => setShowCreateForm(true)}
            className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 sm:px-6 py-3 rounded-lg font-semibold transition flex items-center justify-center space-x-2"
          >
            <span>+</span>
            <span>New Report</span>
          </button>
        )}
      </div>

      {/* Create Report Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-50">
          <div className="bg-white rounded-xl p-4 sm:p-6 w-full max-w-2xl max-h-screen overflow-y-auto">
            <h3 className="text-xl sm:text-2xl font-bold mb-4">Create Service Report</h3>
            
            <form onSubmit={handleCreateReport} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Client</label>
                <select
                  value={selectedClient}
                  onChange={(e) => setSelectedClient(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                  required
                >
                  <option value="">Select a client</option>
                  {clients.map(client => (
                    <option key={client.id} value={client.id}>
                      {client.name} - {client.address}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                  required
                >
                  <option value="URGENT">URGENT</option>
                  <option value="SAME WEEK">SAME WEEK</option>
                  <option value="NEXT WEEK">NEXT WEEK</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none h-24 sm:h-32 resize-none text-sm sm:text-base"
                  placeholder="Describe the maintenance issue..."
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Photos ({photos.length}/5)
                </label>
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  capture="environment"
                  onChange={handlePhotoUpload}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                />
                
                {photos.length > 0 && (
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4">
                    {photos.map((photo, index) => (
                      <div key={index} className="relative">
                        <img
                          src={photo}
                          alt={`Upload ${index + 1}`}
                          className="w-full h-20 sm:h-24 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removePhoto(index)}
                          className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center text-xs sm:text-sm"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full sm:flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
                >
                  {isLoading ? 'Creating...' : 'Create Report'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false);
                    resetForm();
                  }}
                  className="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 py-3 rounded-lg font-semibold transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Report Modal */}
      {showEditForm && editingReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-50">
          <div className="bg-white rounded-xl p-4 sm:p-6 w-full max-w-2xl max-h-screen overflow-y-auto">
            <h3 className="text-xl sm:text-2xl font-bold mb-4">Edit Service Report</h3>
            
            <form onSubmit={handleUpdateReport} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Client</label>
                <select
                  value={selectedClient}
                  onChange={(e) => setSelectedClient(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                  required
                >
                  <option value="">Select a client</option>
                  {clients.map(client => (
                    <option key={client.id} value={client.id}>
                      {client.name} - {client.address}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                  required
                >
                  <option value="URGENT">URGENT</option>
                  <option value="SAME WEEK">SAME WEEK</option>
                  <option value="NEXT WEEK">NEXT WEEK</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none h-24 sm:h-32 resize-none text-sm sm:text-base"
                  placeholder="Describe the maintenance issue..."
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Employee Notes</label>
                <textarea
                  value={employeeNotes}
                  onChange={(e) => setEmployeeNotes(e.target.value)}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none h-20 resize-none text-sm sm:text-base"
                  placeholder="Add any additional notes..."
                />
              </div>

              {user?.role === 'admin' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Admin Notes</label>
                    <textarea
                      value={adminNotes}
                      onChange={(e) => setAdminNotes(e.target.value)}
                      className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none h-20 resize-none text-sm sm:text-base"
                      placeholder="Admin notes..."
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Estimate ($)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={totalCost}
                        onChange={(e) => {
                          setTotalCost(e.target.value);
                          if (partsCost && e.target.value) {
                            setGrossProfit((parseFloat(e.target.value) - parseFloat(partsCost)).toFixed(2));
                          }
                        }}
                        className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                        placeholder="0.00"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Cost of Services ($)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={partsCost}
                        onChange={(e) => {
                          setPartsCost(e.target.value);
                          if (totalCost && e.target.value) {
                            setGrossProfit((parseFloat(totalCost) - parseFloat(e.target.value)).toFixed(2));
                          }
                        }}
                        className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                        placeholder="0.00"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Gross Profit ($)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={grossProfit}
                        readOnly
                        className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg bg-gray-100 text-sm sm:text-base"
                        placeholder="0.00"
                      />
                    </div>
                  </div>
                </>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Photos ({photos.length}/5)
                </label>
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  capture="environment"
                  onChange={handlePhotoUpload}
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                />
                
                {photos.length > 0 && (
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4">
                    {photos.map((photo, index) => (
                      <div key={index} className="relative">
                        <img
                          src={photo}
                          alt={`Photo ${index + 1}`}
                          className="w-full h-20 sm:h-24 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removePhoto(index)}
                          className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center text-xs sm:text-sm"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full sm:flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
                >
                  {isLoading ? 'Updating...' : 'Update Report'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowEditForm(false);
                    resetForm();
                  }}
                  className="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 py-3 rounded-lg font-semibold transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Reports List */}
      <div className="space-y-4 sm:space-y-6">
        {reports.map(report => (
          <div key={report.id} className="bg-white rounded-xl shadow-lg p-4 sm:p-6">
            <div className="flex flex-col sm:flex-row justify-between items-start mb-4 gap-4">
              <div className="flex-1">
                <h3 className="text-lg sm:text-xl font-semibold text-gray-800">{report.client_name}</h3>
                <p className="text-gray-600 text-sm sm:text-base">By: {report.employee_name}</p>
                <p className="text-xs sm:text-sm text-gray-500">
                  Created: {formatLATime(report.request_date)} at {report.created_time || formatLATimeOnly(report.request_date)}
                </p>
                {report.last_modified && (
                  <p className="text-xs text-gray-400">
                    Last modified: {formatLADateTime(report.last_modified)}
                  </p>
                )}
              </div>
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${getPriorityColor(report.priority)}`}>
                  {report.priority}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${getStatusColor(report.status)}`}>
                  {report.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>

            <p className="text-gray-700 mb-4 text-sm sm:text-base">{report.description}</p>

            {report.employee_notes && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-sm font-medium text-blue-800 mb-1">Employee Notes:</p>
                <p className="text-blue-700 text-sm">{report.employee_notes}</p>
              </div>
            )}

            {report.photos && report.photos.length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 mb-4">
                {report.photos.map((photo, index) => (
                  <img
                    key={index}
                    src={photo}
                    alt={`Report photo ${index + 1}`}
                    className="w-full h-20 sm:h-24 object-cover rounded-lg cursor-pointer hover:opacity-75 transition"
                    onClick={() => window.open(photo, '_blank')}
                  />
                ))}
              </div>
            )}

            {/* Edit Button */}
            {(user?.role === 'admin' || report.employee_id === user?.id) && (
              <div className="mb-4">
                <button
                  onClick={() => handleEditReport(report)}
                  className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-medium transition text-sm"
                >
                  Edit Report
                </button>
              </div>
            )}

            {/* Financial Information (Admin Only) */}
            {user?.role === 'admin' && (report.total_cost > 0 || report.parts_cost > 0) && (
              <div className="mb-4 p-3 bg-green-50 rounded-lg">
                <p className="text-sm font-medium text-green-800 mb-2">Financial Summary:</p>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-green-700">Estimate: </span>
                    <span className="font-medium">${report.total_cost?.toFixed(2) || '0.00'}</span>
                  </div>
                  <div>
                    <span className="text-green-700">Cost of Services: </span>
                    <span className="font-medium">${report.parts_cost?.toFixed(2) || '0.00'}</span>
                  </div>
                  <div>
                    <span className="text-green-700">Gross Profit: </span>
                    <span className="font-medium">${((report.total_cost || 0) - (report.parts_cost || 0)).toFixed(2)}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Modification History (for all users) */}
            {report.modification_history && report.modification_history.length > 0 && (
              <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-2">Service History:</p>
                <div className="space-y-1">
                  {report.modification_history.map((mod, index) => (
                    <p key={index} className="text-xs text-gray-600">
                      {formatLADateTime(mod.modified_at)} - Modified by {mod.modified_by} ({mod.modified_by_role}): {mod.changes.join(', ')}
                    </p>
                  ))}
                </div>
              </div>
            )}

            {/* Admin Controls */}
            {user?.role === 'admin' && (
              <div className="border-t pt-4 mt-4">
                <div className="flex flex-wrap gap-2 mb-3">
                  {['scheduled', 'in_progress', 'completed'].map(status => (
                    <button
                      key={status}
                      onClick={() => updateReportStatus(report.id, status)}
                      className={`px-3 py-2 rounded-lg font-medium transition text-xs sm:text-sm ${
                        report.status === status
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                      }`}
                    >
                      {status.replace('_', ' ').toUpperCase()}
                    </button>
                  ))}
                </div>

                {/* Financial Fields */}
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm font-medium text-blue-800 mb-3">Financial Information:</p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-blue-700 mb-1">Estimate ($)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={report.total_cost || ''}
                        onChange={(e) => {
                          const newValue = e.target.value;
                          const updatedReports = reports.map(r => 
                            r.id === report.id ? { ...r, total_cost: parseFloat(newValue) || 0 } : r
                          );
                          setReports(updatedReports);
                          
                          clearTimeout(window.financialTimeout);
                          window.financialTimeout = setTimeout(() => {
                            updateFinancialField(report.id, 'total_cost', parseFloat(newValue) || 0);
                          }, 1000);
                        }}
                        className="w-full px-2 py-1 border border-blue-300 rounded text-sm focus:ring-1 focus:ring-blue-500 outline-none"
                        placeholder="0.00"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-blue-700 mb-1">Cost of Services ($)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={report.parts_cost || ''}
                        onChange={(e) => {
                          const newValue = e.target.value;
                          const updatedReports = reports.map(r => 
                            r.id === report.id ? { ...r, parts_cost: parseFloat(newValue) || 0 } : r
                          );
                          setReports(updatedReports);
                          
                          clearTimeout(window.financialTimeout);
                          window.financialTimeout = setTimeout(() => {
                            updateFinancialField(report.id, 'parts_cost', parseFloat(newValue) || 0);
                          }, 1000);
                        }}
                        className="w-full px-2 py-1 border border-blue-300 rounded text-sm focus:ring-1 focus:ring-blue-500 outline-none"
                        placeholder="0.00"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-blue-700 mb-1">Gross Profit ($)</label>
                      <input
                        type="text"
                        value={`${((report.total_cost || 0) - (report.parts_cost || 0)).toFixed(2)}`}
                        readOnly
                        className="w-full px-2 py-1 border border-blue-300 rounded bg-blue-100 text-sm"
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Admin Notes:</label>
                  <textarea
                    value={report.admin_notes || ''}
                    onChange={(e) => {
                      // Update the local state immediately for better UX
                      const updatedReports = reports.map(r => 
                        r.id === report.id ? { ...r, admin_notes: e.target.value } : r
                      );
                      setReports(updatedReports);
                      
                      // Auto-save notes after user stops typing
                      clearTimeout(window.notesTimeout);
                      window.notesTimeout = setTimeout(() => {
                        updateAdminNotes(report.id, e.target.value);
                      }, 1000);
                    }}
                    placeholder="Admin notes..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none text-sm h-20"
                    rows="2"
                  />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {reports.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl sm:text-6xl mb-4">🏊‍♂️</div>
          <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-2">No service reports yet</h3>
          <p className="text-gray-600 text-sm sm:text-base px-4">
            {user?.role === 'employee' 
              ? 'Create your first service report to get started!'
              : 'No service reports have been created yet.'
            }
          </p>
        </div>
      )}
    </div>
  );
};

// Services Completed Component
const ServicesConcluded = () => {
  const { user } = useAuth();
  const [reports, setReports] = useState([]);
  const [clients, setClients] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchCompletedReports();
    fetchClients();
  }, []);

  const fetchCompletedReports = async () => {
    try {
      const response = await axios.get(`${API}/reports`);
      // Filter only completed reports
      const completedReports = response.data.filter(report => report.status === 'completed');
      setReports(completedReports);
    } catch (error) {
      console.error('Failed to fetch completed reports:', error);
    }
  };

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Failed to fetch clients:', error);
    }
  };

  const getStatusColor = (status) => {
    return 'bg-green-100 text-green-800'; // All concluded are completed
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'URGENT': 'bg-red-100 text-red-800',
      'SAME WEEK': 'bg-orange-100 text-orange-800',
      'NEXT WEEK': 'bg-blue-100 text-blue-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-7xl mx-auto px-2 sm:px-4 py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">Services Completed</h2>
        <div className="text-sm text-gray-600">
          Total completed: {reports.length}
        </div>
      </div>

      {/* Reports List */}
      <div className="space-y-4 sm:space-y-6">
        {reports.map(report => (
          <div key={report.id} className="bg-white rounded-xl shadow-lg p-4 sm:p-6 border-l-4 border-green-500">
            <div className="flex flex-col sm:flex-row justify-between items-start mb-4 gap-4">
              <div className="flex-1">
                <h3 className="text-lg sm:text-xl font-semibold text-gray-800">{report.client_name}</h3>
                <p className="text-gray-600 text-sm sm:text-base">By: {report.employee_name}</p>
                <p className="text-xs sm:text-sm text-gray-500">
                  Created: {formatLATime(report.request_date)} at {report.created_time || formatLATimeOnly(report.request_date)}
                </p>
                {report.completion_date && (
                  <p className="text-xs sm:text-sm text-green-600 font-medium">
                    ✅ Completed: {formatLADateTime(report.completion_date)}
                  </p>
                )}
                {report.last_modified && (
                  <p className="text-xs text-gray-400">
                    Last modified: {formatLADateTime(report.last_modified)}
                  </p>
                )}
              </div>
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${getPriorityColor(report.priority)}`}>
                  {report.priority}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${getStatusColor(report.status)}`}>
                  COMPLETED
                </span>
              </div>
            </div>

            <p className="text-gray-700 mb-4 text-sm sm:text-base">{report.description}</p>

            {report.employee_notes && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-sm font-medium text-blue-800 mb-1">Employee Notes:</p>
                <p className="text-blue-700 text-sm">{report.employee_notes}</p>
              </div>
            )}

            {report.admin_notes && (
              <div className="mb-4 p-3 bg-green-50 rounded-lg">
                <p className="text-sm font-medium text-green-800 mb-1">Admin Notes:</p>
                <p className="text-green-700 text-sm">{report.admin_notes}</p>
              </div>
            )}

            {/* Financial Information (Admin Only) */}
            {user?.role === 'admin' && (report.total_cost > 0 || report.parts_cost > 0) && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-sm font-medium text-blue-800 mb-2">Financial Summary:</p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-blue-700">Estimate: </span>
                    <span className="font-medium">${report.total_cost?.toFixed(2) || '0.00'}</span>
                  </div>
                  <div>
                    <span className="text-blue-700">Cost of Services: </span>
                    <span className="font-medium">${report.parts_cost?.toFixed(2) || '0.00'}</span>
                  </div>
                  <div>
                    <span className="text-blue-700">Gross Profit: </span>
                    <span className="font-medium">${((report.total_cost || 0) - (report.parts_cost || 0)).toFixed(2)}</span>
                  </div>
                </div>
              </div>
            )}

            {report.photos && report.photos.length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 mb-4">
                {report.photos.map((photo, index) => (
                  <img
                    key={index}
                    src={photo}
                    alt={`Report photo ${index + 1}`}
                    className="w-full h-20 sm:h-24 object-cover rounded-lg cursor-pointer hover:opacity-75 transition"
                    onClick={() => window.open(photo, '_blank')}
                  />
                ))}
              </div>
            )}

            {/* Modification History */}
            {report.modification_history && report.modification_history.length > 0 && (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-2">Service History:</p>
                <div className="space-y-1">
                  {report.modification_history.map((mod, index) => (
                    <p key={index} className="text-xs text-gray-600">
                      {formatLADateTime(mod.modified_at)} - Modified by {mod.modified_by} ({mod.modified_by_role}): {mod.changes.join(', ')}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {reports.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl sm:text-6xl mb-4">✅</div>
          <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-2">No completed services yet</h3>
          <p className="text-gray-600 text-sm sm:text-base px-4">
            Completed service reports will appear here.
          </p>
        </div>
      )}
    </div>
  );
};
const ClientsManagement = () => {
  const [clients, setClients] = useState([]);
  const [showUpload, setShowUpload] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Failed to fetch clients:', error);
    }
  };

  const handleExcelUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API}/clients/import-excel`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert(response.data.message);
      fetchClients();
      setShowUpload(false);
    } catch (error) {
      console.error('Failed to upload Excel:', error);
      alert('Failed to import Excel file. Make sure it has "Name" and "Address" columns.');
    }
    setIsUploading(false);
  };

  const deleteClient = async (clientId, clientName) => {
    if (window.confirm(`Are you sure you want to delete client "${clientName}"?`)) {
      try {
        await axios.delete(`${API}/clients/${clientId}`);
        fetchClients();
        alert('Client deleted successfully');
      } catch (error) {
        console.error('Failed to delete client:', error);
        alert('Failed to delete client');
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-2 sm:px-4 py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">Clients Management</h2>
        <button
          onClick={() => setShowUpload(true)}
          className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white px-4 sm:px-6 py-3 rounded-lg font-semibold transition"
        >
          Import Excel
        </button>
      </div>

      {/* Upload Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-50">
          <div className="bg-white rounded-xl p-4 sm:p-6 w-full max-w-md">
            <h3 className="text-lg sm:text-xl font-bold mb-4">Import Clients from Excel</h3>
            <p className="text-gray-600 mb-4 text-sm sm:text-base">
              Excel file should have columns named "Name" and "Address"
            </p>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleExcelUpload}
              className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none mb-4 text-sm sm:text-base"
              disabled={isUploading}
            />
            <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
              <button
                onClick={() => setShowUpload(false)}
                disabled={isUploading}
                className="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 py-3 rounded-lg font-semibold transition disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
            {isUploading && (
              <div className="mt-4 text-center text-blue-600 text-sm">
                Uploading and processing...
              </div>
            )}
          </div>
        </div>
      )}

      {/* Clients List */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Name</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Address</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Added</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {clients.map(client => (
                <tr key={client.id} className="hover:bg-gray-50">
                  <td className="px-3 sm:px-6 py-3 sm:py-4 font-medium text-gray-800 text-sm sm:text-base">{client.name}</td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4 text-gray-600 text-sm sm:text-base">{client.address}</td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm text-gray-500">
                    {formatLATime(client.created_at)}
                  </td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4">
                    <button
                      onClick={() => deleteClient(client.id, client.name)}
                      className="text-red-600 hover:text-red-800 font-medium text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {clients.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl sm:text-6xl mb-4">👥</div>
          <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-2">No clients yet</h3>
          <p className="text-gray-600 text-sm sm:text-base px-4">Import your client list from Excel to get started!</p>
        </div>
      )}
    </div>
  );
};

// Users Management Component
const UsersManagement = () => {
  const [users, setUsers] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    role: 'employee'
  });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await axios.post(`${API}/users`, formData);
      setShowCreateForm(false);
      setFormData({ username: '', password: '', role: 'employee' });
      fetchUsers();
    } catch (error) {
      console.error('Failed to create user:', error);
      alert('Failed to create user. Username might already exist.');
    }
    setIsLoading(false);
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await axios.delete(`${API}/users/${userId}`);
        fetchUsers();
      } catch (error) {
        console.error('Failed to delete user:', error);
        alert('Failed to delete user');
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-2 sm:px-4 py-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-800">User Management</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 sm:px-6 py-3 rounded-lg font-semibold transition"
        >
          Add User
        </button>
      </div>

      {/* Create User Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-50">
          <div className="bg-white rounded-xl p-4 sm:p-6 w-full max-w-md">
            <h3 className="text-lg sm:text-xl font-bold mb-4">Create New User</h3>
            
            <form onSubmit={handleCreateUser} className="space-y-4">
              <input
                type="text"
                placeholder="Username"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                required
              />
              
              <input
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
                required
              />
              
              <select
                value={formData.role}
                onChange={(e) => setFormData({...formData, role: e.target.value})}
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm sm:text-base"
              >
                <option value="employee">Employee</option>
                <option value="admin">Admin</option>
              </select>

              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full sm:flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
                >
                  {isLoading ? 'Creating...' : 'Create User'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 py-3 rounded-lg font-semibold transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Users List */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Username</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Role</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Created</th>
                <th className="px-3 sm:px-6 py-3 sm:py-4 text-left text-xs sm:text-sm font-semibold text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users.map(user => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-3 sm:px-6 py-3 sm:py-4 font-medium text-gray-800 text-sm sm:text-base">{user.username}</td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4">
                    <span className={`px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${
                      user.role === 'admin' 
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm text-gray-500">
                    {formatLATime(user.created_at)}
                  </td>
                  <td className="px-3 sm:px-6 py-3 sm:py-4">
                    {user.username !== 'admin' && (
                      <button
                        onClick={() => deleteUser(user.id)}
                        className="text-red-600 hover:text-red-800 font-medium text-sm"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

// Main Dashboard Component
const Dashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('reports');

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main>
        {activeTab === 'reports' && <ServiceReports />}
        {activeTab === 'completed' && <ServicesConcluded />}
        {activeTab === 'clients' && user?.role === 'admin' && <ClientsManagement />}
        {activeTab === 'users' && user?.role === 'admin' && <UsersManagement />}
      </main>
    </div>
  );
};

// Main App Component
function App() {
  const { user } = useAuth();

  return (
    <div className="App">
      {user ? <Dashboard /> : <Login />}
    </div>
  );
}

// App with Auth Provider
export default function AppWithAuth() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}