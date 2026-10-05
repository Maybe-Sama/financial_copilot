from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Action(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class Verdict(str, Enum):
    SUPPORTED = "SUPPORTED"
    MIXED = "MIXED"
    REJECTED = "REJECTED"


class Evidence(BaseModel):
    agent: str
    dimension: str
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    summary: str
    supports_proposal: bool
    observed_at: datetime
    source: str | None = None
    source_timestamp: datetime | None = None
    metadata: dict[str, str | float | int | bool] = Field(default_factory=dict)

    @field_validator("observed_at", "source_timestamp")
    @classmethod
    def timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware")
        return value


class AnalysisRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    proposed_action: Action
    horizon: str = Field(min_length=1, max_length=80)
    thesis: list[str] = Field(default_factory=list, max_length=20)
    as_of: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("as_of")
    @classmethod
    def as_of_is_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        return value


class AgentResult(BaseModel):
    agent: str
    dimension: str
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    evidence: list[Evidence] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    invalidation_conditions: list[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    ticker: str
    proposed_action: Action
    as_of: datetime
    verdict: Verdict
    support_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    dimension_scores: dict[str, float]
    evidence: list[Evidence]
    main_risks: list[str]
    invalidation_conditions: list[str]
    methodology: Literal["weighted-independent-consensus-v1"] = "weighted-independent-consensus-v1"
    disclaimer: str = (
        "Research output only. This score is not a probability of profit and is not personalised financial advice."
    )
