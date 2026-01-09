import unittest
import sys
import os

# Add the parent directory to the path so we can import the BankAccount class
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bank_account import BankAccount


class TestBankAccountInitialization(unittest.TestCase):
    """Test cases for BankAccount initialization"""

    def test_init_with_default_balance(self):
        """Test that BankAccount initializes with default balance of 0"""
        account = BankAccount()
        self.assertEqual(account.get_balance(), 0)

    def test_init_with_positive_balance(self):
        """Test that BankAccount initializes with a positive balance"""
        account = BankAccount(100)
        self.assertEqual(account.get_balance(), 100)

    def test_init_with_zero_balance(self):
        """Test that BankAccount initializes with zero balance explicitly"""
        account = BankAccount(0)
        self.assertEqual(account.get_balance(), 0)

    def test_init_with_large_balance(self):
        """Test initialization with a large balance"""
        account = BankAccount(1000000)
        self.assertEqual(account.get_balance(), 1000000)

    def test_init_with_float_balance(self):
        """Test initialization with a float balance"""
        account = BankAccount(123.45)
        self.assertEqual(account.get_balance(), 123.45)


class TestBankAccountDeposit(unittest.TestCase):
    """Test cases for BankAccount deposit method"""

    def setUp(self):
        """Create a fresh BankAccount instance for each test"""
        self.account = BankAccount(100)

    def test_deposit_positive_amount(self):
        """Test depositing a positive amount"""
        result = self.account.deposit(50)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 150)

    def test_deposit_small_amount(self):
        """Test depositing a small amount"""
        result = self.account.deposit(0.01)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account.get_balance(), 100.01, places=2)

    def test_deposit_large_amount(self):
        """Test depositing a large amount"""
        result = self.account.deposit(999999)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 1000099)

    def test_deposit_zero_amount(self):
        """Test that depositing zero returns False"""
        result = self.account.deposit(0)
        self.assertFalse(result)
        self.assertEqual(self.account.get_balance(), 100)

    def test_deposit_negative_amount(self):
        """Test that depositing a negative amount returns False"""
        result = self.account.deposit(-50)
        self.assertFalse(result)
        self.assertEqual(self.account.get_balance(), 100)

    def test_deposit_multiple_times(self):
        """Test multiple deposits"""
        self.account.deposit(50)
        self.account.deposit(25)
        self.account.deposit(75)
        self.assertEqual(self.account.get_balance(), 250)

    def test_deposit_to_empty_account(self):
        """Test depositing to an account with zero balance"""
        account = BankAccount(0)
        result = account.deposit(100)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 100)

    def test_deposit_return_value_true(self):
        """Test that deposit returns True for valid deposits"""
        result = self.account.deposit(1)
        self.assertIs(result, True)

    def test_deposit_return_value_false_negative(self):
        """Test that deposit returns False (not None) for negative amounts"""
        result = self.account.deposit(-1)
        self.assertIs(result, False)

    def test_deposit_float_amount(self):
        """Test depositing float amounts"""
        result = self.account.deposit(25.75)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account.get_balance(), 125.75, places=2)


