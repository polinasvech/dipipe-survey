from typing import Dict
from uuid import UUID

from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    survey_uuid: UUID


class MetricValues(BaseModel):
    NPS: float
    CSI: float
    probability_repeat_purchase: float = Field(..., alias="Вероятность Повторной Покупки")


class NpsSchema(BaseModel):
    average: float
    promoters: int
    neutral: int
    critics: int
    promoters_percent: float
    neutral_percent: float
    critics_percent: float
    neutral_percent: float
    nps_val: float = Field(..., description="(% Промоутеры - % Критики)")


class NpsResponse(BaseModel):
    nps: Dict[str, NpsSchema]
    average_total: float


class CalculatorResponse(BaseModel):
    survey_uuid: UUID
    metrics: Dict[str, MetricValues]
    nps: NpsResponse


class ClientsStatisticsResponse(BaseModel):
    by_division: Dict[str, int]
    by_type: Dict[str, int]
    by_preferences: Dict[str, int]
