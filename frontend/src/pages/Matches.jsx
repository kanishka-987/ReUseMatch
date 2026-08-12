import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import MatchCard from '../components/MatchCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { CheckCircle2, ArrowRight, Building2, Sparkles } from 'lucide-react';

export default function Matches({ showToast }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMatches();
  }, [id]);

  const loadMatches = async () => {
    setLoading(true);
    try {
      const data = await api.getMatches(id);
      setMatches(data);
      if (data.length > 0) setSelectedMatch(data[0]);
    } catch (err) {
      showToast('Failed to load recipient matches', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleProceed = () => {
    if (!selectedMatch) return;
    showToast(`Match ${selectedMatch.recipientName} selected!`, 'info');
    navigate(`/recommendation/${id}`);
  };

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-65px)]">
        <Sidebar deviceId={id} />
        <main className="flex-1 flex items-center justify-center">
          <LoadingSpinner label="Need Matching Agent scanning verified recipient database..." />
        </main>
      </div>
    );
  }

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={id} />

      <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-cyan-400 text-xs font-mono mb-1">
              <Building2 className="w-4 h-4" />
              <span>RECIPIENT & REFURBISHER MATCH ENGINE</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              Verified Candidate Recipients
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Need Agent evaluated 48 organizations to find the highest-impact placement.
            </p>
          </div>

          <button
            onClick={handleProceed}
            className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-6 py-2.5 rounded-xl text-xs flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20 self-start md:self-auto"
          >
            <span>Review Final Recommendation</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Match Cards List */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {matches.map((m) => (
            <MatchCard
              key={m.id}
              match={m}
              isSelected={selectedMatch?.id === m.id}
              onSelect={(mat) => setSelectedMatch(mat)}
            />
          ))}
        </div>

        {/* Selected Match Summary Banner */}
        {selectedMatch && (
          <div className="glass-card rounded-3xl p-6 border border-emerald-500/30 bg-emerald-950/20 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-mono uppercase text-emerald-400 font-bold">Currently Selected Match</span>
                <h3 className="text-lg font-bold text-slate-100">{selectedMatch.recipientName}</h3>
                <p className="text-xs text-slate-300 mt-0.5">{selectedMatch.estimatedImpact}</p>
              </div>
            </div>

            <button
              onClick={handleProceed}
              className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-6 py-3 rounded-xl text-xs flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20 shrink-0"
            >
              <span>Confirm & View Recommendation</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        )}

      </main>
    </div>
  );
}
