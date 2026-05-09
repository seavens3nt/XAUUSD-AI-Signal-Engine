# XAUUSD AI Signal Engine

Paper-trading / assisted-decision foundation for scanning XAUUSD market context.

V1 is intentionally mock-data only. It does not connect to MT5, does not place broker orders, and does not contain hidden auto-trading. The deterministic risk engine runs before the fake LLM trader, and every decision is validated before it can become a paper signal.

## Architecture

- Frontend: Next.js, React, Tailwind
- Backend: Python FastAPI
- Scheduler: APScheduler, every 5 minutes
- Database boundary: repository layer, currently in-memory; Supabase/PostgreSQL can replace it later
- Market data V1: mock XAUUSD candles and quote
- Market data V2: `MT5ClientPlaceholder`, deliberately disabled
- Alerts: Discord webhook formatter/sender, server-side only
- AI V1: fake strict-JSON trader
- AI later: OpenAI structured JSON output behind the same validator

## Run Backend

```bash
cd xauusd-ai-signal-engine/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

Useful endpoints:

- `GET /health`
- `POST /api/signals/run-once`
- `POST /api/signals/run-once?scenario=trending`
- `GET /api/signals/latest`
- `GET /api/signals/history`
- `POST /api/comments`

## Run Frontend

```bash
cd xauusd-ai-signal-engine/frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## Safety Rules In V1

- Paper trading / assisted decision only
- No real broker execution
- No MT5 connection
- No martingale
- No averaging down
- No adding to losing trades
- No increasing lot size after losses
- Risk engine calculates suggested lot size, not the LLM
- Discord webhook stays in backend environment only

## Signal Flow

1. Generate 15 closed M1, M5, and H1 mock candles plus bid/ask/spread.
2. Compute trend, momentum, mean reversion pressure, volatility, chop, session, spread, news, and mock volume state.
3. Apply hard deterministic risk filters.
4. Build a dashboard-style LLM prompt.
5. Ask the fake LLM trader for strict JSON.
6. Validate JSON, SL/TP side, confidence, R:R, and risk filter status.
7. Log the decision.
8. Format and optionally send Discord alert when a webhook is configured.

## Environment

Copy `.env.example` files when needed. Do not put `DISCORD_WEBHOOK_URL`, Supabase service keys, or future broker credentials in the frontend.
