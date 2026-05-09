export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-[#080b10] px-6 py-8 text-ink">
      <div className="mx-auto max-w-3xl rounded-lg border border-line bg-panel p-6">
        <p className="text-xs uppercase tracking-wide text-gold">Settings</p>
        <h1 className="mt-2 text-2xl font-semibold">Paper Mode Configuration</h1>
        <div className="mt-6 space-y-4 text-sm text-slate-300">
          <p>Backend secrets stay server-side in backend environment variables.</p>
          <p>Discord alerts are sent only when DISCORD_WEBHOOK_URL is configured on the backend.</p>
          <p>No MT5 or broker execution is implemented in V1.</p>
        </div>
      </div>
    </main>
  );
}
