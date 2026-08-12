import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import PassportTimeline from '../components/PassportTimeline';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { QrCode, ShieldCheck, Leaf, Download, Share2, Award } from 'lucide-react';

export default function Passport({ showToast }) {
  const { id } = useParams();
  const [passport, setPassport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPassport();
  }, [id]);

  const loadPassport = async () => {
    setLoading(true);
    try {
      const data = await api.getPassport(id);
      setPassport(data);
    } catch (err) {
      showToast('Failed to load digital passport', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    showToast('Digital Passport Certificate downloaded!', 'success');
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Digital Product Passport Agent generating cryptographic lifecycle record..." />
        </main>
      </div>
    );
  }

  if (!passport) return null;

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={id} />

      <main className="flex-1 p-4 md:p-8 max-w-5xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-teal-400 text-xs font-mono mb-1">
              <QrCode className="w-4 h-4" />
              <span>DIGITAL PRODUCT PASSPORT (DPP)</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              ReUse Passport Certificate
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Tamper-evident circular lifecycle & environmental auditability pass.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleDownload}
              className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20"
            >
              <Download className="w-4 h-4" />
              <span>Download DPP</span>
            </button>
          </div>
        </div>

        {/* Passport Certificate Card */}
        <div className="glass-card rounded-3xl p-6 md:p-8 border border-emerald-500/30 bg-slate-900/90 relative overflow-hidden space-y-8">
          
          {/* Top Banner with QR Code */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-800">
            <div>
              <span className="text-xs font-mono uppercase text-emerald-400 font-bold">Verified Product Passport</span>
              <h2 className="text-2xl font-extrabold text-slate-100 mt-1">{passport.title}</h2>
              <p className="text-xs text-slate-400 font-mono mt-1">Serial No: {passport.serialNumber}</p>
              
              <div className="mt-3 inline-flex items-center gap-1.5 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800 text-[11px] text-slate-300 font-mono">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Hash: {passport.passportHash?.substring(0, 18)}...</span>
              </div>
            </div>

            {/* Simulated QR Code SVG */}
            <div className="p-4 bg-white rounded-2xl shadow-xl shrink-0 text-center">
              <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
                <rect width="100" height="100" fill="white" />
                <path d="M10 10h30v30H10zM15 15v20h20V15zM20 20h10v10H20z" fill="black" />
                <path d="M60 10h30v30H60zM65 15v20h20V15zM70 20h10v10H70z" fill="black" />
                <path d="M10 60h30v30H10zM15 65v20h20V65zM20 70h10v10H20z" fill="black" />
                <rect x="50" y="50" width="10" height="10" fill="black" />
                <rect x="70" y="50" width="20" height="10" fill="black" />
                <rect x="50" y="70" width="10" height="20" fill="black" />
                <rect x="70" y="70" width="10" height="10" fill="black" />
              </svg>
              <span className="block text-[9px] text-slate-900 font-bold font-mono mt-1">SCAN PASSPORT</span>
            </div>
          </div>

          {/* Impact Certificate Summary */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400">
                <Leaf className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs text-slate-400 block font-mono">Total CO₂ Saved</span>
                <span className="text-xl font-bold text-slate-100 font-sans">{passport.carbonSavedTotalKg} kg CO₂e</span>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-teal-500/10 text-teal-400">
                <Award className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs text-slate-400 block font-mono">Circular Economic Valuation</span>
                <span className="text-xl font-bold text-slate-100 font-sans">${passport.circularValuationUsd} USD</span>
              </div>
            </div>
          </div>

          {/* Lifecycle History */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-100">Lifecycle & Maintenance Audit Trail</h3>
            <PassportTimeline events={passport.lifecycleEvents} />
          </div>

        </div>

      </main>
    </div>
  );
}
