from typing import Any

from pydantic import BaseModel, ConfigDict


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_data: dict[str, Any]


class PredictionResponse(BaseModel):
    churn_probability: float
    predicted_churn: int
    risk_tier: str
    decision_threshold: float