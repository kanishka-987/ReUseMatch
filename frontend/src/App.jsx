import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Toast from './components/Toast';
import ProtectedRoute from './components/ProtectedRoute';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AddDevice from './pages/AddDevice';
import DeviceDetails from './pages/DeviceDetails';
import Diagnosis from './pages/Diagnosis';
import AgentActivity from './pages/AgentActivity';
import Matches from './pages/Matches';
import Recommendation from './pages/Recommendation';
import Logistics from './pages/Logistics';
import Passport from './pages/Passport';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem('loggedIn') === 'true';
  });

  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4000);
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-white">
        <Navbar 
          isLoggedIn={isLoggedIn} 
          setIsLoggedIn={setIsLoggedIn} 
          showToast={showToast} 
        />

        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Home showToast={showToast} />} />
            <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} showToast={showToast} />} />
            <Route path="/register" element={<Register setIsLoggedIn={setIsLoggedIn} showToast={showToast} />} />

            <Route path="/dashboard" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Dashboard showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/devices/new" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <AddDevice showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/devices/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <DeviceDetails showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/diagnosis/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Diagnosis showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/agents/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <AgentActivity showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/matches/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Matches showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/recommendation/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Recommendation showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/logistics/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Logistics showToast={showToast} />
              </ProtectedRoute>
            } />

            <Route path="/passport/:id" element={
              <ProtectedRoute isLoggedIn={isLoggedIn}>
                <Passport showToast={showToast} />
              </ProtectedRoute>
            } />
          </Routes>
        </div>

        <Toast toast={toast} onClose={() => setToast(null)} />
      </div>
    </BrowserRouter>
  );
}
