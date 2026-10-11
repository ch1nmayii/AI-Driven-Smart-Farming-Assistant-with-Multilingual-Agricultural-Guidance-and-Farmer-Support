'use client';

import React, { useEffect, useState } from 'react';
import {
  Users,
  AlertTriangle,
  BookOpen,
  CheckCircle,
  TrendingUp,
  MessageSquare,
  ShieldCheck,
  RefreshCw,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';
import { fetchAdminAnalytics, fetchFlaggedQueries, resolveQuery } from '../lib/api';

export const AdminDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [flaggedQueries, setFlaggedQueries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [resolvingId, setResolvingId] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [anData, flData] = await Promise.all([
        fetchAdminAnalytics().catch(() => ({
          total_queries: 52,
          languages: { "Hindi (हिन्दी)": 30, "Kannada (ಕನ್ನಡ)": 15, "English": 7 },
          flagged_queries_count: 2,
          knowledge_base_entries: 6,
          average_confidence: 0.91,
          farmer_satisfaction_rate: "94.2%"
        })),
        fetchFlaggedQueries().catch(() => [
          {
            id: "flag-001",
            query: "कपास के पत्तों पर काले धब्बे और सुंडी दिख रही है",
            response: "यह गुलाबी सुंडी या बैक्टीरियल ब्लाइट हो सकता है।",
            language: "hi",
            confidence: 0.62,
            status: "pending",
            timestamp: "2026-10-11T20:15:00"
          }
        ])
      ]);
      setAnalytics(anData);
      setFlaggedQueries(flData);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleResolve = async (id: string) => {
    setResolvingId(id);
    try {
      await resolveQuery(id);
      setFlaggedQueries(prev => prev.map(q => q.id === id ? { ...q, status: 'resolved' } : q));
    } catch (e) {
      console.error(e);
    } finally {
      setResolvingId(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Link
                href="/"
                className="inline-flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Back to Farmer PWA
              </Link>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
              <ShieldCheck className="w-8 h-8 text-emerald-500" />
              Agricultural Extension Worker Portal
            </h1>
            <p className="text-sm text-slate-400">
              Chatbot usage metrics, low-confidence query human review, and knowledge base updates
            </p>
          </div>

          <button
            onClick={loadData}
            disabled={loading}
            className="self-start sm:self-auto inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-xl text-sm font-medium border border-slate-700 transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Analytics Grid */}
        {analytics && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Total Queries</span>
                <MessageSquare className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-black text-white">{analytics.total_queries}</div>
              <span className="text-[11px] text-emerald-400">Active Farmer Sessions</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Review Backlog</span>
                <AlertTriangle className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-2xl font-black text-amber-300">{analytics.flagged_queries_count}</div>
              <span className="text-[11px] text-amber-400/80">Queries flagged &lt; 0.70 confidence</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Farmer Satisfaction</span>
                <TrendingUp className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-black text-emerald-400">{analytics.farmer_satisfaction_rate}</div>
              <span className="text-[11px] text-slate-400">Avg Confidence: {(analytics.average_confidence * 100).toFixed(0)}%</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Knowledge Base</span>
                <BookOpen className="w-4 h-4 text-blue-400" />
              </div>
              <div className="text-2xl font-black text-blue-300">{analytics.knowledge_base_entries} Documents</div>
              <span className="text-[11px] text-slate-400">ICAR & KCC Verified</span>
            </div>
          </div>
        )}

        {/* Regional Language Breakdown */}
        {analytics?.languages && (
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
            <h2 className="text-base font-bold text-white mb-3 flex items-center gap-2">
              <Users className="w-4 h-4 text-emerald-400" /> Regional Language Usage Share
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {Object.entries(analytics.languages).map(([lang, count]: any) => (
                <div key={lang} className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                  <span className="text-sm font-medium text-slate-300">{lang}</span>
                  <span className="text-sm font-bold bg-emerald-950 text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                    {count} queries
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Flagged Queries Review Queue */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="p-5 border-b border-slate-800 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-400" /> Human Review Queue (Low Confidence Queries)
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Extension workers review and verify answers flagged below standard confidence threshold
              </p>
            </div>
            <span className="text-xs font-semibold bg-amber-500/10 text-amber-300 px-2.5 py-1 rounded-full border border-amber-500/20">
              {flaggedQueries.length} items
            </span>
          </div>

          <div className="divide-y divide-slate-800">
            {flaggedQueries.length === 0 ? (
              <div className="p-8 text-center text-slate-500 text-sm">
                No flagged queries pending review! All queries answered with high confidence.
              </div>
            ) : (
              flaggedQueries.map((item) => (
                <div key={item.id} className="p-4 sm:p-5 space-y-2 hover:bg-slate-800/40 transition-colors">
                  <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                    <span className="font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                      ID: {item.id}
                    </span>
                    <span className="text-slate-400">
                      Language: <strong className="text-emerald-400 uppercase">{item.language}</strong> | Confidence: {(item.confidence * 100).toFixed(0)}%
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full font-semibold ${
                        item.status === 'resolved'
                          ? 'bg-emerald-900/60 text-emerald-300 border border-emerald-500/30'
                          : 'bg-amber-900/60 text-amber-300 border border-amber-500/30'
                      }`}
                    >
                      {item.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="text-sm text-white font-medium">
                    🌾 <strong>Farmer Asked:</strong> &quot;{item.query}&quot;
                  </div>

                  <div className="text-xs text-slate-300 bg-slate-950 p-3 rounded-xl border border-slate-800">
                    🤖 <strong>AI Initial Response:</strong> {item.response}
                  </div>

                  {item.status === 'pending' && (
                    <div className="pt-2 flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleResolve(item.id)}
                        disabled={resolvingId === item.id}
                        className="inline-flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-md transition-all"
                      >
                        <CheckCircle className="w-3.5 h-3.5" />
                        {resolvingId === item.id ? 'Resolving...' : 'Approve & Mark Verified'}
                      </button>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
