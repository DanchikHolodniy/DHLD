import pytest

from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as CreditCrud


@pytest.mark.api
class TestCredit:
    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (10000, 12),
        ],
    )
    def test_credit_user(
        self,
        db_session: Session,
        api_manager,
        create_user_credit_request,
        amount,
        termMonths,
    ):
        account = api_manager.user_steps.create_account_credit(
            create_user_credit_request
        )
        response = api_manager.user_steps.credit(
            create_user_credit_request,
            account_id=account.id,
            amount=amount,
            termMonths=termMonths,
        )
        assert response.balance == amount
        assert response.termMonths == termMonths

        credit_from_db = CreditCrud.get_credit_by_account_id(db_session, account.id)

        assert credit_from_db is not None, "Кредит не был выдан"
        assert credit_from_db.balance == -amount

    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (4999, 12),
            (15001, 12),
        ],
    )
    def test_credit_user_invalid(
        self, api_manager, create_user_credit_request, amount, termMonths
    ):
        account = api_manager.user_steps.create_account(create_user_credit_request)
        response = api_manager.user_steps.credit_invalid(
            create_user_credit_request,
            account_id=account.id,
            amount=amount,
            termMonths=termMonths,
        )
