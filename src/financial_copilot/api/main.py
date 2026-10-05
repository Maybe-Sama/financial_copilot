from __future__ import annotations

from fastapi import FastAPI

from financial_copilot.agents.mock import default_mock_agents
from financial_copilot.core.orchestrator import FinancialCopilot
from financial_copilot.domain.models import AnalysisRequest, AnalysisResponse

app = FastAPI(
    title="Financial Copilot",
    version="0.1.0",
    description="Investment second-opinion engine with independent analysis, red-team review and risk gating.",
)

copilot = FinancialCopilot(default_mock_agents())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    return await copilot.analyze(request)
