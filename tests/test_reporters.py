"""
Tests for report generation modules.
"""
import pytest
from src.reporters import ReportGenerator, DataMasker


class TestDataMasker:
    """Test DataMasker functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.masker = DataMasker()
    
    def test_mask_name_full(self):
        """Test full name masking."""
        result = self.masker.mask_name("Maulana Muhammad Sobri")
        
        assert result.startswith("Maulana")
        assert "M." in result
        assert "S." in result
        assert "Muhammad" not in result or result == "Maulana M. S."
    
    def test_mask_name_single(self):
        """Test single name."""
        result = self.masker.mask_name("John")
        
        assert result == "John"
    
    def test_mask_name_empty(self):
        """Test empty name."""
        result = self.masker.mask_name("")
        
        assert result == "[Unknown]"
    
    def test_mask_email(self):
        """Test email masking."""
        result = self.masker.mask_email("user@example.com")
        
        assert result.startswith("u")
        assert "@example.com" in result
        assert "*" in result
    
    def test_mask_phone(self):
        """Test phone number masking."""
        result = self.masker.mask_phone("+628123456789")
        
        assert result.startswith("+62")
        assert "*" in result
        assert result.endswith("789")
    
    def test_mask_address(self):
        """Test address masking."""
        address = {'city': 'Jakarta', 'postal_code': '12345'}
        result = self.masker.mask_address(address)
        
        assert "Jakarta" in result
        assert "Indonesia" in result
        assert "12345" not in result
    
    def test_mask_passport(self):
        """Test passport masking."""
        result = self.masker.mask_passport("A1234567")
        
        assert result.startswith("A1")
        assert result.endswith("67")
        assert "*" in result
    
    def test_mask_sensitive_value(self):
        """Test generic sensitive value masking."""
        result = self.masker.mask_sensitive_value("SecretValue123", show_chars=2)
        
        assert result.startswith("Se")
        assert result.endswith("23")
        assert "*" in result
    
    def test_mask_list(self):
        """Test list masking."""
        items = ["email1@test.com", "email2@test.com", "email3@test.com", "email4@test.com"]
        result = self.masker.mask_list(items, self.masker.mask_email, max_show=2)
        
        assert len(result) == 3
        assert "and 2 more" in result[-1]


class TestReportGenerator:
    """Test ReportGenerator functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.generator = ReportGenerator()
    
    def create_sample_data(self):
        """Create sample data for testing."""
        extracted_data = {
            'names': ['John Doe Smith'],
            'emails': ['john@example.com', 'john.doe@test.com'],
            'phones': ['+1-555-123-4567', '+1-555-987-6543'],
            'dates': [{'value': '1990-01-01', 'format': 'YYYY-MM-DD'}],
            'addresses': [{'city': 'Jakarta', 'postal_code': '12345'}],
            'passwords': [
                {'type': 'MD5', 'risk': 'HIGH', 'value': '5f4dcc...'},
                {'type': 'bcrypt', 'risk': 'LOW', 'value': '$2a$10...'},
            ],
            'sensitive_data': [
                {'type': 'passport', 'value': 'A1234567', 'context': 'test'}
            ],
            'telegram_info': {
                'user_ids': ['@johndoe'],
                'channels': ['tech_channel', 'news_channel'],
                'urls': ['https://t.me/tech_channel'],
            },
            'sources': ['Bhinneka', 'Civil Registry', 'Telegram'],
        }
        
        risk_assessment = {
            'risk_level': 'HIGH',
            'risk_score': 25,
            'findings': [
                {
                    'category': 'Password Security',
                    'severity': 'HIGH',
                    'description': 'Weak password hash detected: MD5',
                    'detail': 'MD5 is cryptographically weak'
                },
                {
                    'category': 'Sensitive Data Exposure',
                    'severity': 'HIGH',
                    'description': 'Passport number exposed',
                    'detail': 'Critical identity data'
                },
            ],
            'recommendations': [
                '🔐 Segera ganti password di platform dengan hash MD5',
                '🛡️ Monitor identitas Anda',
                '🔑 Aktifkan 2FA di semua akun',
            ],
        }
        
        consistency_check = {
            'has_inconsistencies': True,
            'inconsistency_count': 2,
            'inconsistencies': [
                {
                    'type': 'Email Inconsistency',
                    'severity': 'MEDIUM',
                    'description': 'Found 2 different email addresses',
                    'details': 'Multiple emails detected',
                },
            ],
            'consistency_score': 85.0,
        }
        
        behavior_analysis = {
            'channel_analysis': {
                'total_channels': 2,
                'categories': {'technology': 1, 'news': 1},
                'top_category': 'technology',
            },
            'anomalies': [],
            'user_profile': {
                'primary_interest': 'Technology',
                'activity_level': 'Low',
                'data_richness': 'Rich',
            },
            'behavior_score': 100.0,
        }
        
        return extracted_data, risk_assessment, consistency_check, behavior_analysis
    
    def test_generate_header(self):
        """Test header generation."""
        extracted_data, risk_assessment, _, _ = self.create_sample_data()
        
        header = self.generator._generate_header(extracted_data, risk_assessment)
        
        assert "DATA BREACH ANALYSIS REPORT" in header
        assert "HIGH RISK" in header
        assert "🔴" in header
    
    def test_generate_personal_data_section(self):
        """Test personal data section generation."""
        extracted_data, _, _, _ = self.create_sample_data()
        
        section = self.generator._generate_personal_data_section(extracted_data)
        
        assert "Data Pribadi" in section
        assert "Nama" in section
        assert "Email" in section
        assert "Telepon" in section
        assert "Alamat" in section
        assert "*" in section
    
    def test_generate_data_sources_section(self):
        """Test data sources section generation."""
        extracted_data, risk_assessment, _, _ = self.create_sample_data()
        
        section = self.generator._generate_data_sources_section(
            extracted_data, risk_assessment
        )
        
        assert "Sumber Data" in section
        assert "Risiko" in section
        assert "|" in section
    
    def test_generate_findings_section(self):
        """Test findings section generation."""
        _, risk_assessment, consistency_check, behavior_analysis = self.create_sample_data()
        
        section = self.generator._generate_findings_section(
            risk_assessment, consistency_check, behavior_analysis
        )
        
        assert "Temuan Kritis" in section
        assert "Password Security" in section or "Weak password" in section
    
    def test_generate_recommendations_section(self):
        """Test recommendations section generation."""
        _, risk_assessment, _, _ = self.create_sample_data()
        
        section = self.generator._generate_recommendations_section(risk_assessment)
        
        assert "Rekomendasi" in section
        assert any(char in section for char in ['🔐', '🛡️', '🔑'])
    
    def test_generate_full_report(self):
        """Test full report generation."""
        extracted_data, risk_assessment, consistency_check, behavior_analysis = self.create_sample_data()
        
        report = self.generator.generate_full_report(
            extracted_data,
            risk_assessment,
            consistency_check,
            behavior_analysis
        )
        
        assert "DATA BREACH ANALYSIS REPORT" in report
        assert "Data Pribadi" in report
        assert "Sumber Data" in report
        assert "Temuan Kritis" in report
        assert "Rekomendasi" in report
        assert "Disclaimer" in report
        assert isinstance(report, str)
        assert len(report) > 100
