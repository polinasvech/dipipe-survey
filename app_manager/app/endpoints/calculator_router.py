import logging
from collections import Counter
from itertools import cycle
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from helpers import colors3, colors10
from schemas.calculator_schemas import (BaseRequest, CalculatorResponse,
                                        NpsResponse)
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


@router.get("/dashboard/{survey_id}")
async def dashboard(
    survey_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
    client_service: ClientService = Depends(ClientService),
) -> ReportTemplate:
    try:
        survey_service.get_survey_by_id(survey_id)
    except KeyError:
        logger.error(f"Survey not found for ID: {survey_id}")
        raise HTTPException(status_code=404, detail="Survey not found")

    try:
        clients = client_service.get_all_clients()
    except Exception as e:  # TODO
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=400, detail="Error fetching clients")

    # BLOCK 1
    main_colors = colors10()

    division_counter = Counter(client.division for client in clients)
    colors_map = list(zip(division_counter.items(), cycle(main_colors)))

    division_diagram = Diagram(
        uuid=str(uuid4()),
        title="По дивизионам",
        type="bar",
        categories=[
            Category(label=division_count_tuple[0], value=division_count_tuple[1], color=color)
            for division_count_tuple, color in colors_map
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

    clients_block = Block(diagrams=[division_diagram, type_diagram, preferences_diagram])

    # BLOCK 2
    calculator = Calculator(survey_id=survey_id)
    metrics_stat = calculator.get_main_metrics()

    main_colors = colors3()

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

    main_metrics_blocks = Block(diagrams=[loyalty_diagram, satisfaction_diagram, repeat_purchase_diagram])

    # BLOCK 3
    nps, avg_total = calculator.calculate_nps()

    main_colors = colors10()
    main_colors = [c for v, c in list(zip(nps, cycle(main_colors)))]

    categories_cols = []
    categories_table = [[":)", ":|", ":("]]
    for i, key in enumerate(nps):
        categories_cols.append(Category(label=key, value=nps[key]["average"], color=main_colors[i]))
        categories_table.append(
            [str(nps[key]["promoters_percent"]), str(nps[key]["neutral_percent"]), str(nps[key]["critics_percent"])]
        )
    categories_table = [list(row) for row in zip(*categories_table)]

    columns_diagram = Diagram(
        uuid=str(uuid4()),
        title="Удовлетворенность в разбивке по процессам",
        type="column",
        categories=categories_cols,
    )
    satisfaction_by_process_diagram_block = Block(diagrams=[columns_diagram])

    table_diagram = Diagram(
        uuid=str(uuid4()),
        title="",
        type="table",
        categories=categories_table,
    )
    satisfaction_by_process_table_block = Block(diagrams=[table_diagram])

    return ReportTemplate(
        uuid=str(uuid4()),
        title="Статистика по клиентам",
        blocks=[clients_block, main_metrics_blocks, satisfaction_by_process_diagram_block, satisfaction_by_process_table_block],
    )
