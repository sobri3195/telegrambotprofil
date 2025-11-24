"""
Tests for data parsing modules.
"""
import pytest
from src.parsers import DataExtractor, DocumentParser
from src.parsers.patterns import REGEX_PATTERNS, PASSWORD_HASH_PATTERNS


class TestDataExtractor:
    """Test DataExtractor functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.extractor = DataExtractor()
    
    def test_extract_emails(self):
        """Test email extraction."""
        text = "Contact: user@example.com or admin@test.org"
        emails = self.extractor.extract_emails(text)
        
        assert len(emails) == 2
        assert "user@example.com" in emails
        assert "admin@test.org" in emails
    
    def test_extract_phones(self):
        """Test phone number extraction."""
        text = "Call +62-812-3456-7890 or 021-1234567"
        phones = self.extractor.extract_phones(text)
        
        assert len(phones) >= 1
        assert any('+62' in phone for phone in phones)
    
    def test_extract_dates(self):
        """Test date extraction."""
        text = "Born: 1990-05-15 or 15/05/1990"
        dates = self.extractor.extract_dates(text)
        
        assert len(dates) >= 1
        assert any(d['value'] == '1990-05-15' for d in dates)
    
    def test_extract_password_hashes(self):
        """Test password hash detection."""
        text = """
        MD5: 5f4dcc3b5aa765d61d8327deb882cf99
        bcrypt: $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
        """
        hashes = self.extractor.extract_password_hashes(text)
        
        assert len(hashes) >= 2
        hash_types = [h['type'] for h in hashes]
        assert 'MD5' in hash_types
        assert 'bcrypt' in hash_types
    
    def test_extract_names(self):
        """Test name extraction."""
        text = "FullName: Maulana Muhammad Sobri"
        names = self.extractor.extract_names(text)
        
        assert len(names) >= 1
        assert any('Maulana' in name for name in names)
    
    def test_extract_telegram_info(self):
        """Test Telegram info extraction."""
        text = """
        User: @johndoe
        Channel: https://t.me/testchannel
        """
        telegram_info = self.extractor.extract_telegram_info(text)
        
        assert len(telegram_info['user_ids']) >= 1
        assert '@johndoe' in telegram_info['user_ids']
        assert len(telegram_info['channels']) >= 1
    
    def test_identify_sources(self):
        """Test data source identification."""
        text = "Data from Bhinneka breach and Civil Registry leak"
        sources = self.extractor.identify_sources(text)
        
        assert 'Bhinneka' in sources
        assert 'Civil Registry' in sources
    
    def test_extract_all(self):
        """Test comprehensive extraction."""
        text = """
        Name: John Doe Smith
        Email: john@example.com
        Phone: +1-555-123-4567
        Date: 1990-01-01
        Password: 5f4dcc3b5aa765d61d8327deb882cf99
        Source: Database Leak
        """
        result = self.extractor.extract_all(text)
        
        assert 'names' in result
        assert 'emails' in result
        assert 'phones' in result
        assert 'dates' in result
        assert 'passwords' in result
        assert 'sources' in result


class TestDocumentParser:
    """Test DocumentParser functionality."""
    
    def test_parse_text(self):
        """Test text file parsing."""
        content = b"This is test content"
        result = DocumentParser.parse_text(content)
        
        assert result == "This is test content"
    
    def test_parse_text_with_encoding(self):
        """Test text parsing with different encodings."""
        content = "Test content".encode('utf-8')
        result = DocumentParser.parse_text(content)
        
        assert "Test content" in result
    
    def test_invalid_extension(self):
        """Test handling of invalid extensions."""
        with pytest.raises(ValueError):
            DocumentParser.parse_document(b"content", "invalid")


class TestPatterns:
    """Test regex patterns."""
    
    def test_email_pattern(self):
        """Test email regex pattern."""
        pattern = REGEX_PATTERNS['email']
        
        assert pattern.search("test@example.com")
        assert pattern.search("user.name+tag@example.co.uk")
        assert not pattern.search("invalid.email")
    
    def test_phone_pattern(self):
        """Test phone regex pattern."""
        pattern = REGEX_PATTERNS['phone']
        
        assert pattern.search("+1-555-123-4567")
        assert pattern.search("(555) 123-4567")
        assert pattern.search("+628123456789")
    
    def test_date_patterns(self):
        """Test date regex patterns."""
        iso_pattern = REGEX_PATTERNS['date_iso']
        dmy_pattern = REGEX_PATTERNS['date_dmy']
        
        assert iso_pattern.search("2024-01-15")
        assert dmy_pattern.search("15/01/2024")
        assert dmy_pattern.search("15-01-2024")
    
    def test_password_hash_patterns(self):
        """Test password hash detection patterns."""
        md5_pattern = PASSWORD_HASH_PATTERNS['md5']['pattern']
        bcrypt_pattern = PASSWORD_HASH_PATTERNS['bcrypt']['pattern']
        
        assert md5_pattern.search("5f4dcc3b5aa765d61d8327deb882cf99")
        assert bcrypt_pattern.search("$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy")
