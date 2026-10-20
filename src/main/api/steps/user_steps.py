from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import (
    ValidateCrudRequester,
)
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.create_user_credit import CreateUserCreditRequest
from src.main.api.models.credit_account import CreditAccountRequest
from src.main.api.models.credit_repay import CreditRepayRequest
from src.main.api.models.deposit_account import DepositRequest
from src.main.api.models.transfer_account import TransferRequest
from src.main.api.specs.request_spc import Request
from src.main.api.specs.response_spc import ResponseSpc
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpc.response_create(),
        ).post()
        return response

    def create_account_invalid(self, create_user_request: CreateUserRequest):
        response = CrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpc.response_conflict(),
        ).post(create_user_request)
        return response

    def create_account_credit(self, create_user_request: CreateUserCreditRequest):
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpc.response_create(),
        ).post()
        return response

    def deposit(
        self, create_user_request: CreateUserRequest, account_id: int, amount: float
    ):
        deposit_request = DepositRequest(
            accountId=account_id,
            amount=amount,
        )
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpc.response_ok(),
        ).post(deposit_request)
        return response

    def credit(
        self,
        create_user_credit_request: CreateUserCreditRequest,
        account_id: int,
        amount: float,
        termMonths: int,
    ):
        credit_request = CreditAccountRequest(
            accountId=account_id, amount=amount, termMonths=termMonths
        )
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password,
            ),
            Endpoint.CREDIT_ACCOUNT,
            ResponseSpc.response_create(),
        ).post(credit_request)
        return response

    def credit_invalid(
        self,
        create_user_credit_request: CreateUserCreditRequest,
        account_id: int,
        amount: float,
        termMonths: int,
    ):
        credit_request = CreditAccountRequest(
            accountId=account_id, amount=amount, termMonths=termMonths
        )
        response = CrudRequester(
            Request.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password,
            ),
            Endpoint.CREDIT_ACCOUNT,
            ResponseSpc.response_bad(),
        ).post(credit_request)
        return response

    def repay(
        self,
        create_user_credit_request: CreateUserCreditRequest,
        creditId: int,
        accountId: int,
        amount: float,
    ):
        credit_request = CreditRepayRequest(
            creditId=creditId,
            accountId=accountId,
            amount=amount,
        )
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password,
            ),
            Endpoint.CREDIT_REPAY_ACCOUNT,
            ResponseSpc.response_ok(),
        ).post(credit_request)
        return response

    def deposit_invalid(
        self, create_user_request: CreateUserRequest, account_id: int, amount: float
    ):
        deposit_request = DepositRequest(
            accountId=account_id,
            amount=amount,
        )
        response = CrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpc.response_bad(),
        ).post(deposit_request)
        return response

    def transfer(
        self,
        create_user_request: CreateUserRequest,
        first_account_id,
        second_account_id,
        amount: float,
    ):
        transfer_request = TransferRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=amount,
        )
        response = ValidateCrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpc.response_ok(),
        ).post(transfer_request)
        return response

    def transfer_invalid(
        self,
        create_user_request: CreateUserRequest,
        first_account_id,
        second_account_id,
        amount: float,
    ):
        transfer_request = TransferRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=amount,
        )
        response = CrudRequester(
            Request.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpc.response_bad(),
        ).post(transfer_request)
        return response
