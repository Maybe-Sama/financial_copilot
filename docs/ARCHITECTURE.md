# Architecture

## 1. Purpose

Financial Copilot is a **decision-validation system**, not a price oracle.

The system receives an investor proposal and asks several independent analysis engines whether current point-in-time evidence supports it. Before a positive verdict can be produced, an adversarial red-team pass and a dedicated risk pass are mandatory.

The architecture is designed around five properties:

1. **Independence** — analysis tracks do not initially see each other's conclusions.
2. **Point-in-time integrity** — no source may contain information unavailable at `as_of`.
3. **Determinism where possible** — financial calculations are code, not language-model guesses.
4. **Auditability** — every conclusion can be traced to evidence, timestamp and provider/version.
5. **Calibration** — confidence becomes probabilistic only after out-of-sample evidence justifies it.

---

## 2. Domain flow

```text
AnalysisRequest
  ticker
  proposed_action
  horizon
  thesis[]
  as_of
       |
       v
PointInTimeDataLayer
       |
       +--> Quant adapter ---------> AgentResult
       +--> Fundamental adapter ---> AgentResult
       +--> Technical adapter -----> AgentResult
       +--> News/Macro adapter ----> AgentResult
       +--> Debate adapter --------> AgentResult
       +--> Risk adapter ----------> AgentResult
       +--> Red-team adapter ------> AgentResult
                                      |
                                      v
                                Consensus Engine
                                      |
                                      v
                               AnalysisResponse
```

The current MVP uses deterministic fixtures in place of provider adapters. Their job is to verify orchestration and contracts only.

---

## 3. Point-in-time contract

`AnalysisRequest.as_of` is the hard information cutoff.

A production provider must reject or remove observations whose publication/availability timestamp is greater than `as_of`.

### Rule

For any evidence item `e`:

```text
e.source_timestamp <= request.as_of
```

The key timestamp is when the information became available to the market, **not merely the period it describes**.

Example: a Q2 earnings report describing June data but published in August must not be visible to a July backtest.

### Planned implementation

Every provider adapter will return an `Evidence` object containing:

- `source`
- `source_timestamp`
- `observed_at`
- provider/model/calculation metadata

A central PIT validator will fail closed when a timestamp is missing for a historical run.

---

## 4. Agent independence

Agents receive:

- proposal
- approved point-in-time data for their domain

They **must not** receive other agents' conclusions during the independent analysis stage.

Why: five agents prompted with the same preceding conclusions are not five independent signals. Correlated LLM outputs create false confidence.

A later synthesis/debate stage may compare outputs explicitly.

---

## 5. Dimensions

### Quant

Target stack: Microsoft Qlib and optionally RD-Agent research workflows.

Responsibilities:

- factor/model signals
- cross-sectional and time-series evidence
- volatility and regime features
- benchmark-relative analysis
- walk-forward evaluation

All performance metrics are calculated deterministically.

### Fundamental

Responsibilities:

- income statement / balance sheet / cash flow
- valuation
- growth and quality metrics
- earnings revisions/surprises where PIT data permits
- competitive/business risks

LLMs may summarize evidence but cannot invent numeric inputs.

### Technical

Responsibilities:

- trend
- momentum
- volatility
- volume/market structure
- support/resistance only if algorithmically defined

Indicators are computed in code.

### News / macro

Responsibilities:

- timestamped company news
- sector developments
- macro regime
- event risk

Retrieval must enforce `published_at <= as_of`.

### Debate

Bull and bear cases should be generated independently before being compared.

The output is not "who wrote the better prose". It should identify which claims are supported, contradicted or unresolved by evidence.

### Risk

Responsibilities include:

- downside scenarios
- volatility / drawdown
- portfolio concentration (later phase)
- correlation exposure
- liquidity where relevant
- thesis invalidation
- horizon mismatch

Risk has veto capability in the consensus engine.

### Red team

The red team receives the proposal and evidence and is explicitly tasked with finding:

- falsified assumptions
- missing variables
- contradictory facts
- stale evidence
- confirmation bias
- causal stories unsupported by data
- regime changes
- reasons the proposed horizon may be wrong

A positive final verdict cannot bypass this stage.

---

## 6. Scoring

MVP weights:

```python
quant        0.25
fundamental  0.20
technical    0.10
news_macro   0.10
debate       0.10
risk         0.15
red_team     0.10
```

These values are **bootstrap configuration**, not empirical truth.

Production weights should be estimated from out-of-sample performance and periodically recalibrated.

### Semantics

`support_score = 75` means the weighted evidence system strongly supports the proposed decision under the current scoring model.

It does **not** mean:

```text
P(profit) = 75%
```

Probability-like interpretation requires calibration tests such as reliability curves / Brier score on unseen decisions.

---

## 7. Verdict policy

Initial thresholds:

- `>= 70`: SUPPORTED
- `50–69.99`: MIXED
- `< 50`: REJECTED

Risk score `< 40` forces REJECTED regardless of aggregate score.

These thresholds belong in configuration once empirical calibration begins.

---

## 8. Backtesting standard

A result is not considered credible unless the evaluation includes:

- chronological train/validation/test separation
- walk-forward or expanding-window validation
- point-in-time datasets
- realistic commissions
- spread/slippage assumptions
- benchmark
- survivorship-bias controls when applicable
- no tuning on the final test set

Metrics should include at least:

- CAGR / total return
- benchmark excess return
- Sharpe
- Sortino
- max drawdown
- volatility
- hit rate
- average win / loss
- expectancy
- profit factor
- turnover
- transaction costs
- calibration by support-score bucket

---

## 9. Provider boundaries

External projects should be integrated through adapters rather than copied wholesale into the core.

Planned adapter interfaces:

```text
providers/
  market_data/
  filings/
  news/
  quant/
  llm/

agents/
  quant.py
  fundamental.py
  technical.py
  news_macro.py
  debate.py
  risk.py
  red_team.py
```

This protects the domain model from provider churn and reduces licensing/dependency coupling.

---

## 10. Execution boundary

The MVP is **read-only**.

If broker execution is ever implemented, the architecture should enforce:

```text
Analysis -> Proposed order -> HUMAN CONFIRMATION -> Broker adapter
```

No LLM or consensus score should directly submit a live trade by default.
