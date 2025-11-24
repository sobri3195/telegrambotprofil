"""
Regex patterns and detection rules for data extraction.
"""
import re
from typing import Dict, Pattern

REGEX_PATTERNS: Dict[str, Pattern] = {
    'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    'phone': re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4,}'),
    'date_iso': re.compile(r'\b\d{4}-\d{2}-\d{2}\b'),
    'date_dmy': re.compile(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b'),
    'passport': re.compile(r'\b[A-Z0-9]{6,9}\b'),
    'telegram_id': re.compile(r'@[a-zA-Z0-9_]{5,32}'),
    'url': re.compile(r'https?://[^\s]+'),
    'postal_code': re.compile(r'\b\d{5}(?:-\d{4})?\b'),
}

PASSWORD_HASH_PATTERNS: Dict[str, Dict] = {
    'md5': {
        'pattern': re.compile(r'\b[a-f0-9]{32}\b', re.IGNORECASE),
        'length': 32,
        'risk': 'HIGH',
        'name': 'MD5'
    },
    'sha1': {
        'pattern': re.compile(r'\b[a-f0-9]{40}\b', re.IGNORECASE),
        'length': 40,
        'risk': 'HIGH',
        'name': 'SHA-1'
    },
    'sha256': {
        'pattern': re.compile(r'\b[a-f0-9]{64}\b', re.IGNORECASE),
        'length': 64,
        'risk': 'MEDIUM',
        'name': 'SHA-256'
    },
    'bcrypt': {
        'pattern': re.compile(r'\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}'),
        'length': 60,
        'risk': 'LOW',
        'name': 'bcrypt'
    },
    'argon2': {
        'pattern': re.compile(r'\$argon2i?d?\$v=\d+\$m=\d+,t=\d+,p=\d+\$[A-Za-z0-9+/]+\$[A-Za-z0-9+/]+'),
        'length': None,
        'risk': 'LOW',
        'name': 'Argon2'
    },
}

ADDRESS_KEYWORDS = [
    'address', 'alamat', 'street', 'jalan', 'city', 'kota',
    'region', 'provinsi', 'province', 'postcode', 'postal', 'zip'
]

NAME_PATTERNS = [
    re.compile(r'(?:FullName|Name|Nama):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', re.IGNORECASE),
    re.compile(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'),
]

SENSITIVE_DATA_KEYWORDS = [
    'passport', 'paspor', 'identity', 'ktp', 'driver license', 'sim',
    'social security', 'credit card', 'kartu kredit', 'bank account'
]
