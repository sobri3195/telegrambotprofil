"""
Search parser module for identifying and parsing different search types.
"""
import re
from typing import List, Dict, Any
from enum import Enum


class SearchType(Enum):
    """Types of searches supported."""
    EMAIL = "email"
    PHONE = "phone"
    CAR_PLATE = "car_plate"
    CAR_VIN = "car_vin"
    IP_ADDRESS = "ip"
    COMBO = "combo"
    NAME = "name"
    UNKNOWN = "unknown"


class SearchParser:
    """Parser for identifying search queries."""
    
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|'
        r'\b[A-Za-z0-9._%+-]+@\b|'
        r'@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    PHONE_PATTERN = re.compile(
        r'\+?\d{7,15}\b'
    )
    
    IP_PATTERN = re.compile(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    )
    
    CAR_PLATE_PATTERN = re.compile(
        r'\b[A-Z]{1,2}\d{3,4}[A-Z]{1,2}\d{2,3}\b',
        re.IGNORECASE
    )
    
    CAR_VIN_PATTERN = re.compile(
        r'\b[A-HJ-NPR-Z0-9]{17}\b',
        re.IGNORECASE
    )
    
    @classmethod
    def parse_query(cls, query: str) -> Dict[str, Any]:
        """
        Parse a search query and identify its type.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with query type and parsed data
        """
        query = query.strip()
        
        if cls.EMAIL_PATTERN.fullmatch(query):
            return {
                'type': SearchType.EMAIL,
                'value': query,
                'subtype': cls._get_email_subtype(query)
            }
        
        if cls.IP_PATTERN.fullmatch(query):
            return {
                'type': SearchType.IP_ADDRESS,
                'value': query
            }
        
        if cls.CAR_VIN_PATTERN.fullmatch(query):
            return {
                'type': SearchType.CAR_VIN,
                'value': query
            }
        
        if cls.CAR_PLATE_PATTERN.fullmatch(query):
            return {
                'type': SearchType.CAR_PLATE,
                'value': query
            }
        
        if cls.PHONE_PATTERN.fullmatch(query):
            return {
                'type': SearchType.PHONE,
                'value': query
            }
        
        if cls._is_combo_search(query):
            return {
                'type': SearchType.COMBO,
                'value': query,
                'components': cls._parse_combo(query)
            }
        
        return {
            'type': SearchType.NAME,
            'value': query
        }
    
    @classmethod
    def parse_multi_query(cls, text: str) -> List[Dict[str, Any]]:
        """
        Parse multiple queries from text (one per line).
        
        Args:
            text: Text containing multiple queries
            
        Returns:
            List of parsed queries
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return [cls.parse_query(line) for line in lines]
    
    @classmethod
    def _get_email_subtype(cls, email: str) -> str:
        """Determine email search subtype."""
        if email.startswith('@'):
            return 'domain_only'
        elif email.endswith('@'):
            return 'name_only'
        else:
            return 'full'
    
    @classmethod
    def _is_combo_search(cls, query: str) -> bool:
        """Check if query is a combo search."""
        parts = query.split()
        if len(parts) < 2:
            return False
        
        has_name = any(part.isalpha() and len(part) > 2 for part in parts)
        has_identifier = any(
            cls.EMAIL_PATTERN.search(part) or
            cls.PHONE_PATTERN.search(part) or
            cls.IP_PATTERN.search(part) or
            part.count('/') == 2  # Date pattern
            for part in parts
        )
        
        return has_name and has_identifier
    
    @classmethod
    def _parse_combo(cls, query: str) -> Dict[str, Any]:
        """Parse combo search components."""
        components = {
            'name_parts': [],
            'identifiers': []
        }
        
        parts = query.split()
        
        for part in parts:
            if cls.EMAIL_PATTERN.search(part):
                components['identifiers'].append({'type': 'email', 'value': part})
            elif cls.PHONE_PATTERN.fullmatch(part):
                components['identifiers'].append({'type': 'phone', 'value': part})
            elif cls.IP_PATTERN.fullmatch(part):
                components['identifiers'].append({'type': 'ip', 'value': part})
            elif '/' in part and len(part.split('/')) == 3:
                components['identifiers'].append({'type': 'date', 'value': part})
            elif part.isalpha() and len(part) > 2:
                components['name_parts'].append(part)
        
        return components
