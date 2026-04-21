from fastapi import APIRouter, Depends, Query

from app.dtos import AppealDTO, PaginatedAppealsDTO
from app.services import AppealService, TransferService

appeal_router = APIRouter(prefix="/appeals", tags=["appeals"])

@appeal_router.post("/create")
async def create_appeal(appeal: AppealDTO, service: AppealService = Depends(AppealService.depends_init)):
    return await service.create_appeal(appeal)

@appeal_router.get("/{appeal_id}")
async def get_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return await service.get_appeal(appeal_id)

@appeal_router.get("/", response_model=PaginatedAppealsDTO)
async def get_appeals(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    service: AppealService = Depends(AppealService.depends_init)
):
    return await service.get_appeals(page, page_size)

@appeal_router.post("/{appeal_id}/lend")
async def lend_to_appeal(appeal_id: str, pledger_id: str, amount: float, service: TransferService = Depends(TransferService.depends_init)):
    return await service.lend(pledger_id, appeal_id, amount)

@appeal_router.post("/{appeal_id}/repay")
async def repay_appeal(appeal_id: str, payer_id: str, amount: float, service: TransferService = Depends(TransferService.depends_init)):
    return await service.payback(appeal_id, payer_id, amount)

@appeal_router.post("/{appeal_id}/activate")
async def activate_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return await service.set_appeal_active(appeal_id)

@appeal_router.delete("/{appeal_id}/close")
async def close_appeal(appeal_id: str, service: AppealService = Depends(AppealService.depends_init)):
    return await service.set_appeal_cancelled(appeal_id)