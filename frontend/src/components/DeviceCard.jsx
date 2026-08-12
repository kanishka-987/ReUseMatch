import React from 'react';
import { Link } from 'react-router-dom';
import StatusBadge from './StatusBadge';
import { ArrowRight, Leaf, ShieldAlert } from 'lucide-react';

export default function DeviceCard({ device }) {
  return (
    <div className="glass-card glass-card-hover rounded-2xl overflow-hidden p-5 flex flex-col justify-between border border-slate-800 bg-slate-900/60 relative group">
      
      {/* Background glow accent */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-emerald-500/10 transition-colors" />

      <div>
        {/* Header with image & status */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="w-16 h-16 rounded-xl overflow-hidden bg-slate-950 border border-slate-800 shrink-0">
            <img 
              src={device.images?.[0] || "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80"} 
              alt={device.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          </div>
          <StatusBadge status={device.status} />
        </div>

        {/* Device Information */}
        <div className="mb-4">
          <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-400 font-medium">
            {device.category} • {device.brand}
          </span>
          <h4 className="text-base font-bold text-slate-100 group-hover:text-emerald-400 transition-colors line-clamp-1">
            {device.title}
          </h4>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            SN: {device.serialNumber}
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-3 gap-2 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/80 mb-4 text-center">
          <div>
            <div className="text-[10px] text-slate-500 font-medium">Usability</div>
            <div className="text-sm font-bold text-emerald-400">{device.usabilityScore}%</div>
          </div>
          <div>
            <div className="text-[10px] text-slate-500 font-medium">Repairability</div>
            <div className="text-sm font-bold text-teal-400">{device.repairabilityScore}%</div>
          </div>
          <div>
            <div className="text-[10px] text-slate-500 font-medium">CO₂ Saved</div>
            <div className="text-sm font-bold text-cyan-400 flex items-center justify-center gap-0.5">
              <Leaf className="w-3 h-3 text-cyan-400 inline" />
              {device.environmentalSavings?.co2Kg || 0}kg
            </div>
          </div>
        </div>
      </div>

      {/* Footer Link */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60">
        <span className="text-xs text-slate-500 font-mono">ID: {device.id}</span>
        <Link
          to={`/devices/${device.id}`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition-colors"
        >
          <span>View Details</span>
          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
        </Link>
      </div>
    </div>
  );
}
