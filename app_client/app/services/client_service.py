from uuid import UUID, uuid4
from typing import List, Optional

from fastapi import Depends

from app_client.app.schemas.client_schema import Client
from app_client.app.repositories.client_repo import ClientRepo


class ClientService:
    def __init__(self, client_repo: ClientRepo = Depends(ClientRepo)) -> None:
        self.client_repo = client_repo

    def create_client(
            self,
            tin: str,
            preferences: Optional[str] = None,
            division: Optional[str] = None,
            ca_type: Optional[str] = None
    ) -> Client:
        client = Client(
            uuid = uuid4(),
            tin=tin,
            preferences=preferences,
            division=division,
            ca_type=ca_type
        )
        return self.client_repo.create_client(client)


    def get_all_clients(self) -> List[Client]:
        return self.client_repo.get_all_clients()

    def get_client_by_id(self, client_id: UUID) -> Client:
        return self.client_repo.get_client_by_id(client_id)

    def delete_client(self, client_id: UUID) -> None:
        return self.client_repo.delete_client(client_id)

    def update_client(self, client_id: UUID, tin: str,
        preferences: str,
        division: str,
        ca_type: str) -> Client:
        client = Client(
            uuid=client_id,
            tin=tin,
            preferences=preferences,
            division=division,
            ca_type=ca_type,
        )
        return self.client_repo.update_client(client)