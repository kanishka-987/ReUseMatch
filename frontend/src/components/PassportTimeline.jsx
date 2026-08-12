import React from 'react';
import { CheckCircle2, Clock, MapPin, Tag, Wrench } from 'lucide-react';

export default function PassportTimeline({ events }) {
  const getIcon = (type) => {
    switch (type) {
      case 'Origin': return Tag;
      case 'Maintenance': return Wrench;
      case 'Platform Entry': return MapPin;
      default: return CheckCircle2;
    }
  };

  return (
    <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
      {events?.map((evt, idx) => {
        const Icon = getIcon(evt.type);
        const isLatest = idx === events.length - 1;
        return (
          <div key={idx} className="relative flex items-start gap-4 group">
            <div className={`absolute -left-6 top-1 w-5 h-5 rounded-full flex items-center justify-center text-xs border ${
              isLatest 
                ? 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-md shadow-emerald-500/30'
                : 'bg-slate-900 text-slate-400 border-slate-700'
            }`}>
              <Icon className="w-3 h-3" />
            </div>
            
            <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800/80 w-full hover:border-slate-700 transition-colors">
              <div className="flex items-center justify-between text-xs text-slate-400 mb-1 font-mono">
                <span>{evt.date}</span>
                <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[10px]">{evt.type}</span>
              </div>
              <p className="text-sm font-semibold text-slate-200">{evt.event}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
