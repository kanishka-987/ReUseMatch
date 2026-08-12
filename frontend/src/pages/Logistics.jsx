import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import PassportTimeline from '../components/PassportTimeline';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { Truck, MapPin, Leaf, QrCode, ArrowRight, ShieldCheck } from 'lucide-react';

export default function Logistics({ showToast }) {
  const { id } = useParams();
  const [logistics, setLogistics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogistics();
  }, [id]);

  const loadLogistics = async () => {
    setLoading(true);
    try {
      const data = await api.getLogistics(id);
      setLogistics(data);
    } catch (err) {
      showToast('Failed to load logistics route', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Logistics Agent computing zero-emission courier route..." />
        </main>
      </div>
    );
  }

  if (!logistics) return null;

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={id} />

      <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-cyan-400 text-xs font-mono mb-1">
              <Truck className="w-4 h-4" />
              <span>LOGISTICS OPTIMIZATION ENGINE</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              Transit Route & Delivery Status
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Zero-emission courier tracking managed by Logistics Agent.
            </p>
          </div>

          <Link
            to={`/passport/${id}`}
            className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20 self-start md:self-auto"
          >
            <QrCode className="w-4 h-4" />
            <span>View Digital Passport</span>
          </Link>
        </div>

        {/* Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Timeline Column */}
          <div className="md:col-span-2 glass-card p-6 rounded-3xl border border-slate-800 bg-slate-900/60 space-y-6">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Truck className="w-5 h-5 text-emerald-400" />
              Delivery Status Timeline
            </h3>

            <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
              {logistics.timeline?.map((step, idx) => (
                <div key={idx} className="relative flex items-start gap-4">
                  <div className={`absolute -left-6 top-1 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold border ${
                    step.status === 'Completed'
                      ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                      : step.status === 'Active'
                      ? 'bg-cyan-500 text-slate-950 border-cyan-400 animate-pulse'
                      : 'bg-slate-900 text-slate-500 border-slate-700'
                  }`}>
                    {idx + 1}
                  </div>
                  
                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 w-full">
                    <div className="flex items-center justify-between text-xs text-slate-400 mb-1 font-mono">
                      <span>{step.date}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        step.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-400' :
                        step.status === 'Active' ? 'bg-cyan-500/10 text-cyan-400' : 'bg-slate-800 text-slate-400'
                      }`}>{step.status}</span>
                    </div>
                    <h4 className="text-sm font-bold text-slate-200">{step.step}</h4>
                    <p className="text-xs text-slate-400 mt-1">{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Map Placeholder & Carrier Info */}
          <div className="space-y-6">
            
            {/* Courier Info Card */}
            <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-slate-900/60 space-y-3 text-xs">
              <h4 className="font-bold text-slate-100 text-sm">Carrier Telemetry</h4>
              <div className="flex justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400">Courier:</span>
                <span className="font-bold text-emerald-400">{logistics.carrier}</span>
              </div>
              <div className="flex justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400">Mode:</span>
                <span className="font-bold text-cyan-400">{logistics.mode}</span>
              </div>
            </div>

            {/* Map Placeholder */}
            <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-slate-950 text-center space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center mx-auto">
                <MapPin className="w-6 h-6 animate-bounce" />
              </div>
              <h4 className="text-sm font-bold text-slate-100">Live GPS Route Simulation</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Pickup: {logistics.origin} <br />
                Destination: {logistics.destination}
              </p>
              <div className="bg-slate-900 p-2 rounded-xl border border-slate-800 text-[10px] font-mono text-emerald-400">
                GPS: 41.8781° N, 87.6298° W (En Route)
              </div>
            </div>

          </div>

        </div>

      </main>
    </div>
  );
}
