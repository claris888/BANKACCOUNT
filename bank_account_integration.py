# BankAccount class with NotificationSystem integration
class NotificationSystem:
    """Simulates a notification system for bank account operations"""
    
    def __init__(self):
        self.notifications = []
    
    def send_notification(self, message, notification_type='info'):
        """Send a notification for an account operation"""
        notification = {
            'message': message,
            'type': notification_type,
            'timestamp': None
        }
        self.notifications.append(notification)
        return True
    
    def get_notifications(self):
        """Get all notifications"""
        return self.notifications
    
    def clear_notifications(self):
        """Clear all notifications"""
        self.notifications = []


class BankAccount:
    """BankAccount class with NotificationSystem integration"""
    
    def __init__(self, initial_balance=0, notification_system=None):
        self.balance = initial_balance
        self.notification_system = notification_system
        self.transaction_history = []
    
    def deposit(self, amount):
        """Deposit money into the account and notify"""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append({
                'type': 'deposit',
                'amount': amount,
                'balance_after': self.balance
            })
            
            # Send notification if notification system is available
            if self.notification_system:
                message = f"Deposit of ${amount:.2f} successful. New balance: ${self.balance:.2f}"
                self.notification_system.send_notification(message, 'deposit')
            
            return True
        return False
    
    def withdraw(self, amount):
        """Withdraw money from the account and notify"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append({
                'type': 'withdrawal',
                'amount': amount,
                'balance_after': self.balance
            })
            
            # Send notification if notification system is available
            if self.notification_system:
                message = f"Withdrawal of ${amount:.2f} successful. New balance: ${self.balance:.2f}"
                self.notification_system.send_notification(message, 'withdrawal')
            
            return True
        return False
    
    def get_balance(self):
        """Get the current account balance"""
        return self.balance
    
    def get_transaction_history(self):
        """Get the transaction history"""
        return self.transaction_history
    
    def set_notification_system(self, notification_system):
        """Set or update the notification system"""
        self.notification_system = notification_system
