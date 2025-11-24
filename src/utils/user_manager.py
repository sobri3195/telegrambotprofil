"""
User manager module for handling user credits and profiles.
"""
from typing import Dict, Optional


class UserManager:
    """Manages user credits and profiles."""
    
    def __init__(self):
        """Initialize user manager with in-memory storage."""
        self._users: Dict[int, Dict] = {}
    
    def get_user(self, user_id: int) -> Dict:
        """
        Get user data or create new user with initial credits.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User data dictionary
        """
        from config import get_settings
        settings = get_settings()
        
        if user_id not in self._users:
            self._users[user_id] = {
                'user_id': user_id,
                'credits': settings.initial_credits,
                'is_new': True,
                'total_searches': 0,
            }
        else:
            self._users[user_id]['is_new'] = False
        
        return self._users[user_id]
    
    def get_credits(self, user_id: int) -> int:
        """
        Get user's current credit balance.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Credit balance
        """
        user = self.get_user(user_id)
        return user['credits']
    
    def deduct_credits(self, user_id: int, amount: int) -> bool:
        """
        Deduct credits from user account.
        
        Args:
            user_id: Telegram user ID
            amount: Number of credits to deduct
            
        Returns:
            True if successful, False if insufficient credits
        """
        user = self.get_user(user_id)
        
        if user['credits'] < amount:
            return False
        
        user['credits'] -= amount
        user['total_searches'] += 1
        return True
    
    def add_credits(self, user_id: int, amount: int) -> int:
        """
        Add credits to user account.
        
        Args:
            user_id: Telegram user ID
            amount: Number of credits to add
            
        Returns:
            New credit balance
        """
        user = self.get_user(user_id)
        user['credits'] += amount
        return user['credits']
    
    def has_sufficient_credits(self, user_id: int, required: int) -> bool:
        """
        Check if user has sufficient credits.
        
        Args:
            user_id: Telegram user ID
            required: Required number of credits
            
        Returns:
            True if user has enough credits
        """
        return self.get_credits(user_id) >= required


user_manager = UserManager()
