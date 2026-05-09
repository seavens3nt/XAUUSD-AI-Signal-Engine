import { Activity, ShieldCheck } from "lucide-react";
import type { SignalRecord } from "@/lib/api";

export function SignalCard({ signal }: { signal?: SignalRecord | null }) {
  const decision = signal?.llm_decision?.decision || "NO_TRADE";
  const accepted = signal?.validation?.status === "ACCEPTED";
  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-400">Latest paper signal</p>
          <h1 className="mt-2 text-3xl font-semibold text-ink">{decision}</h1>
        </div>
        <Activity className="h-8 w-8 text-gold" />
      </div>
      <div className="mt-5 grid gap-3 text-sm sm:grid-cols-3">
        <Metric label="Confidence" value={signal ? `${Math.round(signal.llm_decision.confidence * 100)}%` : "-"} />
        <Metric label="Validation" value={signal?.validation?.status || "WAITING"} />
        <Metric label="Mode" value="PAPER / ASSISTED" />
      </div>
      <div className="mt-4 flex items-start gap-2 rounded-md border border-line bg-black/20 p-3 text-sm text-slate-300">
        <ShieldCheck className={accepted ? "mt-0.5 h-4 w-4 text-emerald-400" : "mt-0.5 h-4 w-4 text-amber-300"} />
        <p>{signal?.llm_decision?.thesis || "Run the mock engine once to create the first decision."}</p>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-[#0c1118] p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-base font-medium text-ink">{value}</p>
    </div>
  );
}
