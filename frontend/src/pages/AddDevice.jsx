import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';
import { 
  PlusCircle, 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft, 
  Upload, 
  Smartphone, 
  ShieldAlert, 
  MapPin, 
  Sparkles 
} from 'lucide-react';

export default function AddDevice({ showToast }) {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    category: 'Laptops',
    brand: 'Apple',
    model: 'MacBook Air M2',
    serialNumber: 'C02H1234MD99',
    condition: 'Like New',
    workingStatus: 'Fully Functional',
    defects: 'None',
    processor: 'Apple M2 (8-Core)',
    ram: '16 GB',
    storage: '512 GB SSD',
    batteryHealth: '92%',
    location: '742 Evergreen Terrace, Springfield, IL',
    contactPhone: '+1 (555) 019-2834',
    images: [
      'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80'
    ]
  });

  const handleChange = (field, val) => {
    setFormData(prev => ({ ...prev, [field]: val }));
  };

  const handleNext = () => setStep(s => Math.min(s + 1, 5));
  const handlePrev = () => setStep(s => Math.max(s - 1, 1));

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const created = await api.createDevice(formData);
      showToast(`Device ${created.id} registered into AI Pipeline!`, 'success');
      navigate(`/agents/${created.id}`);
    } catch (err) {
      showToast('Failed to register device', 'error');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar />

      <main className="flex-1 p-4 md:p-8 max-w-4xl mx-auto space-y-8 overflow-y-auto">
        {/* Header */}
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
            Register Hardware Device
          </h1>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            5-Step wizard to submit item details into the autonomous AI evaluation pipeline.
          </p>
        </div>

        {/* Wizard Step Indicator */}
        <div className="grid grid-cols-5 gap-2 bg-slate-900/60 p-2 rounded-2xl border border-slate-800 backdrop-blur-md">
          {['Device', 'Condition', 'Specs & Media', 'Logistics', 'Review'].map((label, idx) => {
            const stepNum = idx + 1;
            const isDone = step > stepNum;
            const isCurrent = step === stepNum;
            return (
              <div
                key={label}
                className={`py-2 px-2 rounded-xl text-center transition-all ${
                  isCurrent
                    ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                    : isDone
                    ? 'bg-slate-800 text-emerald-400 font-semibold'
                    : 'text-slate-500 font-medium'
                }`}
              >
                <div className="text-[10px] uppercase font-mono tracking-wider">Step 0{stepNum}</div>
                <div className="text-xs truncate">{label}</div>
              </div>
            );
          })}
        </div>

        {/* Step Form Box */}
        <div className="glass-card rounded-3xl p-6 md:p-8 border border-slate-800 bg-slate-900/70 space-y-6">
          
          {/* STEP 1: DEVICE INFORMATION */}
          {step === 1 && (
            <div className="space-y-4 animate-fadeIn">
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Smartphone className="w-5 h-5 text-emerald-400" />
                Step 1: General Device Information
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => handleChange('category', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="Laptops">Laptops</option>
                    <option value="Smartphones">Smartphones</option>
                    <option value="Tablets">Tablets</option>
                    <option value="Audio">Audio & Headphones</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Brand / Manufacturer</label>
                  <input
                    type="text"
                    value={formData.brand}
                    onChange={(e) => handleChange('brand', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                    placeholder="e.g. Apple, Dell, Lenovo"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Model Name</label>
                  <input
                    type="text"
                    value={formData.model}
                    onChange={(e) => handleChange('model', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                    placeholder="e.g. MacBook Air M2"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Serial Number / IMEI</label>
                  <input
                    type="text"
                    value={formData.serialNumber}
                    onChange={(e) => handleChange('serialNumber', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
                    placeholder="C02H1234MD99"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: CONDITION ASSESSMENT */}
          {step === 2 && (
            <div className="space-y-4 animate-fadeIn">
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-emerald-400" />
                Step 2: Condition & Integrity Rating
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Cosmetic Condition</label>
                  <select
                    value={formData.condition}
                    onChange={(e) => handleChange('condition', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="New / Sealed">New / Sealed</option>
                    <option value="Like New">Like New (Mint)</option>
                    <option value="Good">Good (Minor wear)</option>
                    <option value="Fair">Fair (Noticeable scratches)</option>
                    <option value="Salvage">Salvage / Parts Only</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Functional Status</label>
                  <select
                    value={formData.workingStatus}
                    onChange={(e) => handleChange('workingStatus', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="Fully Functional">Fully Functional</option>
                    <option value="Minor Defect (Port/Speaker)">Minor Defect (Port/Speaker)</option>
                    <option value="Battery Needs Replacement">Battery Needs Replacement</option>
                    <option value="Non-Functional / Dead Motherboard">Non-Functional</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Notes on Defects or Damage</label>
                  <textarea
                    rows={3}
                    value={formData.defects}
                    onChange={(e) => handleChange('defects', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                    placeholder="Describe any screen scratches, keyboard wear, or battery notes..."
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: SPECS & MEDIA */}
          {step === 3 && (
            <div className="space-y-4 animate-fadeIn">
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Upload className="w-5 h-5 text-emerald-400" />
                Step 3: Specifications & Hardware Media
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Processor / SoC</label>
                  <input
                    type="text"
                    value={formData.processor}
                    onChange={(e) => handleChange('processor', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">RAM Capacity</label>
                  <input
                    type="text"
                    value={formData.ram}
                    onChange={(e) => handleChange('ram', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Storage Capacity</label>
                  <input
                    type="text"
                    value={formData.storage}
                    onChange={(e) => handleChange('storage', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <div className="border-2 border-dashed border-slate-800 rounded-2xl p-6 text-center bg-slate-950/50 hover:border-emerald-500/40 transition-colors">
                <Upload className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                <p className="text-sm font-semibold text-slate-200">Hardware Image Upload (Simulated)</p>
                <p className="text-xs text-slate-500 mt-1">Image URL is automatically attached for Object Agent vision testing.</p>
              </div>
            </div>
          )}

          {/* STEP 4: LOGISTICS */}
          {step === 4 && (
            <div className="space-y-4 animate-fadeIn">
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-emerald-400" />
                Step 4: Pickup & Location
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Pickup Address</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => handleChange('location', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Contact Phone</label>
                  <input
                    type="text"
                    value={formData.contactPhone}
                    onChange={(e) => handleChange('contactPhone', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 5: REVIEW */}
          {step === 5 && (
            <div className="space-y-4 animate-fadeIn">
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-emerald-400" />
                Step 5: Review & Trigger AI Pipeline
              </h3>

              <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-3 text-xs">
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Item Name:</span>
                  <span className="font-bold text-emerald-400">{formData.brand} {formData.model}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Category & Condition:</span>
                  <span className="text-slate-200">{formData.category} • {formData.condition}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/60 pb-2">
                  <span className="text-slate-400">Specs:</span>
                  <span className="text-slate-200">{formData.processor} / {formData.ram} RAM / {formData.storage}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Pickup Location:</span>
                  <span className="text-slate-200">{formData.location}</span>
                </div>
              </div>
            </div>
          )}

          {/* Wizard Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <button
              onClick={handlePrev}
              disabled={step === 1}
              className="px-4 py-2.5 rounded-xl border border-slate-800 text-xs font-semibold text-slate-300 hover:bg-slate-800 disabled:opacity-40 transition-colors flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>

            {step < 5 ? (
              <button
                onClick={handleNext}
                className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-md shadow-emerald-500/20 text-xs transition-all flex items-center gap-2"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-bold px-8 py-2.5 rounded-xl shadow-lg shadow-emerald-500/25 text-xs transition-all flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                <span>{isSubmitting ? 'Launching Agents...' : 'Submit to AI Pipeline'}</span>
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
