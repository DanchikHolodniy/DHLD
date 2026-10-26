from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import AccountResponse
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.create_user_response import CreateResponse
from src.main.api.models.credit_account import CreditAccountRequest
from src.main.api.models.credit_account_response import CreditAccountResponse
from src.main.api.models.credit_repay import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.deposit_account import DepositRequest
from src.main.api.models.deposit_account_response import DepositResponse
from src.main.api.models.login_user import Login
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_account import TransferRequest
from src.main.api.models.transfer_account_response import TransferResponse




@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]




class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateResponse,
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        url="/auth/token/login",
        request_model=Login,
        response_model=LoginUserResponse,
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        url="/account/create",
        request_model=None,
        response_model=AccountResponse,
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        url="/account/deposit",
        request_model=DepositRequest,
        response_model=DepositResponse,
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        url="/account/transfer",
        request_model=TransferRequest,
        response_model=TransferResponse,
    )

    CREDIT_ACCOUNT = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditAccountRequest,
        response_model=CreditAccountResponse,
    )

    CREDIT_REPAY_ACCOUNT = EndpointConfiguration(
        url="/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse,
    )
