from financial_copilot.core.scoring import classify_verdict, weighted_support_score
from financial_copilot.domain.models import AgentResult, Verdict


def result(dimension: str, score: float, confidence: float = 0.8) -> AgentResult:
    return AgentResult(
        agent=dimension,
        dimension=dimension,
        score=score,
        confidence=confidence,
    )


def test_weighted_score_and_dimension_map() -> None:
    results = [
        result("quant", 80),
        result("fundamental", 70),
        result("technical", 60),
        result("news_macro", 50),
        result("debate", 70),
        result("risk", 80),
        result("red_team", 60),
    ]

    score, confidence, dimensions = weighted_support_score(results)

    assert score == 70.0
    assert confidence == 0.8
    assert dimensions["risk"] == 80


def test_risk_gate_can_reject_high_consensus() -> None:
    assert classify_verdict(85, risk_score=35) == Verdict.REJECTED


def test_supported_requires_threshold() -> None:
    assert classify_verdict(70, risk_score=60) == Verdict.SUPPORTED
    assert classify_verdict(69.9, risk_score=60) == Verdict.MIXED
