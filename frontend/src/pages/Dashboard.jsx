import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import ScoreCard from '../components/ScoreCard';
import DeviceCard from '../components/DeviceCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { api } from '../services/api';
import { PlusCircle, Search, Filter, Smartphone, Leaf, ShieldCheck, Sparkles } from 'lucide-react';

export default function Dashboard({ showToast }) {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    loadData();
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

  const categories = ['All', 'Laptops', 'Smartphones', 'Tablets', 'Audio'];

  const filteredDevices = devices.filter(d => {
    const matchesCategory = selectedCategory === 'All' || d.category === selectedCategory;
    const matchesSearch = d.title.toLowerCase().includes(search.toLowerCase()) || 
                          d.brand.toLowerCase().includes(search.toLowerCase()) ||
                          d.id.toLowerCase().includes(search.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="flex min-h-[calc(100vh-65px)]">
      <Sidebar deviceId={devices[0]?.id || "DEV-1092"} />

      <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto space-y-8 overflow-y-auto">
        
        {/* Top Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
              Platform Dashboard
            </h1>
            <p className="text-xs md:text-sm text-slate-400 mt-1">
              Overview of registered hardware devices and autonomous AI matching pipeline.
            </p>
          </div>

          <Link
            to="/devices/new"
            className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-slate-950 font-bold px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 self-start md:self-auto text-sm"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Register New Device</span>
          </Link>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <ScoreCard 
            title="Total Registered" 
            value={devices.length} 
            subtitle="Hardware devices in system"
            icon={Smartphone}
            trend="+12% this week"
            color="emerald"
          />
          <ScoreCard 
            title="Active Matches" 
            value="84" 
            subtitle="Verified recipients paired"
            icon={Sparkles}
            color="blue"
          />
          <ScoreCard 
            title="CO₂ Avoided" 
            value="760 kg" 
            subtitle="Total carbon displacement"
            icon={Leaf}
            trend="High Eco Impact"
            color="purple"
          />
          <ScoreCard 
            title="Platform Health" 
            value="99.4%" 
            subtitle="Agent accuracy rating"
            icon={ShieldCheck}
            color="amber"
          />
        </div>

        {/* Search & Filter Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
          {/* Search Input */}
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search title, brand, or ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
            />
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-1 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  selectedCategory === cat
                    ? 'bg-emerald-500 text-slate-950 shadow-sm shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Devices Grid */}
        {loading ? (
          <LoadingSpinner label="Fetching registered devices..." />
        ) : filteredDevices.length === 0 ? (
          <div className="glass-card rounded-2xl p-12 text-center border border-slate-800">
            <p className="text-slate-400 text-sm">No devices found matching your search criteria.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredDevices.map((device) => (
              <DeviceCard key={device.id} device={device} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
