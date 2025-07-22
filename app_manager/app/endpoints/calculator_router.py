import logging
from collections import Counter
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from helpers import generate_random_hex_color
from schemas.calculator_schemas import BaseRequest, CalculatorResponse, ClientsStatisticsResponse, NpsResponse
from schemas.diagrams import Block, Category, Diagram, ReportTemplate
from services.calculator import Calculator
from services.client_service import ClientService
from services.survey_service import SurveyService

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
) -> ReportTemplate:
    try:
        clients = client_service.get_all_clients()
    except Exception as e:  # TODO
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=400, detail="Error fetching clients")

    main_colors = [generate_random_hex_color() for _ in range(25)]  # TODO
    division_counter = Counter(client.division for client in clients)
    division_diagram = Diagram(
        uuid=str(uuid4()),
        title="По дивизионам",
        type="column",
        categories=[
            Category(label=division_count_tuple[0], value=division_count_tuple[1], color=color)
            for color, division_count_tuple in zip(main_colors, division_counter.items())
        ],
    )

    type_counter = Counter(client.ca_type for client in clients)
    type_diagram = Diagram(
        uuid=str(uuid4()),
        title="По типам",
        type="round",
        categories=[
            Category(label=type_count_tuple[0], value=round(type_count_tuple[1] / len(clients) * 100, 2), color=color)
            for color, type_count_tuple in zip(main_colors, type_counter.items())
        ],
    )

    preferences_counter = Counter(client.preferences for client in clients)
    preferences_diagram = Diagram(
        uuid=str(uuid4()),
        title="По преференциям",
        type="round",
        categories=[
            Category(label=pref_count_tuple[0], value=round(pref_count_tuple[1] / len(clients) * 100, 2), color=color)
            for color, pref_count_tuple in zip(main_colors, preferences_counter.items())
        ],
    )

    blocks = Block(diagrams=[division_diagram, type_diagram, preferences_diagram])
    return ReportTemplate(uuid=str(uuid4()), title="Статистика по клиентам", blocks=[blocks])


@router.post("/metrics_statistics")
async def calculate(
    request: BaseRequest,
    survey_service: SurveyService = Depends(SurveyService),
) -> ReportTemplate:
    try:
        survey_service.get_survey_by_id(request.survey_uuid)
    except KeyError:
        logger.error(f"Survey not found for ID: {request.survey_uuid}")
        raise HTTPException(status_code=404, detail="Survey not found")

    calculator = Calculator(survey_id=request.survey_uuid)
    metrics_stat = calculator.get_main_metrics()

    main_colors = [generate_random_hex_color() for _ in range(3)]

    loyalty_diagram = Diagram(
        uuid=str(uuid4()),
        title="Лояльность",
        type="round",
        categories=[
            Category(label=kv_tuple[0], value=kv_tuple[1], color=color)
            for color, kv_tuple in zip(main_colors, metrics_stat["loyalty"].items())
        ],
    )
    satisfaction_diagram = Diagram(
        uuid=str(uuid4()),
        title="Удовлетворенность",
        type="round",
        categories=[
            Category(label=kv_tuple[0], value=kv_tuple[1], color=color)
            for color, kv_tuple in zip(main_colors, metrics_stat["satisfaction"].items())
        ],
    )

    repeat_purchase_diagram = Diagram(
        uuid=str(uuid4()),
        title="Вероятность повторной покупки",
        type="round",
        categories=[
            Category(label=kv_tuple[0], value=kv_tuple[1], color=color)
            for color, kv_tuple in zip(main_colors, metrics_stat["repeat_purchase"].items())
        ],
    )

    blocks = Block(diagrams=[loyalty_diagram, satisfaction_diagram, repeat_purchase_diagram])
    return ReportTemplate(uuid=str(uuid4()), title="Статистика по клиентам", blocks=[blocks])
