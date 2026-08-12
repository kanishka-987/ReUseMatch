import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import PipelineViewer from '../components/PipelineViewer';
import ScoreCard from '../components/ScoreCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import {
  Play,
  Sparkles,
  Smartphone,
  Leaf,
  ShieldCheck,
  RotateCcw,
  PlusCircle,
  Search,
  Bot
} from 'lucide-react';

export default function Dashboard({ showToast }) {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  // Submission & Pipeline state
  const [description, setDescription] = useState("A three-year-old Dell laptop. It turns on but has visible scratches.");
  const [location, setLocation] = useState("123 Hope Lane, Springfield, IL");
  const [isProcessing, setIsProcessing] = useState(false);
  const [pipelineData, setPipelineData] = useState(null);

  useEffect(() => {
    loadData();
    // Run initial demo pipeline automatically
    handleRunPipeline("A three-year-old Dell laptop. It turns on but has visible scratches.", "123 Hope Lane, Springfield, IL");
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await api.getDevices();
      setDevices(data);
    } catch (err) {
      showToast('Failed to load devices', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRunPipeline = async (descToRun = description, locToRun = location) => {
    setIsProcessing(true);
    try {
      const result = await api.runPipeline(descToRun, locToRun);
      setPipelineData(result);
      showToast('5-Agent Pipeline executed successfully!', 'success');
    } catch (err) {
      showToast('Failed to execute pipeline', 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  const setPresetScenario = (desc, loc = "123 Hope Lane, Springfield, IL") => {
    setDescription(desc);
    setLocation(loc);
    handleRunPipeline(desc, loc);
  };

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={devices[0]?.id || "DEV-1092"} />

      <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto space-y-8 overflow-y-auto">

        {/* Top Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              5-Agent Pipeline Dashboard
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Real-time execution telemetry for Evidence, Diagnosis, Decision, Need, and Logistics Agents.
            </p>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <ScoreCard
            title="Pipeline Status"
            value={pipelineData ? pipelineData.status.toUpperCase() : "ACTIVE"}
            subtitle="5/5 Agents Orchestrated"
            icon={Bot}
            color="emerald"
          />
          <ScoreCard
            title="Evidence Source"
            value={pipelineData?.evidence?.source === 'llm' ? "LLM (Gemini)" : "mock_fallback"}
            subtitle="Model execution state"
            icon={Sparkles}
            color="blue"
          />
          <ScoreCard
            title="Lifecycle Decision"
            value={pipelineData?.decision?.best_lifecycle_action || "REUSE"}
            subtitle="Action classification"
            icon={ShieldCheck}
            color="purple"
          />
          <ScoreCard
            title="Recipient Matches"
            value={pipelineData?.need?.matching_organizations_count || 0}
            subtitle="Matched organizations"
            icon={Leaf}
            color="amber"
          />
        </div>

        {/* INTERACTIVE ITEM SUBMISSION & PRESET SCENARIOS */}
        <div className="glass-card rounded-3xl p-6 md:p-8 border border-slate-800 bg-slate-900/80 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs font-mono uppercase text-emerald-400 font-bold tracking-wider">
                Pipeline Execution Control
              </span>
              <h2 className="text-xl font-bold text-slate-100 mt-0.5">Submit Item to Autonomous Pipeline</h2>
            </div>

            {/* Scenario Buttons */}
            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => setPresetScenario("A three-year-old Dell laptop. It turns on but has visible scratches.")}
                className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-mono transition-colors"
              >
                Test 1: Dell Laptop (REUSE)
              </button>
              <button
                onClick={() => setPresetScenario("Broken motherboard destroyed beyond repair recycle")}
                className="px-3 py-1.5 rounded-xl bg-rose-950/40 hover:bg-rose-900/40 text-xs text-rose-300 border border-rose-800 font-mono transition-colors"
              >
                Test 2: RECYCLE Scenario
              </button>
              <button
                onClick={() => setPresetScenario("Obsolete unknown unmatchable device")}
                className="px-3 py-1.5 rounded-xl bg-amber-950/40 hover:bg-amber-900/40 text-xs text-amber-300 border border-amber-800 font-mono transition-colors"
              >
                Test 3: No Matches
              </button>
            </div>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); handleRunPipeline(); }} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-xs font-semibold text-slate-300 mb-1">Item Description</label>
                <textarea
                  rows={2}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                  placeholder="Describe item condition, wear, or functional state..."
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Donor Location</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                  placeholder="e.g. 123 Hope Lane"
                />
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="w-full mt-3 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-bold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md shadow-emerald-500/20 transition-all disabled:opacity-50"
                >
                  <Play className={`w-4 h-4 ${isProcessing ? 'animate-spin' : ''}`} />
                  <span>{isProcessing ? 'Running Pipeline...' : 'Run 5-Agent Pipeline'}</span>
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* 5-AGENT PIPELINE RESULTS DISPLAY */}
        {isProcessing ? (
          <LoadingSpinner label="Sequencing Evidence -> Diagnosis -> Decision -> Need -> Logistics Agents..." />
        ) : (
          <PipelineViewer pipelineData={pipelineData} />
        )}

      </main>
    </div>
  );
}
