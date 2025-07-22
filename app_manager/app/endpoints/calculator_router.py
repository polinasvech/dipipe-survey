from fastapi import APIRouter, Depends, HTTPException
from schemas.calculator_schemas import CalculatorRequest, CalculatorResponse, NpsResponse
from services.calculator import Calculator
from services.survey_service import SurveyService
import logging

router = APIRouter(prefix="/calculator", tags=["Calculator"])

logger = logging.getLogger(__name__)


@router.post("/")
async def calculate(
        request: CalculatorRequest,
        survey_service: SurveyService = Depends(SurveyService),
) -> CalculatorResponse:
    try:
        survey_service.get_survey_by_id(request.survey_uuid)
    except KeyError:
        logger.error(f"Survey not found for ID: {request.survey_uuid}")
        raise HTTPException(status_code=404, detail="Survey not found")

    calculator = Calculator(survey_id=request.survey_uuid)
    metrics = calculator.calculate_correlations()
    nps, avg_total = calculator.calculate_nps()
    nps_response = NpsResponse(average_total=avg_total, nps=nps)
    return CalculatorResponse(survey_uuid=request.survey_uuid, metrics=metrics, nps=nps_response)
