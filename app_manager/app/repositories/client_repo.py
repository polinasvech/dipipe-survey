from uuid import UUID
import traceback
from typing import List
from typing import Union
from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.client_schema import Client as DBClient
from app_manager.app.models.client_model import Client as Client, CreateClientRequest


class ClientRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, client: DBClient) -> Client:
        result = Client.from_orm(client)
        return result

    def _map_to_schema(self, client: Client) -> DBClient:
        return DBClient(
            uuid=client.uuid,
            tin=client.tin,
            preferences=client.preferences,
            division=client.division,
            ca_type=client.ca_type
        )

    def create_client(self, client: Client) -> Client:
        try:
            db_client = self._map_to_schema(client)
            self.db.add(db_client)
            self.db.commit()
            self.db.refresh(db_client)
            return self._map_to_model(db_client)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_all_clients(self) -> List[Client]:
        return [self._map_to_model(c) for c in self.db.query(DBClient).all()]

    def get_client_by_id(self, client_id: UUID) -> Client:
        client = self.db.query(DBClient).filter(DBClient.uuid == client_id).first()
        if not client:
            raise KeyError(f"Client with id {client_id} not found.")
        return self._map_to_model(client)

    def update_client(self, client: Client) -> Client:
        try:
            db_client = self.db.query(DBClient).filter(DBClient.uuid == client.uuid).first()
            for field, value in client.model_dump().items():
                setattr(db_client, field, value)
            self.db.commit()
            return self._map_to_model(db_client)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def delete_client(self, client_id: UUID) -> None:
        try:
            self.db.query(DBClient).filter(DBClient.uuid == client_id).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise
