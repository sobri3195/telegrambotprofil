"""
Tests for data analysis modules.
"""
import pytest
from src.analyzers import RiskAssessor, ConsistencyChecker, BehaviorAnalyzer


class TestRiskAssessor:
    """Test RiskAssessor functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.assessor = RiskAssessor()
    
    def test_assess_password_risk_high(self):
        """Test high risk password assessment."""
        passwords = [
            {'type': 'MD5', 'risk': 'HIGH', 'value': 'abc...'}
        ]
        risk_score, findings = self.assessor._assess_password_risk(passwords)
        
        assert risk_score > 0
        assert len(findings) > 0
        assert any(f['severity'] == 'HIGH' for f in findings)
    
    def test_assess_password_risk_low(self):
        """Test low risk password assessment."""
        passwords = [
            {'type': 'bcrypt', 'risk': 'LOW', 'value': 'abc...'}
        ]
        risk_score, findings = self.assessor._assess_password_risk(passwords)
        
        assert risk_score >= 0
    
    def test_assess_sensitive_data_risk(self):
        """Test sensitive data risk assessment."""
        sensitive_data = [
            {'type': 'passport', 'value': 'A1234567', 'context': 'test'}
        ]
        risk_score, findings = self.assessor._assess_sensitive_data_risk(sensitive_data)
        
        assert risk_score > 0
        assert len(findings) > 0
    
    def test_calculate_risk_level(self):
        """Test risk level calculation."""
        assert self.assessor._calculate_risk_level(20) == 'HIGH'
        assert self.assessor._calculate_risk_level(10) == 'MEDIUM'
        assert self.assessor._calculate_risk_level(5) == 'LOW'
    
    def test_assess_overall_risk(self):
        """Test overall risk assessment."""
        extracted_data = {
            'emails': ['test@example.com', 'user@test.com'],
            'phones': ['+1234567890'],
            'passwords': [{'type': 'MD5', 'risk': 'HIGH'}],
            'addresses': [{'city': 'Jakarta'}],
            'sensitive_data': [{'type': 'passport', 'value': 'A1234567'}],
        }
        
        result = self.assessor.assess_overall_risk(extracted_data)
        
        assert 'risk_level' in result
        assert 'risk_score' in result
        assert 'findings' in result
        assert 'recommendations' in result
        assert result['risk_level'] in ['HIGH', 'MEDIUM', 'LOW']
    
    def test_generate_recommendations(self):
        """Test recommendation generation."""
        findings = [
            {'category': 'Password Security', 'severity': 'HIGH'},
            {'category': 'Sensitive Data Exposure', 'severity': 'HIGH'},
        ]
        
        recommendations = self.assessor._generate_recommendations(findings)
        
        assert len(recommendations) > 0
        assert any('password' in rec.lower() for rec in recommendations)


class TestConsistencyChecker:
    """Test ConsistencyChecker functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.checker = ConsistencyChecker()
    
    def test_check_email_consistency(self):
        """Test email consistency checking."""
        emails = ['email1@test.com', 'email2@test.com', 'email3@test.com']
        result = self.checker._check_email_consistency(emails)
        
        assert result is not None
        assert result['type'] == 'Email Inconsistency'
        assert result['count'] == 3
    
    def test_check_phone_consistency(self):
        """Test phone consistency checking."""
        phones = ['+1234567890', '+9876543210', '+5555555555']
        result = self.checker._check_phone_consistency(phones)
        
        assert result is not None
        assert result['type'] == 'Phone Inconsistency'
    
    def test_check_address_consistency(self):
        """Test address consistency checking."""
        addresses = [
            {'city': 'Jakarta', 'postal_code': '12345'},
            {'city': 'Surabaya', 'postal_code': '67890'},
        ]
        result = self.checker._check_address_consistency(addresses)
        
        assert result is not None
        assert result['severity'] == 'HIGH'
    
    def test_check_name_consistency(self):
        """Test name consistency checking."""
        names = ['John Doe', 'Jane Smith']
        result = self.checker._check_name_consistency(names)
        
        assert result is not None
        assert result['type'] == 'Name Inconsistency'
    
    def test_consistency_score_perfect(self):
        """Test perfect consistency score."""
        inconsistencies = []
        score = self.checker._calculate_consistency_score(inconsistencies)
        
        assert score == 100.0
    
    def test_consistency_score_with_issues(self):
        """Test consistency score with issues."""
        inconsistencies = [
            {'severity': 'HIGH'},
            {'severity': 'MEDIUM'},
        ]
        score = self.checker._calculate_consistency_score(inconsistencies)
        
        assert score < 100.0
        assert score >= 0
    
    def test_check_consistency(self):
        """Test overall consistency check."""
        extracted_data = {
            'emails': ['email1@test.com', 'email2@test.com', 'email3@test.com'],
            'phones': ['+1234567890'],
            'addresses': [{'city': 'Jakarta'}],
            'names': ['John Doe'],
        }
        
        result = self.checker.check_consistency(extracted_data)
        
        assert 'has_inconsistencies' in result
        assert 'inconsistency_count' in result
        assert 'inconsistencies' in result
        assert 'consistency_score' in result


class TestBehaviorAnalyzer:
    """Test BehaviorAnalyzer functionality."""
    
    def setup_method(self):
        """Setup test instance."""
        self.analyzer = BehaviorAnalyzer()
    
    def test_analyze_channels_empty(self):
        """Test channel analysis with no channels."""
        channels = []
        result = self.analyzer._analyze_channels(channels)
        
        assert result['total_channels'] == 0
        assert result['top_category'] is None
    
    def test_analyze_channels_with_data(self):
        """Test channel analysis with channels."""
        channels = ['python_programming', 'tech_news', 'developer_tips']
        result = self.analyzer._analyze_channels(channels)
        
        assert result['total_channels'] == 3
        assert 'technology' in result['categories']
        assert result['top_category'] == 'technology'
    
    def test_interest_level(self):
        """Test interest level calculation."""
        assert self.analyzer._interest_level(15) == 'High'
        assert self.analyzer._interest_level(7) == 'Medium'
        assert self.analyzer._interest_level(3) == 'Low'
    
    def test_calculate_activity_level(self):
        """Test activity level calculation."""
        assert self.analyzer._calculate_activity_level(60) == 'Very High'
        assert self.analyzer._calculate_activity_level(40) == 'High'
        assert self.analyzer._calculate_activity_level(20) == 'Medium'
        assert self.analyzer._calculate_activity_level(10) == 'Low'
        assert self.analyzer._calculate_activity_level(3) == 'Very Low'
    
    def test_calculate_data_richness(self):
        """Test data richness calculation."""
        rich_data = {
            'names': ['John Doe'],
            'emails': ['test@example.com'],
            'phones': ['+1234567890'],
            'addresses': [{'city': 'Jakarta'}],
            'dates': [{'value': '1990-01-01'}],
            'passwords': [{'type': 'MD5'}],
            'telegram_info': {'channels': ['channel1']},
        }
        
        result = self.analyzer._calculate_data_richness(rich_data)
        assert result in ['Very Rich', 'Rich', 'Moderate', 'Limited']
    
    def test_detect_anomalies(self):
        """Test anomaly detection."""
        extracted_data = {
            'telegram_info': {
                'channels': ['kali_linux', 'metasploit', 'tech1', 'tech2', 'tech3', 'tech4', 'tech5', 'tech6']
            },
            'addresses': [
                {'city': 'Jakarta'},
                {'city': 'Surabaya'},
                {'city': 'Bandung'},
            ],
        }
        
        channel_analysis = {
            'total_channels': 60,
            'categories': {'technology': 8},
        }
        
        anomalies = self.analyzer._detect_anomalies(extracted_data, channel_analysis)
        
        assert len(anomalies) > 0
    
    def test_behavior_score(self):
        """Test behavior score calculation."""
        anomalies = [
            {'severity': 'HIGH'},
            {'severity': 'MEDIUM'},
        ]
        
        score = self.analyzer._calculate_behavior_score(anomalies)
        
        assert score <= 100.0
        assert score >= 0
    
    def test_analyze_behavior(self):
        """Test overall behavior analysis."""
        extracted_data = {
            'telegram_info': {
                'channels': ['python_dev', 'tech_news']
            },
            'addresses': [{'city': 'Jakarta'}],
            'emails': ['test@example.com'],
            'phones': ['+1234567890'],
        }
        
        result = self.analyzer.analyze_behavior(extracted_data)
        
        assert 'channel_analysis' in result
        assert 'anomalies' in result
        assert 'user_profile' in result
        assert 'behavior_score' in result
