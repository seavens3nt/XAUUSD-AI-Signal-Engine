import { Ban, CheckCircle2 } from "lucide-react";
import type { SignalRecord } from "@/lib/api";

export function RiskPanel({ signal }: { signal?: SignalRecord | null }) {
  const filters = signal?.risk_filters;
  const checks = filters?.checks ? Object.entries(filters.checks) : [];
  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-ink">Risk Filters</h2>
        <span className={filters?.status === "BLOCK" ? "text-sm font-semibold text-rose-300" : "text-sm font-semibold text-emerald-300"}>
          {filters?.status || "WAITING"}
        </span>
      </div>
      <div className="mt-4 grid gap-2">
        {checks.length === 0 ? <p className="text-sm text-slate-400">No filter run yet.</p> : null}
        {checks.map(([name, value]: any) => (
          <div className="flex gap-2 rounded-md border border-line bg-[#0c1118] p-3" key={name}>
            {value.status === "BLOCK" ? <Ban className="mt-0.5 h-4 w-4 text-rose-300" /> : <CheckCircle2 className="mt-0.5 h-4 w-4 text-emerald-300" />}
            <div>
              <p className="text-sm font-medium text-ink">{name.replaceAll("_", " ")}</p>
              <p className="text-xs text-slate-400">{value.reason}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
