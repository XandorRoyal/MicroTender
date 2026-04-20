from fastapi import APIRouter, Depends, Query

from app.dtos import AppealDTO, PaginatedAppealsDTO
from app.services import AppealService, TransferService

appeal_router = APIRouter(prefix="/appeals", tags=["appeals"])

@appeal_router.post("/create")
def create_appeal(appeal: AppealDTO, service: AppealService = Depends(AppealService.depends_init)):
    return service.create_appeal(appeal)

@appeal_router.get("/{appeal_id}")
def get_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return service.get_appeal(appeal_id)

@appeal_router.get("/", response_model=PaginatedAppealsDTO)
def get_appeals(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    service: AppealService = Depends(AppealService.depends_init)
):
    return service.get_appeals(page, page_size)

@appeal_router.post("/{appeal_id}/lend")
def lend_to_appeal(appeal_id: str, pledger_id: str, amount: float, service: TransferService = Depends(TransferService.depends_init)):
    return service.lend(pledger_id, appeal_id, amount)

@appeal_router.post("/{appeal_id}/repay")
def repay_appeal(appeal_id: str, payer_id: str, amount: float, service: TransferService = Depends(TransferService.depends_init)):
    return service.payback(appeal_id, payer_id, amount)

@appeal_router.post("/{appeal_id}/activate")
def activate_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return service.set_appeal_active(appeal_id)

@appeal_router.delete("/{appeal_id}/close")
def close_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return service.set_appeal_cancelled(appeal_id)