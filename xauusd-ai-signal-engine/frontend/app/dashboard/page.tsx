"use client";

import { useEffect, useState } from "react";
import { RefreshCcw } from "lucide-react";
import { DecisionLog } from "@/components/DecisionLog";
import { CommentLearningPanel } from "@/components/CommentLearningPanel";
import { MarketContextPanel } from "@/components/MarketContextPanel";
import { OrderPanel } from "@/components/OrderPanel";
import { RiskPanel } from "@/components/RiskPanel";
import { SignalCard } from "@/components/SignalCard";
import { getSignalHistory, runSignalOnce, type SignalRecord } from "@/lib/api";

export default function DashboardPage() {
  const [history, setHistory] = useState<SignalRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const latest = history[0];

  async function refresh() {
    setHistory(await getSignalHistory());
  }

  async function runOnce(scenario?: string) {
    setLoading(true);
    try {
      const signal = await runSignalOnce(scenario);
      setHistory((items) => [signal, ...items].slice(0, 25));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh().catch(() => setHistory([]));
  }, []);

  return (
    <main className="min-h-screen bg-[#080b10] px-4 py-5 text-ink sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="flex flex-col gap-4 border-b border-line pb-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-wide text-gold">XAUUSD AI Signal Engine</p>
            <h1 className="mt-1 text-2xl font-semibold">Paper Trading Command Center</h1>
          </div>
          <div className="flex flex-wrap gap-2">
            {["normal", "trending", "choppy", "news_spike"].map((scenario) => (
              <button key={scenario} onClick={() => runOnce(scenario)} disabled={loading} className="rounded-md border border-line px-3 py-2 text-sm text-slate-200 hover:border-gold disabled:opacity-50">
                {scenario.replace("_", " ")}
              </button>
            ))}
            <button onClick={() => runOnce()} disabled={loading} className="inline-flex items-center gap-2 rounded-md bg-gold px-4 py-2 text-sm font-semibold text-black disabled:opacity-60">
              <RefreshCcw className="h-4 w-4" /> Run once
            </button>
          </div>
        </header>
        <div className="mt-6 grid gap-5 lg:grid-cols-[1.5fr_1fr]">
          <div className="space-y-5">
            <SignalCard signal={latest} />
            <MarketContextPanel signal={latest} />
            <DecisionLog history={history} />
          </div>
          <div className="space-y-5">
            <OrderPanel signal={latest} />
            <RiskPanel signal={latest} />
            <CommentLearningPanel />
          </div>
        </div>
      </div>
    </main>
  );
}
