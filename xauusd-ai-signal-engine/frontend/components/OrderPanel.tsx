"use client";

import { useEffect, useMemo, useState } from "react";
import { CircleDollarSign } from "lucide-react";
import type { SignalRecord } from "@/lib/api";

export function OrderPanel({ signal }: { signal?: SignalRecord | null }) {
  const suggested = signal?.position?.suggested_lot_size || 0;
  const [lotSize, setLotSize] = useState(String(suggested));
  const decision = signal?.llm_decision;
  const position = signal?.position;
  const disabled = !signal || signal.validation.status !== "ACCEPTED" || decision.decision === "NO_TRADE";

  useEffect(() => {
    setLotSize(String(suggested));
  }, [suggested]);
  const adjusted = useMemo(() => {
    const lot = Number(lotSize) || 0;
    const base = Number(suggested) || 1;
    const ratio = base > 0 ? lot / base : 0;
    return {
      risk: ((position?.dollar_risk || 0) * ratio).toFixed(2),
      reward: ((position?.reward_estimate || 0) * ratio).toFixed(2)
    };
  }, [lotSize, position, suggested]);

  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-ink">Order Panel</h2>
        <span className="rounded bg-gold px-2 py-1 text-xs font-bold text-black">PAPER ONLY</span>
      </div>
      <div className="mt-4 grid gap-3 text-sm">
        <button disabled={disabled} className="rounded-md bg-emerald-500 px-4 py-3 font-semibold text-black disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400">
          BUY Market
        </button>
        <button disabled={disabled} className="rounded-md bg-rose-500 px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400">
          SELL Market
        </button>
        <label className="grid gap-1">
          <span className="text-slate-400">Editable lot size</span>
          <input value={lotSize} onChange={(event) => setLotSize(event.target.value)} className="rounded-md border border-line bg-[#0c1118] px-3 py-2 text-ink outline-none focus:border-gold" />
        </label>
      </div>
      <div className="mt-4 grid gap-2 text-sm">
        <Row label="Entry" value={decision?.entry_price} />
        <Row label="Stop loss" value={decision?.stop_loss} />
        <Row label="Take profit" value={decision?.take_profit} />
        <Row label="Risk amount" value={`$${adjusted.risk}`} />
        <Row label="Reward amount" value={`$${adjusted.reward}`} />
        <Row label="R:R" value={position?.rr_ratio || "-"} />
      </div>
      <p className="mt-4 flex items-center gap-2 text-xs text-slate-500">
        <CircleDollarSign className="h-4 w-4" /> Buttons are assisted paper controls only. No broker execution exists in V1.
      </p>
    </section>
  );
}

function Row({ label, value }: { label: string; value: any }) {
  return (
    <div className="flex justify-between gap-3 border-b border-line/70 pb-2 last:border-0">
      <span className="text-slate-400">{label}</span>
      <span className="font-medium text-ink">{value ?? "-"}</span>
    </div>
  );
}
