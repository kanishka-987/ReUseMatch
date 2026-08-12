import React from 'react';
import { Building2, MapPin, Sparkles, Award, ArrowRight } from 'lucide-react';

export default function MatchCard({ match, onSelect, isSelected }) {
  return (
    <div className={`rounded-2xl p-5 border transition-all ${
      isSelected 
        ? 'bg-emerald-950/20 border-emerald-500/60 shadow-lg shadow-emerald-500/10'
        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
    }`}>
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-emerald-400">
            <Building2 className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-base font-bold text-slate-100">{match.recipientName}</h4>
            <span className="text-xs text-slate-400 font-medium">{match.type}</span>
          </div>
        </div>

        <div className="text-right">
          <div className="inline-flex items-center gap-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1 rounded-full text-xs font-bold font-mono">
            <Sparkles className="w-3 h-3" />
            {match.matchScore}% Match
          </div>
        </div>
      </div>

      <p className="text-xs text-slate-300 bg-slate-950/60 p-3 rounded-xl border border-slate-800/60 mb-4">
        {match.estimatedImpact}
      </p>

      <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 mb-4 font-mono">
        <div className="flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-slate-500" />
          <span>Distance: <strong className="text-slate-200">{match.distanceKm} km</strong></span>
        </div>
        <div className="flex items-center gap-1.5">
          <Award className="w-3.5 h-3.5 text-slate-500" />
          <span>Urgency: <strong className="text-slate-200">{match.urgentNeed}</strong></span>
        </div>
      </div>

      <button
        onClick={() => onSelect(match)}
        className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all ${
          isSelected
            ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
            : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
        }`}
      >
        <span>{isSelected ? 'Selected Match' : 'Choose This Match'}</span>
        <ArrowRight className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}
