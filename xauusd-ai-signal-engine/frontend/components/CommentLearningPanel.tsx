"use client";

import { useState } from "react";
import { postComment } from "@/lib/api";

export function CommentLearningPanel() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (!text.trim()) return;
    setLoading(true);
    try {
      setResult(await postComment(text));
      setText("");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-lg border border-line bg-panel p-5">
      <h2 className="text-lg font-semibold text-ink">Comment Learning</h2>
      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        className="mt-4 min-h-28 w-full rounded-md border border-line bg-[#0c1118] p-3 text-sm text-ink outline-none focus:border-gold"
        placeholder="Paste an experienced trader comment for review-only classification."
      />
      <button onClick={submit} disabled={loading} className="mt-3 rounded-md bg-gold px-4 py-2 text-sm font-semibold text-black disabled:opacity-60">
        {loading ? "Saving..." : "Classify Comment"}
      </button>
      {result ? (
        <div className="mt-4 rounded-md border border-line bg-black/20 p-3 text-sm">
          <p className="font-medium text-ink">{result.classification}</p>
          <p className="mt-1 text-slate-400">{result.categories.join(", ")}</p>
          <p className="mt-1 text-xs text-slate-500">{result.suggestion}</p>
        </div>
      ) : null}
    </section>
  );
}
