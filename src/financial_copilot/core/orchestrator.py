from __future__ import annotations

import asyncio

from financial_copilot.agents.base import AnalysisAgent
from financial_copilot.core.scoring import classify_verdict, weighted_support_score
from financial_copilot.domain.models import AnalysisRequest, AnalysisResponse


class FinancialCopilot:
    def __init__(self, agents: list[AnalysisAgent]) -> None:
        self.agents = agents
        dimensions = {agent.dimension for agent in agents}
        if "red_team" not in dimensions:
            raise ValueError("A red_team agent is mandatory.")
        if "risk" not in dimensions:
            raise ValueError("A risk agent is mandatory.")

    async def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        # Agents run independently and receive only the investor proposal.
        # Cross-agent conclusions are intentionally unavailable at this stage.
        results = await asyncio.gather(*(agent.analyze(request) for agent in self.agents))

        support_score, confidence, dimension_scores = weighted_support_score(results)
        risk_score = dimension_scores.get("risk")
        verdict = classify_verdict(support_score, risk_score)

        evidence = [item for result in results for item in result.evidence]
        risks = list(dict.fromkeys(risk for result in results for risk in result.risks))
        invalidation_conditions = list(
            dict.fromkeys(
                condition
                for result in results
                for condition in result.invalidation_conditions
            )
        )

        return AnalysisResponse(
            ticker=request.ticker,
            proposed_action=request.proposed_action,
            as_of=request.as_of,
            verdict=verdict,
            support_score=support_score,
            confidence=confidence,
            dimension_scores=dimension_scores,
            evidence=evidence,
            main_risks=risks,
            invalidation_conditions=invalidation_conditions,
        )
