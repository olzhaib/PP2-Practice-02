class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Not enough money")


account = Account("Aiman", 0)

account.deposit(500)
account.deposit(200)
account.deposit(300)

account.withdraw(300)
account.withdraw(1000)
account.withdraw(1000)

print(account.balance)

