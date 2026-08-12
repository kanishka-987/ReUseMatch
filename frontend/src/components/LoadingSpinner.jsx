import React from 'react';
import { Loader2, Bot } from 'lucide-react';

export default function LoadingSpinner({ label = "Simulating Autonomous AI Agent Pipeline..." }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 space-y-4">
      <div className="relative">
        <div className="w-16 h-16 rounded-full border-4 border-slate-800 border-t-emerald-500 animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center text-emerald-400">
          <Bot className="w-6 h-6 animate-pulse" />
        </div>
      </div>
      <p className="text-sm font-medium text-slate-300 font-mono tracking-wide">
        {label}
      </p>
    </div>
  );
}
