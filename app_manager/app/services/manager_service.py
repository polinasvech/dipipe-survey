from uuid import UUID, uuid4
from typing import List

from fastapi import Depends

from app_manager.app.schemas.manager_schema import Manager
from app_manager.app.repositories.manager_repo import ManagerRepo


class ManagerService:
    def __init__(self, manager_repo: ManagerRepo = Depends(ManagerRepo)) -> None:
        self.manager_repo = manager_repo

    def get_all_managers(self) -> List[Manager]:
        return self.manager_repo.get_all_managers()

    def get_manager_by_id(self, manager_id: UUID) -> Manager:
        return self.manager_repo.get_manager_by_id(manager_id)

    def create_manager(self, full_name: str) -> Manager:
        manager = Manager(uuid=uuid4(), full_name=full_name)
        return self.manager_repo.create_manager(manager)

    def update_manager(self, uuid: UUID, full_name: str) -> Manager:
        manager = Manager(uuid=uuid, full_name=full_name)
        return self.manager_repo.update_manager(manager)

    def delete_manager(self, uuid: UUID) -> None:
        return self.manager_repo.delete_manager(uuid)
