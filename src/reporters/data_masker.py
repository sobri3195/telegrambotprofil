"""
Data masking module for protecting PII in reports.
"""
import re
from typing import List, Dict, Any


class DataMasker:
    """Mask sensitive personal information for privacy protection."""
    
    @staticmethod
    def mask_name(name: str) -> str:
        """
        Mask full name showing only first name and last initial.
        
        Example: "Maulana Muhammad Sobri" -> "Maulana M. S."
        """
        if not name:
            return "[Unknown]"
        
        parts = name.split()
        if len(parts) == 1:
            return parts[0]
        
        masked_parts = [parts[0]]
        for part in parts[1:]:
            if part:
                masked_parts.append(part[0] + '.')
        
        return ' '.join(masked_parts)
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email address.
        
        Example: "user@example.com" -> "u***@example.com"
        """
        if not email or '@' not in email:
            return "[Hidden]"
        
        local, domain = email.split('@', 1)
        
        if len(local) <= 2:
            masked_local = local[0] + '*'
        else:
            masked_local = local[0] + '*' * (len(local) - 1)
        
        return f"{masked_local}@{domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        Mask phone number.
        
        Example: "+628123456789" -> "+62*****789"
        """
        if not phone:
            return "[Hidden]"
        
        digits_only = re.sub(r'\D', '', phone)
        
        if len(digits_only) < 4:
            return '*' * len(phone)
        
        if phone.startswith('+'):
            country_code = re.match(r'\+\d{1,3}', phone)
            if country_code:
                cc = country_code.group(0)
                suffix = digits_only[-3:]
                stars = '*' * (len(digits_only) - len(cc) - 2)
                return f"{cc}{stars}{suffix}"
        
        suffix = digits_only[-3:]
        stars = '*' * (len(digits_only) - 3)
        return f"{stars}{suffix}"
    
    @staticmethod
    def mask_address(address: Dict[str, Any]) -> str:
        """
        Mask address showing only city and country.
        
        Example: {"city": "Jakarta", ...} -> "Jakarta, Indonesia"
        """
        city = address.get('city', 'Unknown City')
        return f"{city}, Indonesia"
    
    @staticmethod
    def mask_passport(passport: str) -> str:
        """
        Mask passport number.
        
        Example: "A1234567" -> "A1****67"
        """
        if not passport or len(passport) < 4:
            return '*' * len(passport) if passport else "[Hidden]"
        
        return passport[:2] + '*' * (len(passport) - 4) + passport[-2:]
    
    @staticmethod
    def mask_sensitive_value(value: str, show_chars: int = 2) -> str:
        """
        Generic masking for sensitive values.
        
        Args:
            value: Value to mask
            show_chars: Number of characters to show at start and end
        """
        if not value or len(value) <= show_chars * 2:
            return '*' * len(value) if value else "[Hidden]"
        
        return value[:show_chars] + '*' * (len(value) - show_chars * 2) + value[-show_chars:]
    
    @staticmethod
    def mask_list(items: List[str], masker_func, max_show: int = 3) -> List[str]:
        """
        Mask a list of items using specified masker function.
        
        Args:
            items: List of items to mask
            masker_func: Function to use for masking
            max_show: Maximum number of items to show
        """
        masked = [masker_func(item) for item in items[:max_show]]
        
        if len(items) > max_show:
            masked.append(f"... and {len(items) - max_show} more")
        
        return masked
