import type { SignalRecord } from "@/lib/api";

export function MarketContextPanel({ signal }: { signal?: SignalRecord | null }) {
  const context = signal?.context;
  const rows: [string, any][] = [
    ["Scenario", context?.scenario],
    ["Trend", `${context?.trend?.direction || "-"} (${context?.trend?.score ?? "-"})`],
    ["Momentum", `${context?.momentum?.state || "-"} (${context?.momentum?.score ?? "-"})`],
    ["Mean reversion", context?.mean_reversion?.pressure],
    ["Volatility", `${context?.volatility?.state || "-"} (${context?.volatility?.score ?? "-"})`],
    ["Chop", `${context?.chop?.state || "-"} (${context?.chop?.score ?? "-"})`],
    ["Volume", context?.volume?.state],
    ["Session", `${context?.session?.session || "-"} / ${context?.session?.liquidity || "-"}`],
    ["Spread", `${context?.quote?.spread_points ?? "-"} pts`],
    ["News", context?.news?.severity]
  ];
  return <Panel title="Market Context" rows={rows} />;
}

function Panel({ title, rows }: { title: string; rows: [string, any][] }) {
  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <h2 className="text-lg font-semibold text-ink">{title}</h2>
      <div className="mt-4 space-y-3">
        {rows.map(([label, value]) => (
          <div className="flex items-center justify-between gap-3 border-b border-line/70 pb-2 text-sm last:border-0" key={label}>
            <span className="text-slate-400">{label}</span>
            <span className="text-right font-medium text-ink">{value ?? "-"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