class TestBankAccountWithdraw(unittest.TestCase):
    """Test cases for BankAccount withdraw method"""

    def setUp(self):
        """Create a fresh BankAccount instance for each test"""
        self.account = BankAccount(100)

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount less than balance"""
        result = self.account.withdraw(30)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 70)

    def test_withdraw_exact_balance(self):
        """Test withdrawing the exact balance"""
        result = self.account.withdraw(100)
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_more_than_balance(self):
        """Test that withdrawing more than balance returns False"""
        result = self.account.withdraw(150)
        self.assertFalse(result)
        self.assertEqual(self.account.get_balance(), 100)

    def test_withdraw_zero_amount(self):
        """Test that withdrawing zero returns False"""
        result = self.account.withdraw(0)
        self.assertFalse(result)
        self.assertEqual(self.account.get_balance(), 100)

    def test_withdraw_negative_amount(self):
        """Test that withdrawing a negative amount returns False"""
        result = self.account.withdraw(-50)
        self.assertFalse(result)
        self.assertEqual(self.account.get_balance(), 100)

    def test_withdraw_small_amount(self):
        """Test withdrawing a small amount"""
        result = self.account.withdraw(0.01)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account.get_balance(), 99.99, places=2)

    def test_withdraw_multiple_times(self):
        """Test multiple withdrawals"""
        self.account.withdraw(10)
        self.account.withdraw(20)
        self.account.withdraw(30)
        self.assertEqual(self.account.get_balance(), 40)

    def test_withdraw_from_empty_account(self):
        """Test withdrawing from an empty account"""
        account = BankAccount(0)
        result = account.withdraw(50)
        self.assertFalse(result)
        self.assertEqual(account.get_balance(), 0)

    def test_withdraw_return_value_true(self):
        """Test that withdraw returns True for valid withdrawals"""
        result = self.account.withdraw(1)
        self.assertIs(result, True)

    def test_withdraw_return_value_false_exceeds_balance(self):
        """Test that withdraw returns False (not None) when exceeding balance"""
        result = self.account.withdraw(200)
        self.assertIs(result, False)

    def test_withdraw_float_amount(self):
        """Test withdrawing float amounts"""
        result = self.account.withdraw(25.50)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account.get_balance(), 74.50, places=2)


class TestBankAccountGetBalance(unittest.TestCase):
    """Test cases for BankAccount get_balance method"""

    def test_get_balance_initial(self):
        """Test getting initial balance"""
        account = BankAccount(500)
        self.assertEqual(account.get_balance(), 500)

    def test_get_balance_after_deposit(self):
        """Test balance after deposit"""
        account = BankAccount(100)
        account.deposit(50)
        self.assertEqual(account.get_balance(), 150)

    def test_get_balance_after_withdrawal(self):
        """Test balance after withdrawal"""
        account = BankAccount(100)
        account.withdraw(30)
        self.assertEqual(account.get_balance(), 70)

    def test_get_balance_after_multiple_operations(self):
        """Test balance after multiple operations"""
        account = BankAccount(100)
        account.deposit(50)
        account.withdraw(20)
        account.deposit(30)
        account.withdraw(10)
        self.assertEqual(account.get_balance(), 150)

    def test_get_balance_returns_correct_type(self):
        """Test that get_balance returns numeric type"""
        account = BankAccount(100)
        balance = account.get_balance()
        self.assertIsInstance(balance, (int, float))

    def test_get_balance_zero(self):
        """Test getting balance of zero"""
        account = BankAccount(0)
        self.assertEqual(account.get_balance(), 0)


class TestBankAccountIntegration(unittest.TestCase):
    """Integration tests for BankAccount operations"""

    def test_complete_transaction_sequence(self):
        """Test a complete sequence of transactions"""
        account = BankAccount(1000)
        self.assertEqual(account.get_balance(), 1000)

        # First deposit
        self.assertTrue(account.deposit(500))
        self.assertEqual(account.get_balance(), 1500)

        # First withdrawal
        self.assertTrue(account.withdraw(200))
        self.assertEqual(account.get_balance(), 1300)

        # Second deposit
        self.assertTrue(account.deposit(300))
        self.assertEqual(account.get_balance(), 1600)

        # Second withdrawal
        self.assertTrue(account.withdraw(600))
        self.assertEqual(account.get_balance(), 1000)

    def test_multiple_accounts_independence(self):
        """Test that multiple accounts are independent"""
        account1 = BankAccount(100)
        account2 = BankAccount(200)

        account1.deposit(50)
        account2.withdraw(50)

        self.assertEqual(account1.get_balance(), 150)
        self.assertEqual(account2.get_balance(), 150)

    def test_edge_case_many_small_transactions(self):
        """Test handling many small transactions"""
        account = BankAccount(100)
        
        # Make 100 deposits of $1
        for _ in range(100):
            result = account.deposit(1)
            self.assertTrue(result)
        
        self.assertEqual(account.get_balance(), 200)

        # Make 50 withdrawals of $1
        for _ in range(50):
            result = account.withdraw(1)
            self.assertTrue(result)
        
        self.assertEqual(account.get_balance(), 150)

    def test_fractional_amounts(self):
        """Test handling of fractional currency amounts"""
        account = BankAccount(100.00)
        
        account.deposit(25.50)
        account.withdraw(10.25)
        account.deposit(5.75)
        
        self.assertAlmostEqual(account.get_balance(), 121.00, places=2)

    def test_balance_remains_unchanged_on_failed_operations(self):
        """Test that balance doesn't change when operations fail"""
        account = BankAccount(100)
        
        # Failed deposit (zero)
        account.deposit(0)
        self.assertEqual(account.get_balance(), 100)
        
        # Failed deposit (negative)
        account.deposit(-50)
        self.assertEqual(account.get_balance(), 100)
        
        # Failed withdrawal (exceeds balance)
        account.withdraw(150)
        self.assertEqual(account.get_balance(), 100)
        
        # Failed withdrawal (zero)
        account.withdraw(0)
        self.assertEqual(account.get_balance(), 100)
        
        # Failed withdrawal (negative)
        account.withdraw(-50)
        self.assertEqual(account.get_balance(), 100)


class TestBankAccountEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def test_withdraw_one_cent(self):
        """Test withdrawing one cent"""
        account = BankAccount(1.00)
        result = account.withdraw(0.01)
        self.assertTrue(result)
        self.assertAlmostEqual(account.get_balance(), 0.99, places=2)

    def test_deposit_one_cent(self):
        """Test depositing one cent"""
        account = BankAccount(0)
        result = account.deposit(0.01)
        self.assertTrue(result)
        self.assertAlmostEqual(account.get_balance(), 0.01, places=2)

    def test_very_large_amount(self):
        """Test handling very large amounts"""
        account = BankAccount(1000000000)
        result = account.deposit(1000000000)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 2000000000)

    def test_precision_with_float_operations(self):
        """Test precision with multiple float operations"""
        account = BankAccount(0)
        
        for i in range(10):
            account.deposit(0.1)
        
        # Sum of 10 * 0.1 should be 1.0 (accounting for float precision)
        self.assertAlmostEqual(account.get_balance(), 1.0, places=2)

    def test_negative_initial_balance(self):
        """Test initialization with negative balance (edge case)"""
        account = BankAccount(-100)
        self.assertEqual(account.get_balance(), -100)

    def test_withdraw_with_negative_balance_account(self):
        """Test withdrawal from account with negative balance"""
        account = BankAccount(-100)
        result = account.withdraw(50)
        self.assertFalse(result)
        self.assertEqual(account.get_balance(), -100)


class TestBankAccountDataValidation(unittest.TestCase):
    """Test data validation and error handling"""

    def test_deposit_does_not_accept_string(self):
        """Test that deposit with string doesn't cause crash"""
        account = BankAccount(100)
        try:
            # This might raise a TypeError or return False
            result = account.deposit("50")
            # If it doesn't raise, it should return False
            self.assertFalse(result)
        except TypeError:
            # If it raises TypeError, that's expected behavior
            pass

    def test_withdraw_does_not_accept_string(self):
        """Test that withdraw with string doesn't cause crash"""
        account = BankAccount(100)
        try:
            result = account.withdraw("50")
            self.assertFalse(result)
        except TypeError:
            pass

    def test_balance_type_consistency(self):
        """Test that balance maintains numeric type"""
        account = BankAccount(100)
        account.deposit(50)
        account.withdraw(25)
        
        balance = account.get_balance()
        self.assertTrue(isinstance(balance, (int, float)))

    def test_operations_return_boolean(self):
        """Test that deposit and withdraw return boolean values"""
        account = BankAccount(100)
        
        deposit_result = account.deposit(50)
        self.assertIsInstance(deposit_result, bool)
        
        withdraw_result = account.withdraw(30)
        self.assertIsInstance(withdraw_result, bool)
        
        failed_deposit = account.deposit(-10)
        self.assertIsInstance(failed_deposit, bool)
        
        failed_withdraw = account.withdraw(200)
        self.assertIsInstance(failed_withdraw, bool)


class TestBankAccountBoundaryConditions(unittest.TestCase):
    """Test boundary conditions and limits"""

    def test_deposit_then_withdraw_all(self):
        """Test depositing and then withdrawing all funds"""
        account = BankAccount(0)
        
        account.deposit(500)
        self.assertEqual(account.get_balance(), 500)
        
        result = account.withdraw(500)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 0)

    def test_series_of_failed_operations(self):
        """Test multiple failed operations in sequence"""
        account = BankAccount(100)
        
        results = [
            account.deposit(-10),
            account.deposit(0),
            account.withdraw(0),
            account.withdraw(-10),
            account.withdraw(200)
        ]
        
        # All should return False
        for result in results:
            self.assertFalse(result)
        
        # Balance should remain unchanged
        self.assertEqual(account.get_balance(), 100)

    def test_operation_after_zero_balance(self):
        """Test operations after reaching zero balance"""
        account = BankAccount(100)
        account.withdraw(100)
        
        self.assertEqual(account.get_balance(), 0)
        
        # Should be able to deposit
        result = account.deposit(50)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 50)
        
        # Should be able to withdraw again
        result = account.withdraw(50)
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 0)


if __name__ == '__main__':
    unittest.main()
