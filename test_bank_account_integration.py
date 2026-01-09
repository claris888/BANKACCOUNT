import unittest
from unittest.mock import Mock, MagicMock, call, patch
import sys
import os

# Add the parent directory to the path so we can import the BankAccount class
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bank_account_integration import BankAccount, NotificationSystem


class TestBankAccountDepositWithMockNotification(unittest.TestCase):
    """Integration tests for deposit function with mocked NotificationSystem"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_notification_system = Mock(spec=NotificationSystem)
        self.account = BankAccount(100, self.mock_notification_system)

    def test_deposit_calls_notification_system(self):
        """Test that deposit calls notification system with correct message"""
        self.account.deposit(50)
        
        # Verify that send_notification was called
        self.mock_notification_system.send_notification.assert_called_once()

    def test_deposit_notification_message_format(self):
        """Test that deposit sends notification with correct message format"""
        self.account.deposit(50)
        
        # Get the call arguments
        call_args = self.mock_notification_system.send_notification.call_args
        message = call_args[0][0]  # First positional argument
        
        # Verify message contains deposit amount and new balance
        self.assertIn('50.00', message)
        self.assertIn('150.00', message)
        self.assertIn('Deposit', message)

    def test_deposit_notification_type_parameter(self):
        """Test that deposit sends notification with correct type"""
        self.account.deposit(50)
        
        # Verify the notification type
        call_args = self.mock_notification_system.send_notification.call_args
        notification_type = call_args[0][1]  # Second positional argument
        
        self.assertEqual(notification_type, 'deposit')

    def test_deposit_calls_notification_with_correct_keyword_args(self):
        """Test deposit calls notification with correct keyword arguments"""
        self.account.deposit(75.50)
        
        # Verify send_notification was called with expected arguments
        self.mock_notification_system.send_notification.assert_called_once()
        call_args, call_kwargs = self.mock_notification_system.send_notification.call_args
        
        # Check that it was called with positional args and correct type
        self.assertEqual(len(call_args), 2)
        self.assertEqual(call_args[1], 'deposit')

    def test_deposit_notification_not_called_for_zero_amount(self):
        """Test that notification is not called when deposit amount is zero"""
        self.account.deposit(0)
        
        # Verify send_notification was NOT called
        self.mock_notification_system.send_notification.assert_not_called()

    def test_deposit_notification_not_called_for_negative_amount(self):
        """Test that notification is not called when deposit amount is negative"""
        self.account.deposit(-50)
        
        # Verify send_notification was NOT called
        self.mock_notification_system.send_notification.assert_not_called()

    def test_deposit_returns_true_and_calls_notification(self):
        """Test that successful deposit returns True and calls notification"""
        result = self.account.deposit(25)
        
        self.assertTrue(result)
        self.mock_notification_system.send_notification.assert_called_once()

    def test_deposit_returns_false_and_no_notification_call(self):
        """Test that failed deposit returns False and doesn't call notification"""
        result = self.account.deposit(-100)
        
        self.assertFalse(result)
        self.mock_notification_system.send_notification.assert_not_called()

    def test_multiple_deposits_call_notification_multiple_times(self):
        """Test that multiple deposits trigger notification each time"""
        self.account.deposit(50)
        self.account.deposit(25)
        self.account.deposit(75)
        
        # Verify notification was called 3 times
        self.assertEqual(self.mock_notification_system.send_notification.call_count, 3)

    def test_deposit_notification_messages_are_different(self):
        """Test that different deposits have different notification messages"""
        self.account.deposit(50)
        self.account.deposit(30)
        
        # Get all calls
        calls = self.mock_notification_system.send_notification.call_args_list
        
        message1 = calls[0][0][0]
        message2 = calls[1][0][0]
        
        # Messages should be different
        self.assertNotEqual(message1, message2)
        
        # Check each message
        self.assertIn('50.00', message1)
        self.assertIn('150.00', message1)
        self.assertIn('30.00', message2)
        self.assertIn('180.00', message2)

    def test_deposit_with_notification_system_mock_spy(self):
        """Test deposit using mock as a spy to track calls"""
        mock_notif = Mock(return_value=True)
        account = BankAccount(100)
        account.notification_system = Mock()
        account.notification_system.send_notification = mock_notif
        
        account.deposit(50)
        
        # Verify the mock was called
        self.assertEqual(mock_notif.call_count, 1)
        args, kwargs = mock_notif.call_args
        self.assertIn('50', args[0])


class TestBankAccountDepositWithRealNotificationSystem(unittest.TestCase):
    """Integration tests using real NotificationSystem"""

    def setUp(self):
        """Set up test fixtures with real notification system"""
        self.notification_system = NotificationSystem()
        self.account = BankAccount(100, self.notification_system)

    def test_deposit_creates_notification(self):
        """Test that deposit creates an actual notification"""
        self.account.deposit(50)
        
        notifications = self.notification_system.get_notifications()
        self.assertEqual(len(notifications), 1)

    def test_deposit_notification_content(self):
        """Test the actual notification content"""
        self.account.deposit(50)
        
        notifications = self.notification_system.get_notifications()
        notification = notifications[0]
        
        self.assertIn('50', notification['message'])
        self.assertIn('150', notification['message'])
        self.assertEqual(notification['type'], 'deposit')

    def test_multiple_deposits_create_multiple_notifications(self):
        """Test that multiple deposits create multiple notifications"""
        self.account.deposit(50)
        self.account.deposit(25)
        self.account.deposit(75)
        
        notifications = self.notification_system.get_notifications()
        self.assertEqual(len(notifications), 3)

    def test_failed_deposit_no_notification(self):
        """Test that failed deposits don't create notifications"""
        self.account.deposit(0)
        self.account.deposit(-50)
        
        notifications = self.notification_system.get_notifications()
        self.assertEqual(len(notifications), 0)

    def test_mixed_successful_and_failed_deposits(self):
        """Test notifications only for successful deposits"""
        self.account.deposit(50)    # Success
        self.account.deposit(-20)   # Fail
        self.account.deposit(30)    # Success
        self.account.deposit(0)     # Fail
        self.account.deposit(25)    # Success
        
        notifications = self.notification_system.get_notifications()
        self.assertEqual(len(notifications), 3)

    def test_notification_sequence(self):
        """Test the sequence of notifications"""
        self.account.deposit(50)
        self.account.deposit(100)
        
        notifications = self.notification_system.get_notifications()
        
        # First notification should show balance 150
        self.assertIn('150', notifications[0]['message'])
        # Second notification should show balance 250
        self.assertIn('250', notifications[1]['message'])


class TestBankAccountDepositWithMagicMock(unittest.TestCase):
    """Integration tests using MagicMock for advanced mocking scenarios"""

    def test_deposit_with_magic_mock_notification(self):
        """Test deposit with MagicMock"""
        magic_mock = MagicMock()
        account = BankAccount(100, magic_mock)
        
        account.deposit(50)
        
        magic_mock.send_notification.assert_called_once()

    def test_deposit_notification_call_sequence(self):
        """Test the call sequence of notifications"""
        mock_notif = MagicMock()
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        account.deposit(25)
        
        # Check call count
        self.assertEqual(mock_notif.send_notification.call_count, 2)
        
        # Check the specific calls using call objects
        expected_calls = [
            call('Deposit of $50.00 successful. New balance: $150.00', 'deposit'),
            call('Deposit of $25.00 successful. New balance: $175.00', 'deposit')
        ]
        mock_notif.send_notification.assert_has_calls(expected_calls)

    def test_deposit_with_mock_that_tracks_arguments(self):
        """Test that mock tracks all arguments passed to notification"""
        mock_notif = MagicMock()
        account = BankAccount(200, mock_notif)
        
        account.deposit(100)
        
        # Get the call arguments
        call_args, call_kwargs = mock_notif.send_notification.call_args
        
        self.assertEqual(len(call_args), 2)
        self.assertIn('100', call_args[0])
        self.assertEqual(call_args[1], 'deposit')


class TestBankAccountDepositWithPatch(unittest.TestCase):
    """Integration tests using patch decorator"""

    @patch('bank_account_integration.NotificationSystem')
    def test_deposit_with_patched_notification_system(self, mock_notif_class):
        """Test deposit with patched NotificationSystem class"""
        mock_instance = MagicMock()
        mock_notif_class.return_value = mock_instance
        
        # Create account with mocked notification system
        account = BankAccount(100, mock_instance)
        account.deposit(50)
        
        # Verify the notification was called
        mock_instance.send_notification.assert_called_once()

    def test_deposit_with_side_effect_mock(self):
        """Test deposit with mock that has side effects"""
        mock_notif = MagicMock()
        # Set a side effect that returns True
        mock_notif.send_notification.side_effect = [True, True, False]
        
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        account.deposit(25)
        
        self.assertEqual(mock_notif.send_notification.call_count, 2)

    def test_deposit_notification_called_before_balance_update(self):
        """Test interaction between deposit and notification"""
        mock_notif = MagicMock()
        account = BankAccount(100, mock_notif)
        
        # Deposit amount
        account.deposit(50)
        
        # Get the balance from the call argument
        call_args = mock_notif.send_notification.call_args[0]
        message = call_args[0]
        
        # Verify the message contains the new balance
        self.assertIn('150', message)
        self.assertEqual(account.get_balance(), 150)


