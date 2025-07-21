from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app_manager.app.models.manager_model import Manager,CreateManagerRequest
from app_manager.app.services.manager_service import ManagerService

manager_router = APIRouter(prefix="/managers", tags=["Managers"])


@manager_router.get("/")
def get_all_managers(
    manager_service: ManagerService = Depends(ManagerService),
) -> list[Manager]:
    return manager_service.get_all_managers()


@manager_router.get("/{manager_id}")
def get_manager_by_id(
    manager_id: UUID,
    manager_service: ManagerService = Depends(ManagerService),
) -> Manager:
    try:
        return manager_service.get_manager_by_id(manager_id)
    except KeyError:
        raise HTTPException(404, detail=f"Manager with id={manager_id} not found")


@manager_router.post("/")
def create_manager(
    request: CreateManagerRequest,
    manager_service: ManagerService = Depends(ManagerService),
) -> Manager:
    try:
        return manager_service.create_manager(request.full_name)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@manager_router.put("/{manager_id}")
def update_manager(
    manager_id: UUID,
    full_name: str,
    manager_service: ManagerService = Depends(ManagerService),
) -> Manager:
    try:
        return manager_service.update_manager(manager_id, full_name)
    except KeyError:
        raise HTTPException(404, detail=f"Manager with id={manager_id} not found")


@manager_router.delete("/{manager_id}")
def delete_manager(
    manager_id: UUID,
    manager_service: ManagerService = Depends(ManagerService),
) -> dict:
    try:
        manager_service.delete_manager(manager_id)
        return {"detail": "Manager deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Manager with id={manager_id} not found")
