from fastapi import Depends
from app.dtos import AppealDTO, PaginatedAppealsDTO
from app.repositories import AppealRepository
from app.api.dependencies import get_appeal_repository
from app.services import AccountService

class AppealService():
    _instance = None

    @classmethod
    def depends_init(cls, repository: AppealRepository = Depends(get_appeal_repository), account_service: AccountService = Depends(AccountService.depends_init)):
        if cls._instance is None:
            cls._instance = cls(repository=repository, account_service=account_service)
        return cls._instance

    def __init__(self, repository: AppealRepository, account_service: AccountService):
        self.repository = repository
        self.account_service = account_service
    
    async def create_appeal(self, appeal: AppealDTO):
        is_linked = await self.account_service.get_linked_minecraft_username(appeal.appealer_id) is not None
        if not is_linked:
            raise ValueError("Discord account must be linked to a Minecraft account to create an appeal")
        return AppealDTO.from_model(await self.repository.create_appeal(appeal))

    async def get_appeal(self, appeal_id):
        appeal = await self.repository.get_appeal(appeal_id)
        return AppealDTO.from_model(appeal)

    async def get_appeals(self, page: int = 1, page_size: int = 10):
        paginated = await self.repository.get_appeals(page, page_size)
        paginated["data"] = [AppealDTO.from_model(appeal) for appeal in paginated["data"]]
        return PaginatedAppealsDTO(**paginated)

    async def update_appeal_pledged(self, appeal_id, amount):
        appeal = await self.repository.get_appeal(appeal_id)
        if not appeal:
            raise ValueError("Appeal not found")
        new_pledged = appeal.pledged + amount
        return await self.repository.update_appeal_pledged(appeal_id, new_pledged)

    async def apply_interest(self, appeal_id):
        appeal = await self.repository.get_appeal(appeal_id)
        if not appeal:
            raise ValueError("Appeal not found")
        new_amount = appeal.remaining_amount * (1 + appeal.monthly_interest)
        return await self.repository.update_amount_remaining(appeal_id, new_amount)

    async def update_appeal_amount_remaining(self, appeal_id, amount):
        appeal = await self.repository.get_appeal(appeal_id)
        if not appeal:
            raise ValueError("Appeal not found")
        new_remaining = appeal.remaining_amount + amount
        return await self.repository.update_amount_remaining(appeal_id, new_remaining)

    async def set_appeal_active(self, appeal_id):
        appeal = await self.repository.get_appeal(appeal_id)
        if not appeal:
            raise ValueError("Appeal not found")
        pledged = appeal.pledged
        if pledged <= 0:
            raise ValueError("Cannot activate appeal with no pledged amount")
        await self.repository.update_amount_remaining(appeal_id, pledged)
        await self.account_service.update_balance(appeal.appealer_id, pledged)
        return AppealDTO.from_model(await self.repository.update_appeal_status(appeal_id, "active"))

    async def set_appeal_repaid(self, appeal_id):
        return AppealDTO.from_model(await self.repository.update_appeal_status(appeal_id, "repaid"))

    async def set_appeal_defaulted(self, appeal_id):
        return AppealDTO.from_model(await self.repository.update_appeal_status(appeal_id, "defaulted")) 

    async def set_appeal_cancelled(self, appeal_id):
        return AppealDTO.from_model(await self.repository.update_appeal_status(appeal_id, "cancelled"))