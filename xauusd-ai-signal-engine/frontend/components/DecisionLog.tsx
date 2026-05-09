import type { SignalRecord } from "@/lib/api";

export function DecisionLog({ history }: { history: SignalRecord[] }) {
  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <h2 className="text-lg font-semibold text-ink">Decision History</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full min-w-[620px] text-left text-sm">
          <thead className="text-xs uppercase text-slate-500">
            <tr>
              <th className="pb-3">Time</th>
              <th className="pb-3">Decision</th>
              <th className="pb-3">Scenario</th>
              <th className="pb-3">Filters</th>
              <th className="pb-3">Validation</th>
              <th className="pb-3">R:R</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr className="border-t border-line" key={item.id}>
                <td className="py-3 text-slate-400">{new Date(item.created_at).toLocaleTimeString()}</td>
                <td className="py-3 font-medium text-ink">{item.llm_decision.decision}</td>
                <td className="py-3 text-slate-300">{item.context.scenario}</td>
                <td className="py-3 text-slate-300">{item.risk_filters.status}</td>
                <td className="py-3 text-slate-300">{item.validation.status}</td>
                <td className="py-3 text-slate-300">{item.position?.rr_ratio || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {history.length === 0 ? <p className="py-8 text-sm text-slate-400">No decisions logged yet.</p> : null}
      </div>
    </section>
  );
}
