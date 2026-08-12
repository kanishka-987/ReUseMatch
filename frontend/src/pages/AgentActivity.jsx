import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import AgentCard from '../components/AgentCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { Sparkles, Terminal, ArrowRight, Bot, CheckCircle2 } from 'lucide-react';

export default function AgentActivity({ showToast }) {
  const { id } = useParams();
  const [logsData, setLogsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgentLogs();
  }, [id]);

  const loadAgentLogs = async () => {
    setLoading(true);
    try {
      const data = await api.getAgentLogs(id);
      setLogsData(data);
    } catch (err) {
      showToast('Failed to load agent execution logs', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Fetching agent pipeline execution logs..." />
        </main>
      </div>
    );
  }

  if (!logsData) return null;

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={id} />

      <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-amber-400 text-xs font-mono mb-1">
              <Bot className="w-4 h-4" />
              <span>AUTONOMOUS AGENT ORCHESTRATION</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              Agent Execution & Pipeline Breakdown
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Live status and telemetry for Object, Condition, Need, Logistics, and Orchestrator agents.
            </p>
          </div>

          <Link
            to={`/matches/${id}`}
            className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20 self-start md:self-auto"
          >
            <span>Proceed to Matches</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Agent Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.values(logsData.agents).map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>

        {/* Console Execution Logs */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-950">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
            <div className="flex items-center gap-2 text-slate-300 font-mono text-xs font-bold">
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span>AGENT_PIPELINE_TELEMETRY.log</span>
            </div>
            <span className="text-[10px] text-emerald-400 font-mono bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
              5/5 Steps Executed
            </span>
          </div>

          <div className="space-y-3 font-mono text-xs text-slate-300 max-h-80 overflow-y-auto pr-2">
            {logsData.executionSteps.map((step, idx) => (
              <div key={idx} className="flex items-start gap-3 p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <span className="text-slate-500 shrink-0">{step.time}</span>
                <span className="text-emerald-400 font-bold shrink-0">[{step.agent}]</span>
                <span className="text-slate-300 flex-1">{step.log}</span>
                <span className="text-xs text-teal-400 font-bold shrink-0 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  {step.status}
                </span>
              </div>
            ))}
          </div>
        </div>

      </main>
    </div>
  );
}
