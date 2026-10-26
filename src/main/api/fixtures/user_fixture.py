import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.create_user_credit import CreateUserCreditRequest




@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request




@pytest.fixture
def second_create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request




@pytest.fixture
def create_two_users_with_accounts(api_manager: ApiManager, create_user_request: CreateUserRequest, second_create_user_request: CreateUserRequest):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(second_create_user_request)
    return first_account, second_account




@pytest.fixture
def create_two_users_with_accounts_deposit(api_manager: ApiManager, create_user_request: CreateUserRequest, create_two_users_with_accounts: tuple):
    first_account, second_account = create_two_users_with_accounts
    def _deposit(amount: int):
        if amount > 9000:
            api_manager.user_steps.deposit(create_user_request, account_id=first_account.id, amount=amount // 2)
            api_manager.user_steps.deposit(create_user_request, account_id=first_account.id, amount=amount // 2)
        else:
            api_manager.user_steps.deposit(create_user_request, account_id=first_account.id, amount=amount)
        return create_user_request, first_account, second_account
    return _deposit




@pytest.fixture
def create_user_with_one_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account = api_manager.user_steps.create_account(create_user_request)
    return create_user_request, account




@pytest.fixture
def create_user_with_two_accounts(api_manager: ApiManager, create_user_request: CreateUserRequest):
    my_first_account = api_manager.user_steps.create_account(create_user_request)
    my_second_account = api_manager.user_steps.create_account(create_user_request)
    return create_user_request, my_first_account, my_second_account




@pytest.fixture
def create_user_with_two_accounts_deposit(api_manager: ApiManager, create_user_request: CreateUserRequest, create_user_with_two_accounts: CreateUserRequest):
    user, first_account, second_account = create_user_with_two_accounts
    def _deposit(amount: int):
        api_manager.user_steps.deposit(create_user_request, account_id=first_account.id, amount=amount)
        return create_user_request, first_account, second_account
    return _deposit




@pytest.fixture
def create_user_credit_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserCreditRequest)
    api_manager.admin_steps.create_user_credit(user_request)
    return user_request




@pytest.fixture
def create_credit_account(api_manager: ApiManager, create_user_credit_request: CreateUserCreditRequest):
    account = api_manager.user_steps.create_account_credit(create_user_credit_request)
    return create_user_credit_request, account




@pytest.fixture
def create_account_with_credit(api_manager: ApiManager, create_credit_account: tuple):
    user, account = create_credit_account
    def _take_credit(amount: int, termMonths: int):
        credit = api_manager.user_steps.credit(user, account_id=account.id, amount=amount, termMonths=termMonths)
        return user, account, credit
    return _take_credit