class TestDepositTransactionHistory(unittest.TestCase):
    """Integration tests for deposit and transaction history"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_notification_system = Mock(spec=NotificationSystem)
        self.account = BankAccount(100, self.mock_notification_system)

    def test_deposit_records_transaction(self):
        """Test that deposit records transaction in history"""
        self.account.deposit(50)
        
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['type'], 'deposit')
        self.assertEqual(history[0]['amount'], 50)
        self.assertEqual(history[0]['balance_after'], 150)

    def test_multiple_deposits_recorded_in_order(self):
        """Test that multiple deposits are recorded in order"""
        self.account.deposit(50)
        self.account.deposit(25)
        self.account.deposit(75)
        
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 3)
        
        self.assertEqual(history[0]['amount'], 50)
        self.assertEqual(history[0]['balance_after'], 150)
        
        self.assertEqual(history[1]['amount'], 25)
        self.assertEqual(history[1]['balance_after'], 175)
        
        self.assertEqual(history[2]['amount'], 75)
        self.assertEqual(history[2]['balance_after'], 250)

    def test_failed_deposit_not_in_history(self):
        """Test that failed deposits are not recorded in history"""
        self.account.deposit(50)
        self.account.deposit(-20)
        self.account.deposit(30)
        
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 2)


class TestDepositNotificationIntegration(unittest.TestCase):
    """Integration tests combining deposit, notification, and history"""

    def test_deposit_notification_and_history_synchronized(self):
        """Test that notification and history are synchronized"""
        notification_system = NotificationSystem()
        account = BankAccount(100, notification_system)
        
        account.deposit(50)
        account.deposit(25)
        
        history = account.get_transaction_history()
        notifications = notification_system.get_notifications()
        
        # Should have same number of entries
        self.assertEqual(len(history), len(notifications))
        
        # Check values match
        self.assertEqual(history[0]['amount'], 50)
        self.assertIn('50', notifications[0]['message'])
        
        self.assertEqual(history[1]['amount'], 25)
        self.assertIn('25', notifications[1]['message'])

    def test_deposit_without_notification_system(self):
        """Test that deposit works without notification system"""
        account = BankAccount(100, None)
        
        result = account.deposit(50)
        
        self.assertTrue(result)
        self.assertEqual(account.get_balance(), 150)
        
        history = account.get_transaction_history()
        self.assertEqual(len(history), 1)

    def test_set_notification_system_after_creation(self):
        """Test setting notification system after account creation"""
        account = BankAccount(100)
        
        # First deposit without notification system
        account.deposit(50)
        
        # Set notification system
        mock_notif = Mock(spec=NotificationSystem)
        account.set_notification_system(mock_notif)
        
        # Second deposit with notification system
        account.deposit(25)
        
        # Only second deposit should trigger notification
        mock_notif.send_notification.assert_called_once()
        
        # Both deposits should be in history
        history = account.get_transaction_history()
        self.assertEqual(len(history), 2)


class TestDepositNotificationAssertions(unittest.TestCase):
    """Test various assertion methods on mock notifications"""

    def test_deposit_assert_called_with_exact_message(self):
        """Test assertion of exact message format"""
        mock_notif = Mock(spec=NotificationSystem)
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        
        mock_notif.send_notification.assert_called_with(
            'Deposit of $50.00 successful. New balance: $150.00',
            'deposit'
        )

    def test_deposit_assert_called_once(self):
        """Test that notification is called exactly once"""
        mock_notif = Mock(spec=NotificationSystem)
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        
        mock_notif.send_notification.assert_called_once()
        mock_notif.send_notification.assert_called_once_with(
            'Deposit of $50.00 successful. New balance: $150.00',
            'deposit'
        )

    def test_deposit_call_count_verification(self):
        """Test verification of call count"""
        mock_notif = Mock(spec=NotificationSystem)
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        account.deposit(25)
        account.deposit(75)
        
        self.assertEqual(mock_notif.send_notification.call_count, 3)

    def test_deposit_reset_mock(self):
        """Test resetting mock between operations"""
        mock_notif = Mock(spec=NotificationSystem)
        account = BankAccount(100, mock_notif)
        
        account.deposit(50)
        self.assertEqual(mock_notif.send_notification.call_count, 1)
        
        # Reset the mock
        mock_notif.reset_mock()
        self.assertEqual(mock_notif.send_notification.call_count, 0)
        
        account.deposit(25)
        self.assertEqual(mock_notif.send_notification.call_count, 1)


if __name__ == '__main__':
    unittest.main()
