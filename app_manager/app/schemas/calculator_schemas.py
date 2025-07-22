from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class CalculatorRequest(BaseModel):
    survey_uuid: UUID


class MetricValues(BaseModel):
    NPS: float
    CSI: float
    probability_repeat_purchase: float = Field(..., alias="Вероятность Повторной Покупки")

    # class Config:
    #     validate_by_name = True


class NpsSchema(BaseModel):
    average: float
    promoters: int
    neutral: int
    critics: int


class NpsResponse(BaseModel):
    nps: Dict[str, NpsSchema]
    average_total: float


class CalculatorResponse(BaseModel):
    survey_uuid: UUID
    metrics: Dict[str, MetricValues]
    nps: NpsResponse
