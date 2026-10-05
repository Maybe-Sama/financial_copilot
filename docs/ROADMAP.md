# Roadmap

## Phase 0 — Repository foundation ✅

- [x] Domain models.
- [x] FastAPI service.
- [x] Independent agent protocol.
- [x] Mandatory risk and red-team agents.
- [x] Weighted consensus.
- [x] Initial tests.
- [x] Point-in-time rules documented.

## Phase 1 — Real market-data layer

Goal: replace fixtures with reproducible, timestamped data.

- [ ] Define `MarketDataProvider` protocol.
- [ ] Add OHLCV provider.
- [ ] Add corporate-actions adjustments.
- [ ] Add benchmark data.
- [ ] Add trading-calendar normalization.
- [ ] Introduce central point-in-time validator.
- [ ] Persist immutable analysis snapshots.
- [ ] Add data provenance/version metadata.

**Acceptance criterion:** an analysis can be replayed later from the same snapshot and obtain identical deterministic inputs.

## Phase 2 — Deterministic technical/risk engine

- [ ] Trend and momentum features.
- [ ] Volatility metrics.
- [ ] Drawdown metrics.
- [ ] Benchmark-relative strength.
- [ ] Risk score based on explicit rules.
- [ ] Configurable horizon-specific feature sets.

**Rule:** calculations live in code, not in LLM prompts.

## Phase 3 — Qlib quantitative adapter

- [ ] Research Qlib licensing/dependency strategy.
- [ ] Build `QlibQuantAgent` adapter.
- [ ] Define factor dataset schema.
- [ ] Implement walk-forward evaluation.
- [ ] Include transaction cost/slippage model.
- [ ] Return normalized `AgentResult`.
- [ ] Store model/data version with every result.

Optional extension:

- [ ] RD-Agent experimentation sandbox for generating/evaluating candidate factors.
- [ ] Require deterministic backtests before any generated factor is promoted.

## Phase 4 — Fundamental analysis

- [ ] Filing-data provider.
- [ ] Financial statement normalization.
- [ ] Deterministic ratio/valuation calculator.
- [ ] Fundamental LLM agent using only supplied structured facts.
- [ ] Evidence citations/source timestamps.
- [ ] Thesis-vs-fundamentals contradiction detector.

## Phase 5 — News / macro

- [ ] Timestamped news provider.
- [ ] Enforce publication cutoff.
- [ ] Deduplicate syndicated stories.
- [ ] Event classification.
- [ ] Macro-regime feature set.
- [ ] Separate company, sector and macro evidence.

## Phase 6 — Multi-agent debate

Preferred implementation path: evaluate TradingAgents as an adapter/reference architecture rather than tightly coupling core code to it.

- [ ] Bull analyst.
- [ ] Bear analyst.
- [ ] Evidence-aware debate.
- [ ] Claim extraction.
- [ ] Contradiction resolution.
- [ ] Prevent agents from seeing hidden future data in historical runs.

## Phase 7 — Red-team engine

- [ ] Explicit thesis decomposition into falsifiable claims.
- [ ] Counter-evidence search.
- [ ] Missing-variable detection.
- [ ] Staleness detection.
- [ ] Horizon mismatch detection.
- [ ] Confirmation-bias checklist.
- [ ] Produce explicit thesis invalidation conditions.

## Phase 8 — Persistence and dashboard

Suggested stack:

- PostgreSQL for analyses/evidence/results.
- Object storage for immutable raw snapshots where required.
- FastAPI backend.
- Next.js frontend.

Dashboard views:

1. New proposal.
2. Analysis report.
3. Agent disagreement matrix.
4. Evidence timeline.
5. Open theses and invalidation conditions.
6. Historical decisions.
7. Calibration dashboard.
8. Performance vs benchmark.

## Phase 9 — Calibration

This is when the project starts answering the important question: **does the second opinion add value?**

For each historical decision store:

- proposal timestamp
- action
- horizon
- support score
- component scores
- later realized return
- benchmark return
- max adverse excursion
- max favorable excursion
- whether invalidation condition occurred

Then measure:

- support bucket vs future outcome
- Brier score if probabilities are eventually produced
- expected calibration error
- information coefficient where applicable
- incremental value over baseline investor decisions
- incremental value of each agent
- ablation tests (remove one agent and re-evaluate)

## Phase 10 — Portfolio-aware second opinion

- [ ] Portfolio holdings/import.
- [ ] Position sizing context.
- [ ] Correlation/concentration analysis.
- [ ] Sector/factor exposure.
- [ ] Portfolio-level risk veto.

A good stock can still be a bad additional trade if it duplicates existing exposure.

## Phase 11 — Optional broker integration

Only after research quality is validated.

Default design:

```text
analysis -> proposed order -> human confirmation -> broker
```

No autonomous live execution in the standard configuration.

---

# MVP definition

The first genuinely useful MVP is complete when a user can submit:

```text
ticker + BUY/HOLD/SELL + horizon + thesis
```

and receive a report backed by **real point-in-time data** containing:

- quant score
- fundamental score
- technical score
- news/macro score
- bull case
- bear case
- red-team objections
- risk score
- overall support score
- strongest supporting evidence
- strongest contradictory evidence
- explicit thesis invalidation conditions

with every external fact traceable to its source and timestamp.
