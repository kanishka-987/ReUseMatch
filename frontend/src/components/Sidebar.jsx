import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  PlusCircle, 
  Smartphone, 
  Cpu, 
  CheckCircle2, 
  Truck, 
  QrCode,
  Sparkles
} from 'lucide-react';

export default function Sidebar({ deviceId = "DEV-1092" }) {
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Add New Device', path: '/devices/new', icon: PlusCircle },
    { label: 'Device Overview', path: `/devices/${deviceId}`, icon: Smartphone },
    { label: 'AI Diagnosis', path: `/diagnosis/${deviceId}`, icon: Cpu },
    { label: 'Agent Pipeline', path: `/agents/${deviceId}`, icon: Sparkles },
    { label: 'Matches', path: `/matches/${deviceId}`, icon: CheckCircle2 },
    { label: 'Recommendation', path: `/recommendation/${deviceId}`, icon: CheckCircle2 },
    { label: 'Logistics', path: `/logistics/${deviceId}`, icon: Truck },
    { label: 'Digital Passport', path: `/passport/${deviceId}`, icon: QrCode },
  ];

  return (
    <aside className="w-64 bg-slate-900/60 backdrop-blur-md border-r border-slate-800 shrink-0 hidden md:block min-h-[calc(100vh-65px)] p-4">
      <div className="space-y-6">
        <div>
          <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Platform Navigation
          </h3>
          <div className="mt-3 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shadow-sm shadow-emerald-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-500'}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Quick Info Box */}
        <div className="bg-slate-950/80 rounded-xl p-3 border border-slate-800/80 text-xs">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span>Selected Device</span>
            <span className="text-emerald-400 font-mono font-semibold">{deviceId}</span>
          </div>
          <p className="text-slate-500 truncate">MacBook Pro 16" (2021 M1)</p>
        </div>
      </div>
    </aside>
  );
}
