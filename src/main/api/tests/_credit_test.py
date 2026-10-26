import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as CreditCrud




@pytest.mark.api
class TestCredit:
    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (10000, 12),
        ],
    )
    def test_credit_user(self, db_session: Session, api_manager: ApiManager, create_credit_account: tuple, amount: int, termMonths: int):
        user, account = create_credit_account
        response = api_manager.user_steps.credit(user, account_id=account.id, amount=amount, termMonths=termMonths)
        assert response.balance == amount, "Баланс выданного кредита не совпадает с заявленным"
        assert response.termMonths == termMonths, "Срок кредита выдан на другое количество месяцев"

        credit_from_db = CreditCrud.get_credit_by_account_id(db_session, account.id)

        assert credit_from_db is not None, "Кредит не найден в DB"
        assert credit_from_db.balance == -amount, "Баланс кредита в DB не совпадает с заявленным"


    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (4999, 12),
            (15001, 12),
        ],
    )
    def test_credit_user_invalid(self, api_manager: ApiManager, create_credit_account: tuple, amount: int, termMonths: int):
        user, account = create_credit_account
        response = api_manager.user_steps.credit_invalid(user, account_id=account.id, amount=amount, termMonths=termMonths)
