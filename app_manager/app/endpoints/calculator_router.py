from fastapi import APIRouter, Depends, HTTPException
from schemas.calculator_schemas import BaseRequest, CalculatorResponse, NpsResponse, ClientsStatisticsResponse
from services.calculator import Calculator
from services.survey_service import SurveyService
from services.client_service import ClientService
import logging
from collections import Counter

router = APIRouter(prefix="/calculator", tags=["Calculator"])

logger = logging.getLogger(__name__)


@router.post("/")
async def calculate(
    request: BaseRequest,
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


@router.post("/clients_statistics")
async def calculate(
    client_service: ClientService = Depends(ClientService),
) -> ClientsStatisticsResponse:
    try:
        clients = client_service.get_all_clients()
    except Exception as e:  # TODO
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=400, detail="Error fetching clients")

    division_counter = Counter(client.division for client in clients)
    type_counter = Counter(client.ca_type for client in clients)
    preferences_counter = Counter(client.preferences for client in clients)

    return ClientsStatisticsResponse(
        by_division=dict(division_counter),
        by_type=dict(type_counter),
        by_preferences=dict(preferences_counter)
    )
