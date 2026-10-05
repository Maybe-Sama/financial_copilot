from __future__ import annotations

from abc import ABC, abstractmethod

from financial_copilot.domain.models import AgentResult, AnalysisRequest


class AnalysisAgent(ABC):
    name: str
    dimension: str

    @abstractmethod
    async def analyze(self, request: AnalysisRequest) -> AgentResult:
        """Analyze one investment proposal without seeing other agents' conclusions."""
        raise NotImplementedError
