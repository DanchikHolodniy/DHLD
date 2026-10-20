import pytest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "amount",
        [
            (5000),
        ],
    )
    def test_deposit_user(self, api_manager, create_user_request, amount):
        account = api_manager.user_steps.create_account(create_user_request)
        response = api_manager.user_steps.deposit(
            create_user_request, account_id=account.id, amount=amount
        )
        assert response.balance == amount

    @pytest.mark.parametrize(
        "amount",
        [
            (999),
            (9001),
        ],
    )
    def test_deposit_bank_user_invalid(self, api_manager, create_user_request, amount):
        account = api_manager.user_steps.create_account(create_user_request)
        response = api_manager.user_steps.deposit_invalid(
            create_user_request, account_id=account.id, amount=amount
        )
