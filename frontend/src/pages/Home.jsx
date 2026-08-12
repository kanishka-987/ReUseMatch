import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Recycle, 
  Sparkles, 
  Bot, 
  ShieldCheck, 
  ArrowRight, 
  Leaf, 
  Building2, 
  Truck, 
  QrCode, 
  CheckCircle2, 
  Play
} from 'lucide-react';

export default function Home({ showToast }) {
  const [simStep, setSimStep] = useState(0);
  const [isSimulating, setIsSimulating] = useState(false);

  const demoSteps = [
    { title: 'Item Submitted', agent: 'User Interface', detail: 'Donor submits MacBook Pro 16" (2021 M1 Pro)' },
    { title: 'Object Classification', agent: 'Object Agent', detail: 'Identified laptop model, hardware specs, release MSRP' },
    { title: 'Condition Assessment', agent: 'Condition Agent', detail: 'Battery health 91%, minor surface scratch. Usability score: 94%' },
    { title: 'Recipient Matching', agent: 'Need Agent', detail: 'Matched with Springfield STEM Academy (High Need, 4.2km)' },
    { title: 'Logistics Optimization', agent: 'Logistics Agent', detail: 'Eco-cargo bike route generated. CO2 saved: 285kg' },
    { title: 'Match Approved!', agent: 'Orchestrator Agent', detail: 'Digital Product Passport generated. Delivery dispatched.' }
  ];

  const handleStartSim = () => {
    if (isSimulating) return;
    setIsSimulating(true);
    setSimStep(0);

    let current = 0;
    const interval = setInterval(() => {
      current += 1;
      if (current < demoSteps.length) {
        setSimStep(current);
      } else {
        clearInterval(interval);
        setIsSimulating(false);
        showToast('AI Simulation completed successfully!', 'success');
      }
    }, 1200);
  };

  return (
    <div className="space-y-24 pb-20">
      
      {/* HERO SECTION */}
      <section className="relative pt-12 lg:pt-20 px-4 max-w-7xl mx-auto text-center">
        {/* Glow backdrop */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Multi-Agent Circular Economy Platform</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold text-slate-100 tracking-tight max-w-4xl mx-auto leading-tight">
          Autonomous AI Agents Driving <br className="hidden md:inline" />
          <span className="text-gradient">Zero-Waste Reuse & Recycling</span>
        </h1>

        <p className="mt-6 text-lg text-slate-400 max-w-2xl mx-auto">
          ReUseMatch orchestrates specialized autonomous AI agents to evaluate, match, and route unused electronic devices directly to schools, charities, and eco-refurbishers.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/register"
            className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-bold px-8 py-4 rounded-xl shadow-lg shadow-emerald-500/25 transition-all hover:scale-105 flex items-center gap-2"
          >
            <span>Start Matching Devices</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          
          <Link
            to="/dashboard"
            className="bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 font-semibold px-8 py-4 rounded-xl transition-all"
          >
            Explore Dashboard
          </Link>
        </div>

        {/* Real-time stats row */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          {[
            { label: 'Devices Saved', val: '1,428+' },
            { label: 'E-Waste Diverted', val: '3,840 kg' },
            { label: 'CO₂ Prevented', val: '41.2 Tons' },
            { label: 'Recipients Served', val: '156 Orgs' },
          ].map((st, i) => (
            <div key={i} className="glass-card p-4 rounded-2xl border border-slate-800">
              <div className="text-2xl font-bold text-emerald-400 font-sans">{st.val}</div>
              <div className="text-xs text-slate-400 mt-1">{st.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* AI DEMO SIMULATION SANDBOX */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="glass-card rounded-3xl p-6 md:p-10 border border-slate-800 bg-slate-900/80 relative overflow-hidden">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
              <span className="text-xs font-mono uppercase text-emerald-400 font-semibold tracking-wider">
                Live Interactive Prototype
              </span>
              <h2 className="text-2xl md:text-3xl font-bold text-slate-100 mt-1">
                Simulate Multi-Agent Pipeline
              </h2>
            </div>

            <button
              onClick={handleStartSim}
              disabled={isSimulating}
              className="bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 font-bold px-6 py-3 rounded-xl flex items-center gap-2 shadow-md shadow-emerald-500/20 transition-all self-start md:self-auto"
            >
              <Play className={`w-4 h-4 ${isSimulating ? 'animate-spin' : ''}`} />
              <span>{isSimulating ? 'Processing Pipeline...' : 'Run Live Demo'}</span>
            </button>
          </div>

          {/* Stepper Progress */}
          <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
            {demoSteps.map((step, idx) => {
              const isDone = simStep > idx;
              const isCurrent = simStep === idx;
              return (
                <div 
                  key={idx} 
                  className={`p-3.5 rounded-xl border text-left transition-all ${
                    isCurrent
                      ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 ring-2 ring-emerald-500/40'
                      : isDone
                      ? 'bg-slate-900 border-emerald-500/40 text-emerald-400'
                      : 'bg-slate-950/40 border-slate-800 text-slate-500'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-mono mb-1">
                    <span>Step 0{idx+1}</span>
                    {isDone && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <div className="text-xs font-bold truncate">{step.title}</div>
                  <div className="text-[10px] opacity-75 mt-0.5 truncate">{step.agent}</div>
                </div>
              );
            })}
          </div>

          {/* Active Detail Display */}
          <div className="mt-6 bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 flex items-start gap-3">
            <Bot className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <span className="text-emerald-400 font-bold">[{demoSteps[simStep].agent}]:</span>{' '}
              <span>{demoSteps[simStep].detail}</span>
            </div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-3xl font-extrabold text-slate-100">How ReUseMatch Works</h2>
          <p className="text-slate-400 text-sm mt-2">
            Sequential multi-agent intelligence ensuring maximum environmental and social impact.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { step: '01', title: 'Device Entry', desc: 'Donor registers unused laptop, phone, or tablet with basic specs & images.', icon: Recycle },
            { step: '02', title: 'AI Diagnosis', desc: 'Object & Condition agents assess hardware health and circular value.', icon: Bot },
            { step: '03', title: 'Recipient Match', desc: 'Need agent scores verified schools and non-profits in real time.', icon: Building2 },
            { step: '04', title: 'Eco Logistics', desc: 'Logistics agent schedules carbon-neutral courier and Digital Passport.', icon: Truck }
          ].map((card, i) => {
            const Icon = card.icon;
            return (
              <div key={i} className="glass-card p-6 rounded-2xl border border-slate-800 relative group">
                <span className="text-3xl font-extrabold font-mono text-slate-700 group-hover:text-emerald-500/40 transition-colors">
                  {card.step}
                </span>
                <div className="my-4 p-3 rounded-xl bg-emerald-500/10 text-emerald-400 w-fit">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-100">{card.title}</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{card.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* AI AGENTS SECTION */}
      <section id="agents-section" className="max-w-7xl mx-auto px-4">
        <div className="glass-card rounded-3xl p-8 border border-slate-800 bg-gradient-to-b from-slate-900 to-slate-950">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <span className="text-xs font-mono uppercase text-emerald-400 font-semibold tracking-wider">
              Autonomous Intelligence
            </span>
            <h2 className="text-3xl font-bold text-slate-100 mt-1">Our Autonomous Agent Team</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { name: 'Object Identification Agent', desc: 'Uses computer vision and taxonomy heuristics to identify exact model, specifications, and hardware generation.' },
              { name: 'Condition Assessment Agent', desc: 'Computes battery wear index, display integrity score, repair feasibility, and circular usability percentage.' },
              { name: 'Need Matching Agent', desc: 'Evaluates recipient databases, digital divide urgency scores, and organizational verification.' },
              { name: 'Logistics Agent', desc: 'Optimizes shipping routes, selects eco-couriers, and computes total CO₂ emission savings.' },
              { name: 'Orchestrator Agent', desc: 'Aggregates multi-agent trade-offs to present optimal decision recommendations for donor approval.' },
              { name: 'Digital Passport Agent', desc: 'Issues tamper-evident Digital Product Passports with full lifecycle auditability.' }
            ].map((ag, i) => (
              <div key={i} className="p-5 rounded-2xl bg-slate-950 border border-slate-800/80 hover:border-emerald-500/30 transition-all">
                <div className="flex items-center gap-3 mb-3">
                  <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                    <Bot className="w-5 h-5" />
                  </div>
                  <h4 className="font-bold text-sm text-slate-200">{ag.name}</h4>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{ag.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

    </div>
  );
}
