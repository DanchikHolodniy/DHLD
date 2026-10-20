import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.create_user_credit import CreateUserCreditRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_user_credit_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserCreditRequest)
    api_manager.admin_steps.create_user_credit(user_request)
    return user_request


@pytest.fixture
def second_create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request
