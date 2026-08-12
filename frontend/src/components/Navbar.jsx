import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Recycle, Bell, PlusCircle, LogOut, User, Sparkles, LayoutDashboard } from 'lucide-react';

export default function Navbar({ isLoggedIn, setIsLoggedIn, showToast }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('loggedIn');
    setIsLoggedIn(false);
    showToast('Logged out successfully', 'info');
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 p-0.5 shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Recycle className="w-5 h-5 text-emerald-400 animate-pulse-slow" />
            </div>
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-slate-100 to-emerald-400 bg-clip-text text-transparent">
              ReUse<span className="text-emerald-400">Match</span>
            </span>
            <span className="block text-[10px] text-emerald-500 font-mono tracking-wider uppercase">
              Circular Economy AI
            </span>
          </div>
        </Link>

        {/* Center Nav Links (For Landing & General) */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
          <Link 
            to="/" 
            className={`hover:text-emerald-400 transition-colors ${location.pathname === '/' ? 'text-emerald-400 font-semibold' : ''}`}
          >
            Home
          </Link>
          {isLoggedIn && (
            <Link 
              to="/dashboard" 
              className={`hover:text-emerald-400 transition-colors flex items-center gap-1.5 ${location.pathname.startsWith('/dashboard') ? 'text-emerald-400 font-semibold' : ''}`}
            >
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </Link>
          )}
          <a href="#how-it-works" className="hover:text-emerald-400 transition-colors">How it Works</a>
          <a href="#agents-section" className="hover:text-emerald-400 transition-colors">AI Agents</a>
        </nav>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          {isLoggedIn ? (
            <>
              <button 
                onClick={() => showToast('No new notifications', 'info')}
                className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors relative"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-emerald-500" />
              </button>

              <Link
                to="/devices/new"
                className="hidden sm:flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-semibold text-sm px-4 py-2 rounded-lg shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 transition-all hover:-translate-y-0.5"
              >
                <PlusCircle className="w-4 h-4" />
                <span>Register Device</span>
              </Link>

              <div className="flex items-center gap-2 border-l border-slate-800 pl-3 ml-1">
                <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold text-xs">
                  US
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-400 hover:text-red-400 rounded-lg hover:bg-slate-800 transition-colors"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="text-slate-300 hover:text-white text-sm font-medium px-3 py-2 rounded-lg hover:bg-slate-800 transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold text-sm px-4 py-2 rounded-lg shadow-md shadow-emerald-500/20 transition-all"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
