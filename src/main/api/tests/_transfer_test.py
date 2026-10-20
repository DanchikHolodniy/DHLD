import pytest

from sqlalchemy.orm import Session
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as TransactionCrud


@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize(
        "amount",
        [
            (1000),
        ],
    )
    def test_transfer(
        self,
        db_session: Session,
        api_manager,
        create_user_request,
        second_create_user_request,
        amount,
    ):
        first_account = api_manager.user_steps.create_account(create_user_request)
        second_account = api_manager.user_steps.create_account(
            second_create_user_request
        )
        first_account_deposit = api_manager.user_steps.deposit(
            create_user_request, account_id=first_account.id, amount=amount
        )

        assert first_account_deposit.balance == amount

        first_to_second_deposit = api_manager.user_steps.transfer(
            create_user_request, first_account.id, second_account.id, amount=amount
        )

        assert first_to_second_deposit.fromAccountIdBalance == 0

        transaction_from_db = TransactionCrud.get_transaction_by_from_account_id(
            db_session, first_to_second_deposit.fromAccountId
        )

        assert transaction_from_db is not None, "Транзакция не найдена в DB"
        assert transaction_from_db.amount == amount

    @pytest.mark.parametrize(
        "amount,transfer",
        [
            (1000, 600),
        ],
    )
    def test_transfer_my_accounts(
        self,
        db_session: Session,
        api_manager,
        create_user_request,
        second_create_user_request,
        amount,
        transfer,
    ):
        my_first_account = api_manager.user_steps.create_account(create_user_request)
        my_second_account = api_manager.user_steps.create_account(create_user_request)
        my_first_account_deposit = api_manager.user_steps.deposit(
            create_user_request, account_id=my_first_account.id, amount=amount
        )

        assert my_first_account_deposit.balance == amount

        transfer_between_my_accounts = api_manager.user_steps.transfer(
            create_user_request,
            my_first_account.id,
            my_second_account.id,
            amount=transfer,
        )

        assert transfer_between_my_accounts.fromAccountIdBalance == amount - transfer

        transaction_from_db = TransactionCrud.get_transaction_by_from_account_id(
            db_session, transfer_between_my_accounts.fromAccountId
        )

        assert transaction_from_db is not None, "Транзакция не найдена в DB"
        assert transaction_from_db.amount == transfer
        assert (
            transaction_from_db.to_account_id == my_second_account.id
        ), "Деньги ушли не на тот счёт"

    @pytest.mark.parametrize(
        "valid_amount_deposit, valid_transfer", [(5000, 500), (5000, 10000)]
    )
    def test_transfer_range_valid(
        self,
        api_manager,
        create_user_request,
        second_create_user_request,
        valid_amount_deposit,
        valid_transfer,
    ):
        first_account = api_manager.user_steps.create_account(create_user_request)
        second_account = api_manager.user_steps.create_account(
            second_create_user_request
        )
        first_account_deposit = api_manager.user_steps.deposit(
            create_user_request,
            account_id=first_account.id,
            amount=valid_amount_deposit,
        )
        first_account_deposit_double = api_manager.user_steps.deposit(
            create_user_request,
            account_id=first_account.id,
            amount=valid_amount_deposit,
        )

        assert first_account_deposit_double.balance == valid_amount_deposit * 2

        first_to_second_deposit = api_manager.user_steps.transfer(
            create_user_request,
            first_account.id,
            second_account.id,
            amount=valid_transfer,
        )

        assert (
            first_to_second_deposit.fromAccountIdBalance
            == first_account_deposit_double.balance - valid_transfer
        )

    @pytest.mark.parametrize(
        "invalid_amount_deposit",
        [
            999,
            9001,
        ],
    )
    def test_transfer_range_deposit_invalid(
        self, api_manager, create_user_request, invalid_amount_deposit
    ):
        first_account = api_manager.user_steps.create_account(create_user_request)
        first_account_deposit = api_manager.user_steps.deposit_invalid(
            create_user_request,
            account_id=first_account.id,
            amount=invalid_amount_deposit,
        )

    @pytest.mark.parametrize(
        "valid_amount_deposit, invalid_transfer",
        [
            (1000, 499),
            (9000, 10001),
        ],
    )
    def test_transfer_range_transfer_invalid(
        self,
        api_manager,
        create_user_request,
        second_create_user_request,
        valid_amount_deposit,
        invalid_transfer,
    ):
        first_account = api_manager.user_steps.create_account(create_user_request)
        second_account = api_manager.user_steps.create_account(
            second_create_user_request
        )
        first_account_deposit = api_manager.user_steps.deposit(
            create_user_request,
            account_id=first_account.id,
            amount=valid_amount_deposit,
        )
        first_to_second_deposit = api_manager.user_steps.transfer_invalid(
            create_user_request,
            first_account.id,
            second_account.id,
            amount=invalid_transfer,
        )
