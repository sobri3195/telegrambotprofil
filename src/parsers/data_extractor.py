"""
Data extraction module for identifying and extracting structured data from text.
"""
import re
from typing import Dict, List, Any, Set
from .patterns import (
    REGEX_PATTERNS,
    PASSWORD_HASH_PATTERNS,
    ADDRESS_KEYWORDS,
    NAME_PATTERNS,
    SENSITIVE_DATA_KEYWORDS
)


class DataExtractor:
    """Extract structured data from unstructured text using patterns and rules."""
    
    def extract_all(self, text: str) -> Dict[str, Any]:
        """
        Extract all data types from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing extracted data by category
        """
        return {
            'names': self.extract_names(text),
            'emails': self.extract_emails(text),
            'phones': self.extract_phones(text),
            'dates': self.extract_dates(text),
            'addresses': self.extract_addresses(text),
            'passwords': self.extract_password_hashes(text),
            'sensitive_data': self.extract_sensitive_data(text),
            'telegram_info': self.extract_telegram_info(text),
            'sources': self.identify_sources(text),
        }
    
    def extract_names(self, text: str) -> List[str]:
        """Extract full names from text."""
        names: Set[str] = set()
        
        for pattern in NAME_PATTERNS:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match and len(match.split()) >= 2:
                    names.add(match.strip())
        
        return list(names)
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        matches = REGEX_PATTERNS['email'].findall(text)
        return list(set(matches))
    
    def extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        matches = REGEX_PATTERNS['phone'].findall(text)
        cleaned = []
        for phone in matches:
            phone_clean = re.sub(r'[^\d+]', '', phone)
            if len(phone_clean) >= 10:
                cleaned.append(phone)
        return list(set(cleaned))
    
    def extract_dates(self, text: str) -> List[Dict[str, str]]:
        """Extract dates in various formats."""
        dates = []
        
        iso_dates = REGEX_PATTERNS['date_iso'].findall(text)
        for date in iso_dates:
            dates.append({'value': date, 'format': 'YYYY-MM-DD'})
        
        dmy_dates = REGEX_PATTERNS['date_dmy'].findall(text)
        for date in dmy_dates:
            dates.append({'value': date, 'format': 'DD/MM/YYYY'})
        
        return dates
    
    def extract_addresses(self, text: str) -> List[Dict[str, Any]]:
        """Extract address information from text."""
        addresses = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ADDRESS_KEYWORDS):
                address_text = line
                if i + 1 < len(lines):
                    address_text += ' ' + lines[i + 1]
                
                address_info = {
                    'full_text': address_text.strip(),
                    'city': self._extract_city(address_text),
                    'postal_code': self._extract_postal_code(address_text),
                }
                addresses.append(address_info)
        
        return addresses
    
    def _extract_city(self, text: str) -> str:
        """Extract city name from address text."""
        city_pattern = re.compile(r'(?:City|Kota):\s*([A-Za-z\s]+)', re.IGNORECASE)
        match = city_pattern.search(text)
        return match.group(1).strip() if match else ''
    
    def _extract_postal_code(self, text: str) -> str:
        """Extract postal code from address text."""
        match = REGEX_PATTERNS['postal_code'].search(text)
        return match.group(0) if match else ''
    
    def extract_password_hashes(self, text: str) -> List[Dict[str, Any]]:
        """Extract and identify password hashes."""
        hashes = []
        
        for hash_type, hash_info in PASSWORD_HASH_PATTERNS.items():
            matches = hash_info['pattern'].findall(text)
            for match in matches:
                hashes.append({
                    'value': match[:20] + '...' if len(match) > 20 else match,
                    'type': hash_info['name'],
                    'risk': hash_info['risk'],
                    'full_length': len(match),
                })
        
        return hashes
    
    def extract_sensitive_data(self, text: str) -> List[Dict[str, str]]:
        """Extract sensitive data mentions."""
        sensitive_items = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            for keyword in SENSITIVE_DATA_KEYWORDS:
                if keyword in line_lower:
                    passport_match = REGEX_PATTERNS['passport'].search(line)
                    if passport_match:
                        sensitive_items.append({
                            'type': keyword.title(),
                            'value': passport_match.group(0),
                            'context': line.strip()[:100],
                        })
        
        return sensitive_items
    
    def extract_telegram_info(self, text: str) -> Dict[str, Any]:
        """Extract Telegram-related information."""
        telegram_ids = REGEX_PATTERNS['telegram_id'].findall(text)
        telegram_urls = [url for url in REGEX_PATTERNS['url'].findall(text) if 't.me' in url]
        
        channels = []
        for url in telegram_urls:
            channel_match = re.search(r't\.me/([a-zA-Z0-9_]+)', url)
            if channel_match:
                channels.append(channel_match.group(1))
        
        return {
            'user_ids': list(set(telegram_ids)),
            'channels': list(set(channels)),
            'urls': telegram_urls,
        }
    
    def identify_sources(self, text: str) -> List[str]:
        """Identify data breach sources mentioned in text."""
        sources = []
        common_sources = [
            'Bhinneka', 'Civil Registry', 'Telegram', 'LinkedIn',
            'Facebook', 'Twitter', 'Instagram', 'SlideTeam',
            'Database', 'API', 'Breach', 'Leak'
        ]
        
        text_lower = text.lower()
        for source in common_sources:
            if source.lower() in text_lower:
                sources.append(source)
        
        return list(set(sources))
