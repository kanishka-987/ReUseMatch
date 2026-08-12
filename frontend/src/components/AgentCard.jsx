import React from 'react';
import { Bot, CheckCircle2, Clock, Cpu, Sparkles } from 'lucide-react';

export default function AgentCard({ agent }) {
  const isCompleted = agent.status === 'Completed';

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60 relative overflow-hidden">
      
      {/* Top accent bar */}
      <div className={`absolute top-0 left-0 right-0 h-1 ${isCompleted ? 'bg-gradient-to-r from-emerald-500 to-teal-400' : 'bg-slate-700'}`} />

      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-100">{agent.name}</h4>
            <span className="text-[11px] text-slate-400 font-mono">{agent.version} • {agent.type}</span>
          </div>
        </div>

        <span className={`inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full font-medium ${
          isCompleted 
            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
            : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
        }`}>
          {isCompleted ? <CheckCircle2 className="w-3 h-3" /> : <Clock className="w-3 h-3 animate-spin" />}
          {agent.status}
        </span>
      </div>

      <p className="text-xs text-slate-300 mb-3 line-clamp-2 bg-slate-950/40 p-2.5 rounded-xl border border-slate-800/60">
        {agent.details}
      </p>

      <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/60 font-mono">
        <span>Confidence: <strong className="text-emerald-400">{(agent.confidence * 100).toFixed(0)}%</strong></span>
        <span>Latency: <strong className="text-slate-300">{agent.lastExecutionMs}ms</strong></span>
      </div>
    </div>
  );
}
