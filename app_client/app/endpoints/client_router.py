from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app_client.app.schemas.client_schema import Client
from app_client.app.services.client_service import ClientService

client_router = APIRouter(prefix="/clients", tags=["Clients"])


@client_router.post("/")
def create_client(
    client_id: UUID,
    tin: str,
    preferences: str,
    division: str,
    ca_type: str,
    client_service: ClientService = Depends(ClientService),
) -> Client:
    try:
        return client_service.create_client(client_id, tin, preferences, division, ca_type)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@client_router.get("/")
def get_all_clients(
    client_service: ClientService = Depends(ClientService),
) -> list[Client]:
    return client_service.get_all_clients()


@client_router.get("/{client_id}")
def get_client_by_id(
    client_id: UUID,
    client_service: ClientService = Depends(ClientService),
) -> Client:
    try:
        return client_service.get_client_by_id(client_id)
    except KeyError:
        raise HTTPException(404, detail=f"Client with id={client_id} not found")


@client_router.put("/{client_id}")
def update_client(
    client_id: UUID,
    tin: str,
    preferences: str,
    division: str,
    ca_type: str,
    client_service: ClientService = Depends(ClientService),
) -> Client:
    try:
        return client_service.update_client(client_id, tin, preferences, division, ca_type)
    except KeyError:
        raise HTTPException(404, detail=f"Client with id={client_id} not found")


@client_router.delete("/{client_id}")
def delete_client(
    client_id: UUID,
    client_service: ClientService = Depends(ClientService),
) -> dict:
    try:
        client_service.delete_client(client_id)
        return {"detail": "Client deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Client with id={client_id} not found")
