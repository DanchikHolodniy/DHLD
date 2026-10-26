import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as CreditCrud




@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (10000, 12),
        ]
    )
    def test_credit_repay(self, db_session: Session, api_manager: ApiManager, create_account_with_credit: tuple, amount: int, termMonths: int):
        user, account, credit = create_account_with_credit(amount, termMonths)
        assert credit.balance == amount
        assert credit.termMonths == termMonths

        repay = api_manager.user_steps.repay(user, creditId=credit.creditId, accountId=account.id, amount=amount)
        assert repay.amountDeposited == amount, "Сумма погашения в ответе сервера не совпадает"

        credit_repay_from_db = CreditCrud.get_credit_by_account_id(db_session, account.id)

        assert credit_repay_from_db is not None, "Кредит не существует в DB"
        assert credit_repay_from_db.balance == 0, "Кредит в DB не обнулился после погашения"


    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (10000, 12)
        ]
    )
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_account_with_credit: tuple, amount: int, termMonths: int):
        user, account, credit = create_account_with_credit(amount, termMonths)
        bad_not_all_repay = api_manager.user_steps.repay_invalid(user, creditId=credit.creditId, accountId=account.id, amount=amount // 2)
