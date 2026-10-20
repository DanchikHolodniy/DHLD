import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as AccountCrud
from src.main.api.models.create_user import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
    ):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = AccountCrud.get_account_by_id(db_session, response.id)

        assert (
            account_from_db.id == response.id
        ), "Аккаунт не создан, id аккаунта нет в DB"
        assert (
            account_from_db.balance is not None
        ), "Поле баланса для созданного аккаунта отсутсвует в DB"

    def test_create_account_invalid(self, api_manager, create_user_request):
        response_good = api_manager.user_steps.create_account(create_user_request)
        response_good = api_manager.user_steps.create_account(create_user_request)
        response_bad = api_manager.user_steps.create_account_invalid(
            create_user_request
        )
