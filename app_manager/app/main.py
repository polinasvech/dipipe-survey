import asyncio
import logging
from contextlib import asynccontextmanager

from endpoints.answer_router import answer_router
from endpoints.calculator_router import router as calculator_router
from endpoints.manager_router import manager_router
from endpoints.question_router import question_router
from endpoints.survey_router import survey_router
from endpoints.template_router import template_router
from endpoints.client_router import client_router
from endpoints.admin_router import admin_router
# from endpoints.client_router import client_router
# from endpoints.admin_router import admin_router
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from schemas import answer_schema, client_schema, manager_schema, question_schema, syrvey_schema, template_schema, category_schema
from schemas.base_schema import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],  # Вывод в консоль  # Запись в файл
)

logger = logging.getLogger(__name__)
answer_schema.Base.metadata.create_all(bind=engine)
manager_schema.Base.metadata.create_all(bind=engine)
question_schema.Base.metadata.create_all(bind=engine)
syrvey_schema.Base.metadata.create_all(bind=engine)
template_schema.Base.metadata.create_all(bind=engine)
client_schema.Base.metadata.create_all(bind=engine)
category_schema.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield


app = FastAPI(
    title="App",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(answer_router)
app.include_router(manager_router)
app.include_router(question_router)
app.include_router(survey_router)
app.include_router(template_router)
app.include_router(calculator_router)
app.include_router(client_router)
app.include_router(admin_router)
