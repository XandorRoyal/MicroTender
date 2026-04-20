from fastapi import Depends

from app.dependencies import get_transfer_repository
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

    def get_transfers_for_appeal(self, appeal_id):
        return self.transfer_repository.get_transfers_for_appeal(appeal_id)

    def get_transfer(self, transfer_id):
        return self.transfer_repository.get_transfer(transfer_id)
    
    def lend(self, discord_id, appeal_id, amount):
        if self.account_service.get_balance(discord_id) <= amount:
            raise ValueError("Insufficient balance to lend")
        self.account_service.update_balance(discord_id, -amount)
        self.appeal_service.update_appeal_pledged(appeal_id, amount)
        return self.transfer_repository.create_transfer(appeal_id, discord_id, amount, 'lending')
    
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

    def payback(self, appeal_id, discord_id, amount):
        appeal = self.appeal_service.get_appeal(appeal_id)
        if appeal is None:
            raise ValueError("Appeal not found")
        if appeal.status != "active":
            raise ValueError("Appeal is not active")
        if appeal.pledged <= 0:
            raise ValueError("Appeal has no pledged amount")
        if appeal.appealer_id != discord_id:
            raise ValueError("Only the appealer can repay the appeal")
        if self.account_service.get_balance(discord_id) <= amount:
            raise ValueError("Insufficient balance to repay")

        self.appeal_service.update_appeal_amount_remaining(appeal_id, -amount)
        self.account_service.update_balance(discord_id, -amount)
        lending_transfers = self.transfer_repository.get_transfers_for_appeal_lending(appeal_id)
        accounts_to_percent = self.get_percentage_funded(appeal, lending_transfers)

        # Distribute the repayment amount proportionally to lenders based on their percentage
        repayment_transfers = []
        for lender_id, percentage in accounts_to_percent.items():
            lender_share = amount * percentage
            self.account_service.update_balance(lender_id, lender_share)
            repayment_transfers.append(
                self.transfer_repository.create_transfer(appeal_id, lender_id, lender_share, 'repayment')
            )
        return repayment_transfers