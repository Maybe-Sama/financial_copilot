from __future__ import annotations

from datetime import datetime

from financial_copilot.agents.base import AnalysisAgent
from financial_copilot.domain.models import AgentResult, AnalysisRequest, Evidence


class MockAgent(AnalysisAgent):
    """Deterministic development fixture used until a real provider is wired in."""

    def __init__(
        self,
        *,
        name: str,
        dimension: str,
        score: float,
        confidence: float,
        summary: str,
        supports_proposal: bool,
        risks: list[str] | None = None,
        invalidation_conditions: list[str] | None = None,
    ) -> None:
        self.name = name
        self.dimension = dimension
        self._score = score
        self._confidence = confidence
        self._summary = summary
        self._supports_proposal = supports_proposal
        self._risks = risks or []
        self._invalidation_conditions = invalidation_conditions or []

    async def analyze(self, request: AnalysisRequest) -> AgentResult:
        observed_at: datetime = request.as_of
        evidence = Evidence(
            agent=self.name,
            dimension=self.dimension,
            score=self._score,
            confidence=self._confidence,
            summary=self._summary,
            supports_proposal=self._supports_proposal,
            observed_at=observed_at,
            source="mock-fixture",
            source_timestamp=observed_at,
            metadata={"ticker": request.ticker, "fixture": True},
        )
        return AgentResult(
            agent=self.name,
            dimension=self.dimension,
            score=self._score,
            confidence=self._confidence,
            evidence=[evidence],
            risks=self._risks,
            invalidation_conditions=self._invalidation_conditions,
        )


def default_mock_agents() -> list[AnalysisAgent]:
    return [
        MockAgent(
            name="quant",
            dimension="quant",
            score=72,
            confidence=0.70,
            summary="Placeholder quantitative signal. Replace with Qlib/RD-Agent output.",
            supports_proposal=True,
        ),
        MockAgent(
            name="fundamental",
            dimension="fundamental",
            score=78,
            confidence=0.72,
            summary="Placeholder fundamental review. Replace with filing and valuation analysis.",
            supports_proposal=True,
            risks=["Valuation compression can invalidate an otherwise strong business thesis."],
        ),
        MockAgent(
            name="technical",
            dimension="technical",
            score=65,
            confidence=0.62,
            summary="Placeholder trend and momentum review.",
            supports_proposal=True,
        ),
        MockAgent(
            name="news_macro",
            dimension="news_macro",
            score=58,
            confidence=0.55,
            summary="Placeholder news and macro review.",
            supports_proposal=True,
            risks=["Macro regime may dominate company-specific evidence."],
        ),
        MockAgent(
            name="debate",
            dimension="debate",
            score=63,
            confidence=0.60,
            summary="Placeholder bull-vs-bear debate result.",
            supports_proposal=True,
        ),
        MockAgent(
            name="risk_manager",
            dimension="risk",
            score=60,
            confidence=0.74,
            summary="Placeholder risk score. Higher means the proposal survives more risk checks.",
            supports_proposal=True,
            risks=["Position sizing and correlation are not evaluated in the MVP fixture."],
            invalidation_conditions=["The original thesis no longer matches newly available evidence."],
        ),
        MockAgent(
            name="red_team",
            dimension="red_team",
            score=52,
            confidence=0.68,
            summary="Adversarial fixture: meaningful counterarguments exist and must be reviewed.",
            supports_proposal=False,
            risks=["Confirmation bias: the investor may be overweighting evidence consistent with the proposal."],
            invalidation_conditions=["A high-conviction claim in the thesis is falsified by point-in-time evidence."],
        ),
    ]
