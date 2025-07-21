import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.manager_schema import Manager as DBManager
from app_manager.app.models.manager_model import Manager as Manager, CreateManagerRequest


class ManagerRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, manager: DBManager) -> Manager:
        return Manager.from_orm(manager)

    def _map_to_schema(self, manager: Manager) -> DBManager:
        return DBManager(
            uuid=manager.uuid,
            full_name=manager.full_name
        )

    def create_manager(self, manager: Manager) -> Manager:
        try:
            db_manager = self._map_to_schema(manager)
            self.db.add(db_manager)
            self.db.commit()
            self.db.refresh(db_manager)
            return self._map_to_model(db_manager)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_all_managers(self) -> List[Manager]:
        return [self._map_to_model(m) for m in self.db.query(DBManager).all()]

    def get_manager_by_id(self, manager_id: UUID) -> Manager:
        manager = self.db.query(DBManager).filter(DBManager.uuid == manager_id).first()
        if not manager:
            raise KeyError(f"Manager with id {manager_id} not found.")
        return self._map_to_model(manager)

    def update_manager(self, manager: Manager) -> Manager:
        try:
            db_manager = self.db.query(DBManager).filter(DBManager.uuid == manager.uuid).first()
            for field, value in manager.model_dump().items():
                setattr(db_manager, field, value)
            self.db.commit()
            return self._map_to_model(db_manager)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def delete_manager(self, manager_id: UUID) -> None:
        try:
            self.db.query(DBManager).filter(DBManager.uuid == manager_id).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise
