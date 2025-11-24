"""
Validation utilities for input data.
"""
import re
from typing import Optional


class Validators:
    """Input validation utilities."""
    
    @staticmethod
    def is_valid_file_size(file_size: int, max_size: int) -> bool:
        """
        Check if file size is within allowed limit.
        
        Args:
            file_size: File size in bytes
            max_size: Maximum allowed size in bytes
            
        Returns:
            True if valid, False otherwise
        """
        return 0 < file_size <= max_size
    
    @staticmethod
    def is_valid_extension(filename: str, allowed_extensions: list) -> bool:
        """
        Check if file extension is allowed.
        
        Args:
            filename: File name
            allowed_extensions: List of allowed extensions
            
        Returns:
            True if valid, False otherwise
        """
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in [ext.lower() for ext in allowed_extensions]
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4,}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize user input text.
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        text = text.strip()
        
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
