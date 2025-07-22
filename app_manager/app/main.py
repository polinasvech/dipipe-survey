import asyncio
import logging
from fastapi import FastAPI

from app_manager.app.endpoints.answer_router import answer_router
from app_manager.app.endpoints.manager_router import manager_router
from app_manager.app.endpoints.question_router import question_router
from app_manager.app.endpoints.survey_router import survey_router
from app_manager.app.endpoints.template_router import template_router
from app_manager.app.endpoints.client_router import client_router
from app_manager.app.endpoints.admin_router import admin_router
from app_manager.app.schemas import answer_schema,manager_schema,question_schema,syrvey_schema,template_schema,client_schema,category_schema
from app_manager.app.schemas.base_schema import engine
app = FastAPI(title='App')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler('app.log')  # Запись в файл
    ]
)

logger = logging.getLogger(__name__)
answer_schema.Base.metadata.create_all(bind=engine)
manager_schema.Base.metadata.create_all(bind=engine)
question_schema.Base.metadata.create_all(bind=engine)
syrvey_schema.Base.metadata.create_all(bind=engine)
template_schema.Base.metadata.create_all(bind=engine)
client_schema.Base.metadata.create_all(bind=engine)
category_schema.Base.metadata.create_all(bind=engine)
@app.on_event('startup')
def startup():
    logger.info("Application started")
    loop = asyncio.get_event_loop()


app.include_router(answer_router)
app.include_router(manager_router)
app.include_router(question_router)
app.include_router(survey_router)
app.include_router(template_router)
app.include_router(client_router)
app.include_router(admin_router)
# from scripts.import_xlsx import InitialParser
#
# if __name__ == "__main__":
#     parser = InitialParser()
#     parser.run()

