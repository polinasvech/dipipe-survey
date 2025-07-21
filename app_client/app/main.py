import asyncio

from fastapi import FastAPI

from app_client.app.endpoints.client_router import client_router
from app_client.app.schemas import client_schema
from app_client.app.schemas.base_schema import engine
app = FastAPI(title='App')
client_schema.Base.metadata.create_all(bind=engine)


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()


app.include_router(client_router)
