# Create a BankAccount class with methods for depositing,withdrawing and getting balance of an account.
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance
# Example usage:
if __name__ == "__main__":
    account = BankAccount(100)
    print("Initial Balance:", account.get_balance())  # Output: Initial Balance: 100

    account.deposit(50)
    print("Balance after deposit of 50:", account.get_balance())  # Output: Balance after deposit of 50: 150

    account.withdraw(30)
    print("Balance after withdrawal of 30:", account.get_balance())  # Output: Balance after withdrawal of 30: 120