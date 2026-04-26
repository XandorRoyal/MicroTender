from fastapi import Depends, HTTPException

from app.api.dependencies import get_transfer_repository
from app.api.exceptions import AppealNotFound, InsufficientFunds
from app.models import AppealTransactionModel
from app.repositories import TransferRepository
from app.services.AccountService import AccountService
from app.services.AppealService import AppealService

from app.dtos import AppealDTO

class TransferService():
    _instance = None

    @classmethod
    def depends_init(
        cls,
        account_service: AccountService = Depends(AccountService.depends_init),
        appeal_service: AppealService = Depends(AppealService.depends_init),
        transfer_repository: TransferRepository = Depends(get_transfer_repository),
    ):
        if cls._instance is None:
            cls._instance = cls(account_service, appeal_service, transfer_repository)
        return cls._instance 

    def __init__(self, account_service: AccountService, appeal_service: AppealService, transfer_repository: TransferRepository):
        self.account_service = account_service
        self.appeal_service = appeal_service
        self.transfer_repository = transfer_repository

    async def get_transfers_for_appeal(self, appeal_id):
        return await self.transfer_repository.get_transfers_for_appeal(appeal_id)

    async def get_transfer(self, transfer_id):
        return await self.transfer_repository.get_transfer(transfer_id)
    
    async def lend(self, discord_id, appeal_id, amount):
        appeal = await self.appeal_service.get_appeal(appeal_id)
        if appeal.status != "funding":
            raise HTTPException(status_code=400, detail="Appeal is not open for funding")  
        if await self.account_service.get_balance(discord_id) <= amount:
            raise InsufficientFunds("Insufficient balance to lend")
        await self.account_service.update_balance(discord_id, -amount)
        await self.appeal_service.update_appeal_pledged(appeal_id, amount)
        return await self.transfer_repository.create_transfer(appeal_id, discord_id, amount, 'lending')
    
    def get_percentage_funded(self, appeal: AppealDTO, transfers: list[AppealTransactionModel]):
        if appeal.amount == 0:
            return 0
        pledged = appeal.pledged
        accounts_total = {}
        accounts_percentage = {}
        for transfer in transfers:
            if transfer.account_id not in accounts_total:
                accounts_total[transfer.account_id] = 0
            accounts_total[transfer.account_id] += transfer.amount
            accounts_percentage[transfer.account_id] = accounts_total[transfer.account_id] / pledged
        return accounts_percentage

    async def payback(self, appeal_id, discord_id, amount):
        appeal = await self.appeal_service.get_appeal(appeal_id)
        if appeal is None:
            raise AppealNotFound("Appeal not found")
        if appeal.status != "active":
            raise HTTPException(status_code=400, detail="Appeal is not active")
        if appeal.pledged <= 0:
            raise HTTPException(status_code=400, detail="Appeal has no pledged amount")
        if appeal.appealer_id != discord_id:
            raise HTTPException(status_code=403, detail="Only the appealer can repay the appeal")
        if await self.account_service.get_balance(discord_id) <= amount:
            raise InsufficientFunds("Insufficient balance to repay")
        lending_transfers = await self.transfer_repository.get_transfers_for_appeal_lending(appeal_id)
        if discord_id not in lending_transfers.items():
            raise HTTPException(status_code=400, detail="Appeal has no lending transfers")
        appeal_interest = appeal.interest

        if amount > appeal_interest:
            await self.appeal_service.deduct_interest(appeal_id, appeal_interest)
            amount -= appeal_interest
        if amount > 0:
            await self.appeal_service.update_appeal_amount_remaining(appeal_id, -amount)
        await self.account_service.update_balance(discord_id, -amount)
        accounts_to_percent = self.get_percentage_funded(appeal, lending_transfers)

        # Distribute the repayment amount proportionally to lenders based on their percentage
        repayment_transfers = []
        for lender_id, percentage in accounts_to_percent.items():
            lender_share = amount * percentage
            await self.account_service.update_balance(lender_id, lender_share)
            repayment_transfers.append(
                await self.transfer_repository.create_transfer(appeal_id, lender_id, lender_share, 'repayment')
            )
        return repayment_transfers