import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as AccountCrud




@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "amount",
        [
            (5000),
        ],
    )
    def test_deposit_user(self, db_session: Session, api_manager: ApiManager, create_user_with_one_account: tuple, amount: int):
        user, account = create_user_with_one_account

        response = api_manager.user_steps.deposit(user, account_id=account.id, amount=amount)
        assert response.balance == amount, "Баланс в ответе не равен сумме пополнения"

        account_from_db = AccountCrud.get_account_by_id(db_session, account.id)
        assert account_from_db is not None, "Аккаунт не найден в DB"
        assert account_from_db.balance == amount, "Баланс аккаунта в DB не равен сумме пополнения"


    @pytest.mark.parametrize(
        "amount",
        [
            (999),
            (9001),
        ],
    )
    def test_deposit_bank_user_invalid(self, api_manager: ApiManager, create_user_with_one_account: tuple, amount: int):
        user, account = create_user_with_one_account
        response = api_manager.user_steps.deposit_invalid(user, account_id=account.id, amount=amount)
