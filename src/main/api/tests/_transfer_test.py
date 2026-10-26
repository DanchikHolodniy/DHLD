import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as TransactionCrud




@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize(
        "amount",
        [
            (1000),
        ],
    )
    def test_transfer(self, db_session: Session, api_manager: ApiManager, create_two_users_with_accounts_deposit: tuple, amount: int):
        user, first_account, second_account = create_two_users_with_accounts_deposit(amount)

        first_to_second_account_deposit = api_manager.user_steps.transfer(user, first_account.id, second_account.id, amount=amount)
        assert first_to_second_account_deposit.fromAccountIdBalance == 0, "Баланс отправителя не стал 0"

        transaction_from_db = TransactionCrud.get_transaction_by_from_account_id(db_session, first_to_second_account_deposit.fromAccountId)
        assert transaction_from_db is not None, "Транзакция не найдена в DB"
        assert transaction_from_db.amount == amount, "Сумма перевода не совпадает с DB"


    @pytest.mark.parametrize(
        "amount,transfer",
        [
            (1000, 600),
        ],
    )
    def test_transfer_my_accounts(self, db_session: Session, api_manager: ApiManager, create_user_with_two_accounts_deposit: tuple, amount: int, transfer: int):
        user, my_first_account, my_second_account = create_user_with_two_accounts_deposit(amount)

        transfer_between_my_accounts = api_manager.user_steps.transfer(user, my_first_account.id, my_second_account.id, amount=transfer)
        assert transfer_between_my_accounts.fromAccountIdBalance == amount - transfer, "Баланс отправителя не совпадает с ожидаемым"

        transaction_from_db = TransactionCrud.get_transaction_by_from_account_id(db_session, transfer_between_my_accounts.fromAccountId)
        assert transaction_from_db is not None, "Транзакция не найдена в DB"
        assert transaction_from_db.amount == transfer, "Сумма перевода не совпадает с DB"
        assert transaction_from_db.to_account_id == my_second_account.id, "id аккаунта не совпадает с DB"


    @pytest.mark.parametrize(
        "valid_amount_deposit, valid_transfer",
        [
            (5000, 500),
            (10000, 10000)
        ]
    )
    def test_transfer_range_valid(self, api_manager: ApiManager, create_two_users_with_accounts_deposit: tuple, valid_amount_deposit: int, valid_transfer: int):
        user, first_account, second_account = create_two_users_with_accounts_deposit(valid_amount_deposit)

        first_to_second_transfer = api_manager.user_steps.transfer(user, first_account.id, second_account.id, amount=valid_transfer)
        assert first_to_second_transfer.fromAccountIdBalance == valid_amount_deposit - valid_transfer


    @pytest.mark.parametrize(
        "invalid_amount_deposit",
        [
            999,
            9001,
        ],
    )
    def test_transfer_range_deposit_invalid(self, api_manager: ApiManager, create_user_with_one_account: tuple, invalid_amount_deposit: int):
        user, account = create_user_with_one_account
        invalid_deposit = api_manager.user_steps.deposit_invalid(user, account_id=account.id, amount=invalid_amount_deposit)


    @pytest.mark.parametrize(
        "valid_amount_deposit, invalid_transfer",
        [
            (1000, 499),
            (9000, 10001),
        ],
    )
    def test_transfer_range_transfer_invalid(self, api_manager: ApiManager, create_user_with_two_accounts_deposit: tuple, valid_amount_deposit: int, invalid_transfer: int):
        user, my_first_account, my_second_account = create_user_with_two_accounts_deposit(valid_amount_deposit)
        first_to_second_transfer = api_manager.user_steps.transfer_invalid(user, my_first_account.id, my_second_account.id, amount=invalid_transfer)
