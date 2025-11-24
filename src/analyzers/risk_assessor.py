"""
Risk assessment module for evaluating data breach severity.
"""
from typing import Dict, List, Any, Tuple


class RiskAssessor:
    """Assess risk levels of data breaches based on various factors."""
    
    def __init__(self):
        self.risk_scores = {
            'HIGH': 10,
            'MEDIUM': 5,
            'LOW': 2,
        }
    
    def assess_overall_risk(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess overall risk level based on extracted data.
        
        Args:
            extracted_data: Dictionary containing all extracted data
            
        Returns:
            Risk assessment report
        """
        risk_score = 0
        findings = []
        
        password_risk, password_findings = self._assess_password_risk(
            extracted_data.get('passwords', [])
        )
        risk_score += password_risk
        findings.extend(password_findings)
        
        sensitive_risk, sensitive_findings = self._assess_sensitive_data_risk(
            extracted_data.get('sensitive_data', [])
        )
        risk_score += sensitive_risk
        findings.extend(sensitive_findings)
        
        exposure_risk, exposure_findings = self._assess_data_exposure(extracted_data)
        risk_score += exposure_risk
        findings.extend(exposure_findings)
        
        risk_level = self._calculate_risk_level(risk_score)
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'findings': findings,
            'recommendations': self._generate_recommendations(findings),
        }
    
    def _assess_password_risk(self, passwords: List[Dict]) -> Tuple[int, List[Dict]]:
        """Assess password storage security risk."""
        risk_score = 0
        findings = []
        
        for pwd in passwords:
            pwd_risk = pwd.get('risk', 'MEDIUM')
            risk_score += self.risk_scores.get(pwd_risk, 5)
            
            if pwd_risk == 'HIGH':
                findings.append({
                    'category': 'Password Security',
                    'severity': 'HIGH',
                    'description': f"Weak password hash detected: {pwd['type']}",
                    'detail': f"Hash type {pwd['type']} is cryptographically weak and easily crackable."
                })
            elif pwd_risk == 'MEDIUM':
                findings.append({
                    'category': 'Password Security',
                    'severity': 'MEDIUM',
                    'description': f"Password hash without salt: {pwd['type']}",
                    'detail': "Consider using bcrypt or Argon2 for better security."
                })
        
        return risk_score, findings
    
    def _assess_sensitive_data_risk(self, sensitive_data: List[Dict]) -> Tuple[int, List[Dict]]:
        """Assess risk from exposed sensitive data."""
        risk_score = 0
        findings = []
        
        high_risk_types = ['passport', 'paspor', 'credit card', 'kartu kredit', 'bank account']
        
        for item in sensitive_data:
            item_type = item.get('type', '').lower()
            
            if any(hr_type in item_type for hr_type in high_risk_types):
                risk_score += self.risk_scores['HIGH']
                findings.append({
                    'category': 'Sensitive Data Exposure',
                    'severity': 'HIGH',
                    'description': f"Critical identity data exposed: {item['type']}",
                    'detail': f"Value: {item['value'][:10]}..."
                })
            else:
                risk_score += self.risk_scores['MEDIUM']
                findings.append({
                    'category': 'Sensitive Data Exposure',
                    'severity': 'MEDIUM',
                    'description': f"Personal data exposed: {item['type']}",
                    'detail': "Moderate privacy risk detected."
                })
        
        return risk_score, findings
    
    def _assess_data_exposure(self, extracted_data: Dict[str, Any]) -> Tuple[int, List[Dict]]:
        """Assess risk from general data exposure."""
        risk_score = 0
        findings = []
        
        emails = extracted_data.get('emails', [])
        phones = extracted_data.get('phones', [])
        addresses = extracted_data.get('addresses', [])
        
        if len(emails) > 3:
            risk_score += self.risk_scores['MEDIUM']
            findings.append({
                'category': 'Data Exposure',
                'severity': 'MEDIUM',
                'description': f"Multiple email addresses exposed ({len(emails)} found)",
                'detail': "Increases risk of targeted phishing attacks."
            })
        
        if len(phones) > 2:
            risk_score += self.risk_scores['MEDIUM']
            findings.append({
                'category': 'Data Exposure',
                'severity': 'MEDIUM',
                'description': f"Multiple phone numbers exposed ({len(phones)} found)",
                'detail': "Risk of SMS phishing and identity verification bypass."
            })
        
        if addresses:
            risk_score += self.risk_scores['HIGH']
            findings.append({
                'category': 'Data Exposure',
                'severity': 'HIGH',
                'description': "Physical address information exposed",
                'detail': "Significant privacy and physical security risk."
            })
        
        return risk_score, findings
    
    def _calculate_risk_level(self, risk_score: int) -> str:
        """Calculate overall risk level from score."""
        if risk_score >= 15:
            return 'HIGH'
        elif risk_score >= 8:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_recommendations(self, findings: List[Dict]) -> List[str]:
        """Generate security recommendations based on findings."""
        recommendations = []
        
        has_password_issue = any(f['category'] == 'Password Security' for f in findings)
        has_sensitive_exposure = any(f['category'] == 'Sensitive Data Exposure' for f in findings)
        has_high_severity = any(f['severity'] == 'HIGH' for f in findings)
        
        if has_password_issue:
            recommendations.append(
                "🔐 Segera ganti password di semua platform yang menggunakan hash lemah (MD5/SHA-1)"
            )
        
        if has_sensitive_exposure:
            recommendations.append(
                "🛡️ Monitor identitas Anda secara berkala untuk mendeteksi penyalahgunaan"
            )
        
        if has_high_severity:
            recommendations.append(
                "⚠️ Pertimbangkan freeze credit report untuk mencegah fraud"
            )
        
        recommendations.extend([
            "🔑 Aktifkan Two-Factor Authentication (2FA) di semua akun penting",
            "📧 Gunakan email dan nomor telepon yang berbeda untuk akun sensitif",
            "🔍 Pantau dark web untuk mencari eksposur data tambahan",
        ])
        
        return recommendations
