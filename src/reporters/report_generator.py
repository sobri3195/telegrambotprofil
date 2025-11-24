"""
Report generation module for creating structured analysis reports.
"""
from datetime import datetime
from typing import Dict, Any, List
from .data_masker import DataMasker


class ReportGenerator:
    """Generate structured markdown reports from analysis results."""
    
    def __init__(self):
        self.masker = DataMasker()
    
    def generate_full_report(
        self,
        extracted_data: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        consistency_check: Dict[str, Any],
        behavior_analysis: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive analysis report.
        
        Args:
            extracted_data: Extracted data from parsing
            risk_assessment: Risk assessment results
            consistency_check: Consistency check results
            behavior_analysis: Behavior analysis results
            
        Returns:
            Formatted markdown report
        """
        report_parts = [
            self._generate_header(extracted_data, risk_assessment),
            self._generate_personal_data_section(extracted_data),
            self._generate_data_sources_section(extracted_data, risk_assessment),
            self._generate_findings_section(risk_assessment, consistency_check, behavior_analysis),
            self._generate_recommendations_section(risk_assessment),
            self._generate_footer()
        ]
        
        return '\n\n'.join(report_parts)
    
    def _generate_header(self, extracted_data: Dict[str, Any], risk_assessment: Dict[str, Any]) -> str:
        """Generate report header."""
        names = extracted_data.get('names', [])
        target_name = self.masker.mask_name(names[0]) if names else "[Unknown Target]"
        
        risk_level = risk_assessment.get('risk_level', 'MEDIUM')
        risk_emoji = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }.get(risk_level, '⚪')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""## 🛡️ DATA BREACH ANALYSIS REPORT

**Target**: {target_name}  
**Tanggal Analisis**: {timestamp}  
**Status**: {risk_emoji} **{risk_level} RISK**"""
    
    def _generate_personal_data_section(self, extracted_data: Dict[str, Any]) -> str:
        """Generate personal data section with masking."""
        names = extracted_data.get('names', [])
        emails = extracted_data.get('emails', [])
        phones = extracted_data.get('phones', [])
        addresses = extracted_data.get('addresses', [])
        sensitive_data = extracted_data.get('sensitive_data', [])
        
        masked_name = self.masker.mask_name(names[0]) if names else "[Not Found]"
        masked_emails = self.masker.mask_list(emails, self.masker.mask_email, 2) if emails else ["[Not Found]"]
        masked_phones = self.masker.mask_list(phones, self.masker.mask_phone, 2) if phones else ["[Not Found]"]
        masked_address = self.masker.mask_address(addresses[0]) if addresses else "[Not Found]"
        
        section = f"""### 📋 Data Pribadi (Masked)

- **Nama**: {masked_name}
- **Email**: {', '.join(masked_emails)}
- **Telepon**: {', '.join(masked_phones)}
- **Alamat**: {masked_address}"""
        
        if sensitive_data:
            passport_items = [item for item in sensitive_data if 'passport' in item.get('type', '').lower()]
            if passport_items:
                masked_passport = self.masker.mask_passport(passport_items[0]['value'])
                section += f"\n- **Passport**: {masked_passport}"
        
        return section
    
    def _generate_data_sources_section(
        self,
        extracted_data: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> str:
        """Generate data sources table."""
        sources = extracted_data.get('sources', [])
        passwords = extracted_data.get('passwords', [])
        sensitive_data = extracted_data.get('sensitive_data', [])
        telegram_info = extracted_data.get('telegram_info', {})
        
        section = """### 🔍 Sumber Data

| Sumber        | Data Terdeteksi                  | Risiko |
|---------------|----------------------------------|--------|"""
        
        source_data = self._map_sources_to_data(
            sources, extracted_data, passwords, sensitive_data, telegram_info
        )
        
        for source, data, risk in source_data:
            section += f"\n| {source:<13} | {data:<32} | {risk:<6} |"
        
        return section
    
    def _map_sources_to_data(
        self,
        sources: List[str],
        extracted_data: Dict[str, Any],
        passwords: List[Dict],
        sensitive_data: List[Dict],
        telegram_info: Dict[str, Any]
    ) -> List[tuple]:
        """Map sources to detected data and risk levels."""
        source_mappings = []
        
        if 'Bhinneka' in sources or 'Database' in sources:
            pwd_info = "Password (bcrypt)" if any(p.get('type') == 'bcrypt' for p in passwords) else "Email, Telepon"
            risk = 'LOW' if any(p.get('type') == 'bcrypt' for p in passwords) else 'MEDIUM'
            source_mappings.append(('Bhinneka', 'Email, Telepon, ' + pwd_info, risk))
        
        if 'Civil Registry' in sources or any('passport' in str(sd).lower() for sd in sensitive_data):
            source_mappings.append(('Civil Registry', 'Passport, Alamat Rumah', 'HIGH'))
        
        channels = telegram_info.get('channels', [])
        if channels or 'Telegram' in sources:
            channel_count = len(channels)
            data_desc = f"{channel_count}+ Channel" if channel_count > 0 else "User Info"
            source_mappings.append(('Telegram', data_desc, 'MEDIUM'))
        
        if 'SlideTeam' in sources or any(p.get('type') == 'MD5' for p in passwords):
            source_mappings.append(('SlideTeam', 'Email, Password (MD5)', 'HIGH'))
        
        if not source_mappings:
            source_mappings.append(('Unknown', 'Various Data', 'MEDIUM'))
        
        return source_mappings
    
    def _generate_findings_section(
        self,
        risk_assessment: Dict[str, Any],
        consistency_check: Dict[str, Any],
        behavior_analysis: Dict[str, Any]
    ) -> str:
        """Generate critical findings section."""
        section = "### ⚠️ Temuan Kritis\n"
        
        findings = risk_assessment.get('findings', [])
        inconsistencies = consistency_check.get('inconsistencies', [])
        anomalies = behavior_analysis.get('anomalies', [])
        
        all_issues = []
        
        for finding in findings:
            severity_emoji = {
                'HIGH': '🔴',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(finding.get('severity', 'LOW'), '⚪')
            
            all_issues.append({
                'emoji': severity_emoji,
                'category': finding.get('category'),
                'description': finding.get('description'),
                'severity': finding.get('severity')
            })
        
        for inconsistency in inconsistencies:
            all_issues.append({
                'emoji': '🔄',
                'category': inconsistency.get('type'),
                'description': inconsistency.get('description'),
                'severity': inconsistency.get('severity')
            })
        
        for anomaly in anomalies:
            all_issues.append({
                'emoji': '⚡',
                'category': anomaly.get('type'),
                'description': anomaly.get('description'),
                'severity': anomaly.get('severity')
            })
        
        all_issues.sort(key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}.get(x['severity'], 3))
        
        if all_issues:
            for issue in all_issues[:10]:
                section += f"- {issue['emoji']} **{issue['category']}**: {issue['description']} ({issue['severity']} RISK)\n"
        else:
            section += "- ✅ Tidak ada temuan kritis yang terdeteksi\n"
        
        user_profile = behavior_analysis.get('user_profile', {})
        if user_profile.get('primary_interest'):
            section += f"\n**Profil Pengguna**: Minat utama di {user_profile['primary_interest']}, "
            section += f"Activity Level: {user_profile.get('activity_level', 'Unknown')}"
        
        return section
    
    def _generate_recommendations_section(self, risk_assessment: Dict[str, Any]) -> str:
        """Generate recommendations section."""
        recommendations = risk_assessment.get('recommendations', [])
        
        section = "### 💡 Rekomendasi\n"
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                section += f"{i}. {rec}\n"
        else:
            section += "1. 🔐 Aktifkan Two-Factor Authentication (2FA) di semua akun\n"
            section += "2. 📧 Gunakan password manager untuk keamanan lebih baik\n"
            section += "3. 🔍 Monitor akun secara berkala\n"
        
        return section
    
    def _generate_footer(self) -> str:
        """Generate report footer."""
        return """---
*Report generated by Data Breach Analyzer Bot*  
*⚠️ Disclaimer: Laporan ini untuk tujuan edukasi dan keamanan. Gunakan dengan bijak.*"""
