import React from 'react';

export default function StatusBadge({ status }) {
  const styles = {
    Draft: 'bg-slate-800 text-slate-300 border-slate-700',
    Evaluating: 'bg-amber-500/10 text-amber-400 border-amber-500/30 animate-pulse-slow',
    Diagnosed: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    Matched: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    Approved: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    'In Transit': 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    Completed: 'bg-teal-500/10 text-teal-400 border-teal-500/30',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${styles[status] || styles.Draft}`}>
      {status}
    </span>
  );
}
