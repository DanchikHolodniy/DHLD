import pytest


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize(
        "amount,termMonths",
        [
            (10000, 12),
        ],
    )
    def test_credit_repay(
        self, api_manager, create_user_credit_request, amount, termMonths
    ):
        account = api_manager.user_steps.create_account_credit(
            create_user_credit_request
        )
        credit = api_manager.user_steps.credit(
            create_user_credit_request,
            account_id=account.id,
            amount=amount,
            termMonths=termMonths,
        )
        assert credit.balance == amount
        assert credit.termMonths == termMonths

        repay = api_manager.user_steps.repay(
            create_user_credit_request,
            creditId=credit.creditId,
            accountId=account.id,
            amount=amount,
        )
        assert repay.amountDeposited == amount

    @pytest.mark.parametrize("amount,termMonths", [(4999, 12), (15001, 12)])
    def test_credit_repay_invalid(
        self, api_manager, create_user_credit_request, amount, termMonths
    ):
        account = api_manager.user_steps.create_account_credit(
            create_user_credit_request
        )
        credit = api_manager.user_steps.credit_invalid(
            create_user_credit_request,
            account_id=account.id,
            amount=amount,
            termMonths=termMonths,
        )
