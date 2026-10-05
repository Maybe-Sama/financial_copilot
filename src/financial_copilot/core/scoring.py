from __future__ import annotations

from financial_copilot.domain.models import AgentResult, Verdict


DEFAULT_WEIGHTS: dict[str, float] = {
    "quant": 0.25,
    "fundamental": 0.20,
    "technical": 0.10,
    "news_macro": 0.10,
    "debate": 0.10,
    "risk": 0.15,
    "red_team": 0.10,
}


def weighted_support_score(
    results: list[AgentResult],
    weights: dict[str, float] | None = None,
) -> tuple[float, float, dict[str, float]]:
    active_weights = weights or DEFAULT_WEIGHTS
    result_by_dimension = {result.dimension: result for result in results}

    weighted_sum = 0.0
    confidence_sum = 0.0
    total_weight = 0.0
    dimension_scores: dict[str, float] = {}

    for dimension, weight in active_weights.items():
        result = result_by_dimension.get(dimension)
        if result is None:
            continue

        score = result.score
        # Red-team is adversarial: a high red-team score means the proposal resisted attack.
        # Providers should normalize their output to that convention before returning AgentResult.
        weighted_sum += score * weight
        confidence_sum += result.confidence * weight
        total_weight += weight
        dimension_scores[dimension] = round(score, 2)

    if total_weight == 0:
        return 50.0, 0.0, dimension_scores

    return (
        round(weighted_sum / total_weight, 2),
        round(confidence_sum / total_weight, 3),
        dimension_scores,
    )


def classify_verdict(score: float, risk_score: float | None = None) -> Verdict:
    # Risk acts as a gate so a superficially strong consensus cannot wave through
    # a proposal that fails the dedicated risk pass.
    if risk_score is not None and risk_score < 40:
        return Verdict.REJECTED
    if score >= 70:
        return Verdict.SUPPORTED
    if score >= 50:
        return Verdict.MIXED
    return Verdict.REJECTED
