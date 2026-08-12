import React from 'react';
import { 
  Bot, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Cpu, 
  ShieldCheck, 
  Building2, 
  Truck, 
  ArrowRight, 
  Tag, 
  Search, 
  AlertTriangle,
  RotateCcw
} from 'lucide-react';

export default function PipelineViewer({ pipelineData }) {
  if (!pipelineData) return null;

  const {
    evidence = {},
    diagnosis = {},
    decision = {},
    need = {},
    logistics = [],
    final_recommendation = {},
    status = "completed"
  } = pipelineData;

  const actionColors = {
    REUSE: 'bg-emerald-500 text-slate-950 border-emerald-400',
    REPAIR: 'bg-amber-500 text-slate-950 border-amber-400',
    DONATE: 'bg-cyan-500 text-slate-950 border-cyan-400',
    RESELL: 'bg-purple-500 text-slate-950 border-purple-400',
    RECYCLE: 'bg-rose-500 text-slate-950 border-rose-400',
  };

  const getSourceBadge = (source) => {
    if (source === 'llm') {
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-mono font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
          <Sparkles className="w-3 h-3 text-emerald-400" />
          Source: LLM (Gemini)
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-mono font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30">
        <RotateCcw className="w-3 h-3 text-amber-400" />
        Source: mock_fallback
      </span>
    );
  };

  const getStatusBadge = (agentStatus) => {
    if (agentStatus === 'Success') {
      return (
        <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
          <CheckCircle2 className="w-3.5 h-3.5" />
          Success
        </span>
      );
    } else if (agentStatus === 'Skipped') {
      return (
        <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          <AlertCircle className="w-3.5 h-3.5" />
          Skipped
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/30">
          <AlertCircle className="w-3.5 h-3.5" />
          Failed
        </span>
      );
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      
      {/* PIPELINE VISUAL FLOW DIAGRAM */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/80">
        <h3 className="text-xs font-mono uppercase text-emerald-400 font-bold tracking-wider mb-4">
          Autonomous Agent Pipeline Execution Sequence
        </h3>
        
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-slate-300 bg-slate-950 p-4 rounded-2xl border border-slate-800">
          <div className="flex items-center gap-1.5 font-bold text-slate-100">
            <Tag className="w-4 h-4 text-emerald-400" />
            <span>Submission</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-emerald-400">
            <Search className="w-4 h-4" />
            <span>Evidence</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-teal-400">
            <Cpu className="w-4 h-4" />
            <span>Diagnosis</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-purple-400">
            <ShieldCheck className="w-4 h-4" />
            <span>Decision</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-cyan-400">
            <Building2 className="w-4 h-4" />
            <span>Need Match</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-blue-400">
            <Truck className="w-4 h-4" />
            <span>Logistics</span>
          </div>
          <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden sm:inline" />

          <div className="flex items-center gap-1.5 font-bold text-amber-400">
            <Sparkles className="w-4 h-4" />
            <span>Final Result</span>
          </div>
        </div>
      </div>

      {/* 1. EVIDENCE AGENT */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
              <Search className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-100 text-base">1. Evidence Agent</h4>
              <span className="text-xs text-slate-400">Gemini-powered visual & textual feature extractor</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {getSourceBadge(evidence.source)}
            {getStatusBadge(evidence.status)}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-2">
            <span className="text-slate-400 font-mono block">Identified Item Details:</span>
            <div className="text-slate-200 font-bold text-sm">
              {evidence.item_details?.identified_name || "N/A"}
            </div>
            <div className="flex items-center gap-2 text-slate-400">
              <span>Category: <strong className="text-emerald-400">{evidence.item_details?.category}</strong></span>
            </div>
            <div className="flex flex-wrap gap-1 mt-2">
              {evidence.item_details?.detected_attributes?.map((attr, idx) => (
                <span key={idx} className="bg-slate-900 border border-slate-700 px-2 py-0.5 rounded text-[10px] text-slate-300">
                  {attr}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-2">
            <div className="flex justify-between items-center text-slate-400 font-mono">
              <span>Confidence Score:</span>
              <span className="text-emerald-400 font-bold">{((evidence.confidence || 0.85) * 100).toFixed(0)}%</span>
            </div>

            <div>
              <span className="text-slate-400 font-mono block mb-1">Observed Evidence:</span>
              <ul className="list-disc list-inside text-slate-300 space-y-0.5">
                {evidence.observed_evidence?.map((item, idx) => <li key={idx}>{item}</li>)}
              </ul>
            </div>

            <div>
              <span className="text-slate-400 font-mono block mb-1">Functional Claims:</span>
              <p className="text-slate-300">{evidence.functional_claims?.join(", ")}</p>
            </div>
          </div>
        </div>
      </div>

      {/* 2. DIAGNOSIS AGENT */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-100 text-base">2. Diagnosis Agent</h4>
              <span className="text-xs text-slate-400">Integrity, wear, and structural quality assessment</span>
            </div>
          </div>

          {getStatusBadge(diagnosis.status)}
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
          <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Condition Score</span>
            <span className="text-xl font-bold text-emerald-400">{diagnosis.condition_score} / 10</span>
          </div>
          <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Condition Grade</span>
            <span className="text-xl font-bold text-teal-400">{diagnosis.condition_grade}</span>
          </div>
          <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Repairability</span>
            <span className="text-xl font-bold text-cyan-400">{diagnosis.repairability}</span>
          </div>
          <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Reuse Potential</span>
            <span className="text-xl font-bold text-purple-400">{diagnosis.reuse_potential}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-2">
            <span className="text-slate-400 font-mono block">Likely Repairs Required:</span>
            <ul className="list-disc list-inside text-slate-300 space-y-1">
              {diagnosis.likely_repairs?.map((rep, idx) => <li key={idx}>{rep}</li>)}
            </ul>
          </div>

          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-2">
            <span className="text-slate-400 font-mono block">Risks & Faults:</span>
            <ul className="list-disc list-inside text-amber-300 space-y-1">
              {diagnosis.risks?.map((risk, idx) => <li key={idx}>{risk}</li>)}
            </ul>
            <p className="text-slate-400 pt-2 border-t border-slate-800/60 font-mono">
              Notes: {diagnosis.condition_notes}
            </p>
          </div>
        </div>
      </div>

      {/* 3. DECISION AGENT */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-100 text-base">3. Decision Agent</h4>
              <span className="text-xs text-slate-400">Optimal lifecycle action classification</span>
            </div>
          </div>

          {getStatusBadge(decision.status)}
        </div>

        <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-mono uppercase text-slate-400 block mb-1">Selected Lifecycle Action</span>
            <span className={`inline-block text-lg font-extrabold px-4 py-1.5 rounded-xl border shadow-md font-mono ${actionColors[decision.best_lifecycle_action] || actionColors.REUSE}`}>
              {decision.best_lifecycle_action || "REUSE"}
            </span>
          </div>

          <div className="md:max-w-xl text-xs space-y-1">
            <span className="text-slate-400 font-mono block">Reasoning:</span>
            <p className="text-slate-200 leading-relaxed">{decision.reasoning}</p>
            <div className="text-slate-400 font-mono pt-1">
              Alternatives Considered: <span className="text-slate-300">{decision.alternatives?.join(", ")}</span>
            </div>
          </div>
        </div>
      </div>

      {/* 4. NEED AGENT */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-100 text-base">4. Need Agent</h4>
              <span className="text-xs text-slate-400">Deterministic recipient demand matching</span>
            </div>
          </div>

          {getStatusBadge(need.status)}
        </div>

        {need.status === 'Skipped' ? (
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs text-slate-400 font-mono flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <span>{need.skip_reason || "Recipient matching was bypassed because the lifecycle decision is RECYCLE."}</span>
          </div>
        ) : need.matching_organizations_count === 0 || !need.matches || need.matches.length === 0 ? (
          <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800 text-center text-xs text-slate-400 font-mono">
            <AlertTriangle className="w-6 h-6 text-amber-400 mx-auto mb-2" />
            <p className="font-bold text-slate-200 text-sm">No matching recipient found.</p>
            <p className="mt-1 text-slate-400">No organizations currently request this category with matching minimum condition constraints.</p>
          </div>
        ) : (
          <div className="space-y-3">
            <span className="text-xs font-mono text-slate-400">
              Matched Organizations ({need.matching_organizations_count}):
            </span>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {need.matches.map((m, idx) => (
                <div key={idx} className="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs space-y-2">
                  <div className="flex justify-between items-start">
                    <h5 className="font-bold text-slate-100">{m.organization_name}</h5>
                    <span className="bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded font-mono text-[10px] border border-emerald-500/30">
                      {m.priority} Priority
                    </span>
                  </div>
                  <p className="text-slate-400 font-mono text-[11px]">ID: {m.organization_id}</p>
                  <p className="text-slate-300">{m.reason}</p>
                  <div className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/60 font-mono">
                    Match Score: <strong className="text-emerald-400">{m.match_score}%</strong>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 5. LOGISTICS AGENT */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400">
              <Truck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-bold text-slate-100 text-base">5. Logistics Agent</h4>
              <span className="text-xs text-slate-400">Deterministic transit pathing & cost estimation</span>
            </div>
          </div>

          {getStatusBadge(logistics.length > 0 ? 'Success' : 'Skipped')}
        </div>

        {logistics.length === 0 ? (
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs text-slate-400 font-mono flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400" />
            <span>
              {decision.best_lifecycle_action === 'RECYCLE'
                ? "Logistics calculation was bypassed because the lifecycle decision is RECYCLE."
                : "Logistics skipped because no matching recipient was found."}
            </span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {logistics.map((route, idx) => (
              <div key={idx} className="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs space-y-2 font-mono">
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Origin:</span>
                  <span className="text-slate-200">{route.origin}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Destination:</span>
                  <span className="text-slate-200">{route.destination}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Distance & Cost:</span>
                  <span className="text-emerald-400 font-bold">{route.distance_km} km (${route.estimated_cost_usd} USD)</span>
                </div>
                <div className="flex justify-between pt-1">
                  <span className="text-slate-400">Transport Mode:</span>
                  <span className="text-cyan-400 font-bold">{route.recommended_mode}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* FINAL RECOMMENDATION RESULT */}
      <div className="glass-card rounded-3xl p-6 md:p-8 border border-emerald-500/40 bg-gradient-to-br from-slate-900 via-slate-950 to-emerald-950/20 space-y-4 shadow-xl">
        <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs font-bold uppercase">
          <Sparkles className="w-4 h-4" />
          <span>Final Orchestration Result</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Item & Category</span>
            <span className="text-sm font-bold text-slate-100">{final_recommendation.item_name}</span>
            <span className="text-slate-400 block text-[11px]">{final_recommendation.category} • Grade: {final_recommendation.condition}</span>
          </div>

          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Recommended Action</span>
            <span className="text-base font-extrabold text-emerald-400">{final_recommendation.recommended_lifecycle_action}</span>
          </div>

          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <span className="text-slate-400 block mb-1">Recipients & Logistics</span>
            <span className="text-xs font-bold text-slate-200">{final_recommendation.recipient_organizations?.join(", ")}</span>
            <span className="text-slate-400 block text-[11px] mt-1">{final_recommendation.estimated_logistics}</span>
          </div>
        </div>
      </div>

    </div>
  );
}
