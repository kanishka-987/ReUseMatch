import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { ShieldCheck, CheckCircle2, Leaf, DollarSign, Heart, ArrowRight, Sparkles } from 'lucide-react';

export default function Recommendation({ showToast }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isApproving, setIsApproving] = useState(false);

  useEffect(() => {
    loadRecommendation();
  }, [id]);

  const loadRecommendation = async () => {
    setLoading(true);
    try {
      const data = await api.getRecommendation(id);
      setRecommendation(data);
    } catch (err) {
      showToast('Failed to load recommendation', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    setIsApproving(true);
    try {
      await api.approveRecommendation(id, recommendation.primaryMatch.id);
      setIsModalOpen(false);
      showToast('Match recommendation officially approved!', 'success');
      navigate(`/logistics/${id}`);
    } catch (err) {
      showToast('Failed to approve recommendation', 'error');
    } finally {
      setIsApproving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Orchestrator Agent synthesizing optimal match recommendation..." />
        </main>
      </div>
    );
  }

  if (!recommendation) return null;

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={id} />

      <main className="flex-1 p-4 md:p-8 max-w-5xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Header */}
        <div>
          <div className="flex items-center gap-2 text-purple-400 text-xs font-mono mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>AI ORCHESTRATOR DECISION ENGINE</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
            Final Reuse Recommendation
          </h1>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Synthesized recommendation balancing carbon reduction, social impact, and transit feasibility.
          </p>
        </div>

        {/* Main Recommendation Card */}
        <div className="glass-card rounded-3xl p-6 md:p-8 border border-slate-800 bg-slate-900/80 space-y-6">
          
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
              <span className="text-xs font-mono uppercase text-emerald-400 font-bold">Top Recommended Match</span>
              <h2 className="text-2xl font-extrabold text-slate-100 mt-1">
                {recommendation.primaryMatch.recipientName}
              </h2>
              <span className="text-xs text-slate-400">{recommendation.primaryMatch.type}</span>
            </div>

            <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-4 py-2 rounded-2xl text-sm font-bold font-mono">
              <Sparkles className="w-4 h-4" />
              <span>{recommendation.primaryMatch.matchScore}% Match Score</span>
            </div>
          </div>

          {/* Reasoning */}
          <div>
            <h4 className="text-xs font-mono text-slate-400 uppercase font-semibold mb-2">Orchestrator Reasoning</h4>
            <p className="text-sm text-slate-200 bg-slate-950 p-4 rounded-2xl border border-slate-800/80 leading-relaxed">
              {recommendation.reasoning}
            </p>
          </div>

          {/* Impact Matrix */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 text-emerald-400 mb-1">
                <Leaf className="w-4 h-4" />
                <span className="font-bold">CO₂ Avoided</span>
              </div>
              <span className="text-lg font-bold text-slate-100">{recommendation.circularImpact.co2AvoidedKg} kg</span>
            </div>

            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 text-cyan-400 mb-1">
                <Heart className="w-4 h-4" />
                <span className="font-bold">Social Benefit</span>
              </div>
              <span className="text-lg font-bold text-slate-100">{recommendation.circularImpact.socialBenefitIndex}</span>
            </div>

            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 text-teal-400 mb-1">
                <DollarSign className="w-4 h-4" />
                <span className="font-bold">Fair Residual Value</span>
              </div>
              <span className="text-lg font-bold text-slate-100">{recommendation.circularImpact.economicValuationUsd}</span>
            </div>
          </div>

          {/* Action Trigger */}
          <div className="pt-4 border-t border-slate-800 flex justify-end">
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-bold px-8 py-3 rounded-xl shadow-lg shadow-emerald-500/20 text-sm transition-all flex items-center gap-2"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Approve Match & Dispatch Courier</span>
            </button>
          </div>
        </div>

        {/* Approval Modal */}
        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Confirm Match & Dispatch"
          footer={
            <>
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleApprove}
                disabled={isApproving}
                className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-5 py-2 rounded-xl text-xs flex items-center gap-1.5"
              >
                <span>{isApproving ? 'Dispatched...' : 'Confirm Approval'}</span>
              </button>
            </>
          }
        >
          <div className="space-y-3">
            <p>
              By approving this match, you authorize the <strong>Logistics Agent</strong> to dispatch 
              an eco-courier for pickup from your specified address.
            </p>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs text-slate-300">
              <div><strong>Recipient:</strong> {recommendation.primaryMatch.recipientName}</div>
              <div><strong>Transport Mode:</strong> Zero-Emission Cargo Courier</div>
            </div>
          </div>
        </Modal>

      </main>
    </div>
  );
}
