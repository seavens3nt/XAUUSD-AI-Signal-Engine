export type SignalRecord = {
  id: number;
  created_at: string;
  context: any;
  risk_filters: any;
  llm_decision: any;
  validation: any;
  position: any | null;
  alert?: any;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {})
    },
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

export function getLatestSignal() {
  return request<SignalRecord | Record<string, never>>("/api/signals/latest");
}

export function getSignalHistory() {
  return request<SignalRecord[]>("/api/signals/history");
}

export function runSignalOnce(scenario?: string) {
  const query = scenario ? `?scenario=${encodeURIComponent(scenario)}` : "";
  return request<SignalRecord>(`/api/signals/run-once${query}`, { method: "POST" });
}

export function postComment(text: string) {
  return request<any>("/api/comments", { method: "POST", body: JSON.stringify({ text }) });
}
