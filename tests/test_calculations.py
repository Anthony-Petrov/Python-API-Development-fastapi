from app.calculations import (
    add,
    subtract,
    divide,
    multiply,
    BankAccount,
    InsufficientFunds,
)
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def hundred_bank_account():
    return BankAccount(100)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (4, 2, 6), (0, 0, 0)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(10, 7) == 3


def test_divide():
    assert divide(21, 7) == 3


def test_multiply():
    assert multiply(3, 7) == 21


def test_bank_set_initial_amount(hundred_bank_account):
    assert hundred_bank_account.balance == 100


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_deposit_amount(zero_bank_account):
    zero_bank_account.deposit(50)
    assert zero_bank_account.balance == 50


def test_bank_withdraw_amount():
    bank_account = BankAccount(120)
    bank_account.withdraw(60)
    assert bank_account.balance == 60


def test_bank_collect_interest(hundred_bank_account):
    hundred_bank_account.collect_interest()
    assert round(hundred_bank_account.balance, 6) == 110


@pytest.mark.parametrize(
    "deposit_amount, withdraw_amount, expected",
    [(120, 20, 110), (20, 5, 16.5), (43, 7, 39.6)],
)
def test_bank_transactions(
    zero_bank_account, deposit_amount, withdraw_amount, expected
):
    zero_bank_account.deposit(deposit_amount)
    zero_bank_account.withdraw(withdraw_amount)
    zero_bank_account.collect_interest()
    assert round(zero_bank_account.balance, 3) == expected


def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(10)
