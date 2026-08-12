import React from 'react';

export default function ScoreCard({ title, value, subtitle, icon: Icon, trend, color = 'emerald' }) {
  const colorMap = {
    emerald: 'from-emerald-500/10 to-teal-500/10 border-emerald-500/30 text-emerald-400',
    blue: 'from-cyan-500/10 to-blue-500/10 border-cyan-500/30 text-cyan-400',
    purple: 'from-purple-500/10 to-indigo-500/10 border-purple-500/30 text-purple-400',
    amber: 'from-amber-500/10 to-orange-500/10 border-amber-500/30 text-amber-400',
  };

  return (
    <div className={`p-5 rounded-2xl border bg-gradient-to-br ${colorMap[color] || colorMap.emerald} bg-slate-900/60 backdrop-blur-md relative overflow-hidden group`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-400 tracking-wide uppercase">{title}</span>
        {Icon && (
          <div className="p-2 rounded-xl bg-slate-950/80 border border-slate-800/80">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>
      
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-extrabold text-slate-100 font-sans tracking-tight">
          {value}
        </span>
        {trend && (
          <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
            {trend}
          </span>
        )}
      </div>
      
      {subtitle && (
        <p className="text-xs text-slate-400 mt-2 font-normal">
          {subtitle}
        </p>
      )}
    </div>
  );
}
