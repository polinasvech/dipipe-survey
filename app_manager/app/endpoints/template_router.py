from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app_manager.app.models.template_model import Template,CreateTemplateRequest
from app_manager.app.services.template_service import TemplateService

template_router = APIRouter(prefix="/templates", tags=["Templates"])


@template_router.get("/")
def get_all_templates(
    template_service: TemplateService = Depends(TemplateService),
) -> list[Template]:
    return template_service.get_all_templates()


@template_router.get("/{template_id}")
def get_template_by_id(
    template_id: UUID,
    template_service: TemplateService = Depends(TemplateService),
) -> Template:
    try:
        return template_service.get_template_by_id(template_id)
    except KeyError:
        raise HTTPException(404, detail=f"Template with id={template_id} not found")


@template_router.post("/")
def create_template(
    request: CreateTemplateRequest,
    template_service: TemplateService = Depends(TemplateService),
) -> Template:
    try:
        return template_service.create_template(request.initial_survey_id, request.template_text)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@template_router.put("/")
def update_template(
    initial_survey_id: UUID,
    template_text: Optional[str] = None,
    template_service: TemplateService = Depends(TemplateService),
) -> Template:
    try:
        return template_service.update_template(initial_survey_id, template_text)
    except KeyError:
        raise HTTPException(404, detail=f"Template for survey_id={initial_survey_id} not found")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@template_router.delete("/{template_id}")
def delete_template(
    template_id: UUID,
    template_service: TemplateService = Depends(TemplateService),
) -> dict:
    try:
        template_service.delete_template(template_id)
        return {"detail": "Template deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Template with id={template_id} not found")
