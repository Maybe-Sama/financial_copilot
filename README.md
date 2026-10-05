# Financial Copilot

**Financial Copilot** is an investment *second-opinion* system. It does **not** try to replace the investor with an LLM. Instead, it takes a proposed action (BUY / HOLD / SELL), collects independent evidence, actively tries to disprove the thesis, and produces an auditable support score.

> Core principle: **the system must try to prove you wrong before it is allowed to support your trade.**

## What this project is

You provide a proposal such as:

```text
Ticker: NVDA
Action: BUY
Horizon: 3-6 months
Thesis: AI demand + earnings momentum + secular datacenter growth
```

Financial Copilot runs independent analysis tracks:

1. **Quant** — deterministic/statistical evidence (Qlib / RD-Agent planned).
2. **Fundamental** — filings, earnings, valuation, business quality.
3. **Technical** — trend, momentum, volatility and market structure.
4. **News / macro** — current information constrained to the analysis timestamp.
5. **Bull analyst** — strongest evidence supporting the proposal.
6. **Bear analyst** — strongest evidence opposing it.
7. **Red team** — attempts to invalidate the investment thesis.
8. **Risk manager** — downside, concentration, regime and invalidation conditions.
9. **Meta judge** — aggregates independent evidence and explains the final verdict.

The output is intentionally **not** "78% chance this stock goes up". It is a calibrated **support score** for the proposed decision.

## Architecture

```text
                         INVESTOR PROPOSAL
                                |
                                v
                    +------------------------+
                    | Point-in-time Snapshot |
                    |  as_of / data cutoff   |
                    +-----------+------------+
                                |
                +---------------+----------------+
                |                                |
                v                                v
        +---------------+                +----------------+
        | Quantitative  |                | Agentic review |
        | Qlib / models |                | fundamentals   |
        +-------+-------+                | news / bull    |
                |                        | bear / risk     |
                |                        +--------+-------+
                |                                 |
                +----------------+----------------+
                                 v
                         +---------------+
                         |   RED TEAM    |
                         | disprove it   |
                         +-------+-------+
                                 |
                                 v
                         +---------------+
                         |  META JUDGE   |
                         +-------+-------+
                                 |
                                 v
                     SUPPORT / MIXED / REJECT
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the design rules.

## Current status

This repository contains the **MVP skeleton**:

- FastAPI HTTP API.
- Typed investment-analysis domain models.
- Pluggable agent protocol.
- Independent mock agents so the full flow can be exercised immediately.
- Weighted consensus engine.
- Mandatory red-team pass.
- Risk gate.
- Point-in-time `as_of` field throughout the workflow.
- Audit-friendly evidence objects.
- Initial tests.

The mock agents are **development fixtures, not market analysis**. The next phase replaces them with real data and engines.

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/Maybe-Sama/financial_copilot.git
cd financial_copilot
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn financial_copilot.api.main:app --reload
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn financial_copilot.api.main:app --reload
```

Open:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Example request

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "proposed_action": "BUY",
    "horizon": "3-6 months",
    "thesis": [
      "AI infrastructure demand remains structurally strong",
      "earnings momentum supports the thesis"
    ]
  }'
```

Example response shape:

```json
{
  "ticker": "NVDA",
  "proposed_action": "BUY",
  "verdict": "SUPPORTED",
  "support_score": 74.8,
  "confidence": 0.67,
  "evidence": [],
  "main_risks": [],
  "invalidation_conditions": []
}
```

## Scoring philosophy

A high score means **independent evidence currently agrees with the proposed action**. It is not a forecast probability.

Initial dimensions:

| Dimension | Initial weight |
|---|---:|
| Quant | 25% |
| Fundamental | 20% |
| Technical | 10% |
| News / macro | 10% |
| Bull / bear debate | 10% |
| Risk | 15% |
| Red team | 10% |

These are bootstrap weights only. The goal is to learn/calibrate them later from walk-forward out-of-sample results.

## Non-negotiable research rules

1. **Point-in-time integrity.** Historical analysis must not consume data published after `as_of`.
2. **No hidden consensus.** Agents should not see each other's conclusions until the synthesis stage.
3. **Red-team before approval.** Every proposal must receive an adversarial pass.
4. **Deterministic metrics stay deterministic.** P&L, indicators, drawdown, Sharpe, volatility and backtests are calculated by code, not guessed by an LLM.
5. **No accuracy theatre.** Never report a confidence score as a probability until calibration demonstrates that interpretation.
6. **Auditability.** Evidence records should retain source, timestamp, calculation/model version and reasoning summary.
7. **Out-of-sample first.** Strategy evaluation uses walk-forward validation, costs, slippage and a benchmark.

## Planned integrations

- [TradingAgents](https://github.com/TauricResearch/TradingAgents) — multi-agent qualitative analysis.
- [Microsoft Qlib](https://github.com/microsoft/qlib) — quantitative research/backtesting.
- [Microsoft RD-Agent](https://github.com/microsoft/RD-Agent) — automated quantitative R&D.
- FinRobot-inspired fundamental analysis workflows.
- Market / filing / news providers with strict timestamp filtering.

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Safety / scope

Financial Copilot is research software, **not a broker and not personalised financial advice**. The project should initially remain read-only: no automatic order execution. A broker adapter, if ever added, should require an explicit human confirmation boundary.

## License

No license has been selected yet. Do not assume third-party integrations or source code can be copied into this repository; respect each upstream project's license and integration terms.
