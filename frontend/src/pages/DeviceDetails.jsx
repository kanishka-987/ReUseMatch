import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import StatusBadge from '../components/StatusBadge';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { 
  Smartphone, 
  Cpu, 
  Sparkles, 
  CheckCircle2, 
  Truck, 
  QrCode, 
  Leaf, 
  MapPin, 
  ArrowRight,
  ShieldCheck
} from 'lucide-react';

export default function DeviceDetails({ showToast }) {
  const { id } = useParams();
  const [device, setDevice] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDevice();
  }, [id]);

  const loadDevice = async () => {
    setLoading(true);
    try {
      const data = await api.getDeviceById(id);
      setDevice(data);
    } catch (err) {
      showToast('Failed to load device details', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Loading device overview..." />
        </main>
      </div>
    );
  }

  if (!device) return null;

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={device.id} />

      <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Top Title Banner */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6 rounded-3xl border border-slate-800 bg-slate-900/60">
          <div className="flex items-start gap-4">
            <div className="w-20 h-20 rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 shrink-0">
              <img src={device.images?.[0]} alt={device.title} className="w-full h-full object-cover" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <StatusBadge status={device.status} />
                <span className="text-xs font-mono text-emerald-400 font-semibold">{device.id}</span>
              </div>
              <h1 className="text-xl md:text-2xl font-extrabold text-slate-100">{device.title}</h1>
              <p className="text-xs text-slate-400 mt-1 font-mono">SN: {device.serialNumber} • Owner: {device.owner}</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <Link
              to={`/diagnosis/${device.id}`}
              className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-md shadow-emerald-500/20 transition-all"
            >
              <Cpu className="w-4 h-4" />
              <span>AI Diagnosis</span>
            </Link>
            <Link
              to={`/agents/${device.id}`}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 transition-colors"
            >
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Agent Logs</span>
            </Link>
          </div>
        </div>

        {/* Action Quick Links Row */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {[
            { label: 'Diagnosis', path: `/diagnosis/${device.id}`, icon: Cpu, color: 'text-emerald-400' },
            { label: 'Agents', path: `/agents/${device.id}`, icon: Sparkles, color: 'text-amber-400' },
            { label: 'Matches', path: `/matches/${device.id}`, icon: CheckCircle2, color: 'text-cyan-400' },
            { label: 'Decision', path: `/recommendation/${device.id}`, icon: ShieldCheck, color: 'text-purple-400' },
            { label: 'Logistics', path: `/logistics/${device.id}`, icon: Truck, color: 'text-blue-400' },
            { label: 'Passport', path: `/passport/${device.id}`, icon: QrCode, color: 'text-teal-400' },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.label}
                to={item.path}
                className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all flex flex-col items-center justify-center text-center group"
              >
                <Icon className={`w-5 h-5 ${item.color} group-hover:scale-110 transition-transform mb-1`} />
                <span className="text-xs font-bold text-slate-200">{item.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Specifications & Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Specs Column */}
          <div className="md:col-span-2 glass-card p-6 rounded-3xl border border-slate-800 bg-slate-900/60 space-y-4">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Smartphone className="w-5 h-5 text-emerald-400" />
              Hardware Specifications
            </h3>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 block mb-1">Processor</span>
                <span className="font-semibold text-slate-200">{device.specs?.processor}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 block mb-1">RAM</span>
                <span className="font-semibold text-slate-200">{device.specs?.ram}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 block mb-1">Storage</span>
                <span className="font-semibold text-slate-200">{device.specs?.storage}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 block mb-1">Battery Condition</span>
                <span className="font-semibold text-emerald-400">{device.specs?.batteryHealth}</span>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center gap-3">
              <MapPin className="w-5 h-5 text-emerald-400 shrink-0" />
              <div>
                <span className="text-xs text-slate-400 block">Registered Location</span>
                <span className="text-xs font-semibold text-slate-200">{device.location}</span>
              </div>
            </div>
          </div>

          {/* Environmental Impact Side Card */}
          <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900 to-slate-950 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 text-emerald-400 mb-2">
                <Leaf className="w-5 h-5" />
                <h4 className="font-bold text-sm">Environmental Savings</h4>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">
                Quantified displacement metrics computed by the Condition & Logistics Agents.
              </p>

              <div className="space-y-3 font-mono text-xs">
                <div className="flex justify-between bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-400">CO₂ Avoided:</span>
                  <span className="font-bold text-emerald-400">{device.environmentalSavings?.co2Kg} kg</span>
                </div>
                <div className="flex justify-between bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-400">Water Conserved:</span>
                  <span className="font-bold text-cyan-400">{device.environmentalSavings?.waterLiters} L</span>
                </div>
                <div className="flex justify-between bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  <span className="text-slate-400">E-Waste Prevented:</span>
                  <span className="font-bold text-teal-400">{device.environmentalSavings?.eWasteKg} kg</span>
                </div>
              </div>
            </div>

            <Link
              to={`/recommendation/${device.id}`}
              className="mt-6 w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-xl text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-emerald-500/20"
            >
              <span>View Match Recommendation</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

      </main>
    </div>
  );
}
