def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def divide(num1: int, num2: int):
    return num1 / num2


def multiply(num1: int, num2: int):
    return num1 * num2


class InsufficientFunds(Exception):
    pass


class BankAccount:

    def __init__(self, starting_balance=0):
        if starting_balance >= 0:
            self.balance = starting_balance
        else:
            raise Exception("Cant start with less than 0")

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
        else:
            raise Exception("Cant deposit less than 0")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise InsufficientFunds("Cant withdraw more than balance")

    def collect_interest(self):
        self.balance *= 1.1
