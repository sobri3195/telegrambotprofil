"""
Consistency checker module for cross-referencing data across sources.
"""
from typing import Dict, List, Any


class ConsistencyChecker:
    """Check consistency and identify discrepancies in data across sources."""
    
    def check_consistency(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check data consistency across different fields and sources.
        
        Args:
            extracted_data: Dictionary containing all extracted data
            
        Returns:
            Consistency analysis report
        """
        inconsistencies = []
        
        email_inconsistency = self._check_email_consistency(
            extracted_data.get('emails', [])
        )
        if email_inconsistency:
            inconsistencies.append(email_inconsistency)
        
        phone_inconsistency = self._check_phone_consistency(
            extracted_data.get('phones', [])
        )
        if phone_inconsistency:
            inconsistencies.append(phone_inconsistency)
        
        address_inconsistency = self._check_address_consistency(
            extracted_data.get('addresses', [])
        )
        if address_inconsistency:
            inconsistencies.append(address_inconsistency)
        
        name_inconsistency = self._check_name_consistency(
            extracted_data.get('names', [])
        )
        if name_inconsistency:
            inconsistencies.append(name_inconsistency)
        
        return {
            'has_inconsistencies': len(inconsistencies) > 0,
            'inconsistency_count': len(inconsistencies),
            'inconsistencies': inconsistencies,
            'consistency_score': self._calculate_consistency_score(inconsistencies),
        }
    
    def _check_email_consistency(self, emails: List[str]) -> Dict[str, Any]:
        """Check for multiple email addresses which may indicate inconsistency."""
        if len(emails) > 2:
            return {
                'type': 'Email Inconsistency',
                'severity': 'MEDIUM',
                'description': f"Found {len(emails)} different email addresses",
                'details': f"Multiple emails may indicate data from different sources or identity confusion",
                'count': len(emails),
            }
        return None
    
    def _check_phone_consistency(self, phones: List[str]) -> Dict[str, Any]:
        """Check for multiple phone numbers."""
        if len(phones) > 2:
            return {
                'type': 'Phone Inconsistency',
                'severity': 'MEDIUM',
                'description': f"Found {len(phones)} different phone numbers",
                'details': "Multiple numbers may indicate different devices or time periods",
                'count': len(phones),
            }
        return None
    
    def _check_address_consistency(self, addresses: List[Dict]) -> Dict[str, Any]:
        """Check for multiple addresses."""
        if len(addresses) > 1:
            cities = [addr.get('city', '') for addr in addresses if addr.get('city')]
            unique_cities = set(filter(None, cities))
            
            if len(unique_cities) > 1:
                return {
                    'type': 'Address Inconsistency',
                    'severity': 'HIGH',
                    'description': f"Found addresses in {len(unique_cities)} different cities",
                    'details': f"Cities: {', '.join(unique_cities)}",
                    'count': len(addresses),
                }
        return None
    
    def _check_name_consistency(self, names: List[str]) -> Dict[str, Any]:
        """Check for variations in names."""
        if len(names) > 1:
            first_names = set()
            for name in names:
                parts = name.split()
                if parts:
                    first_names.add(parts[0].lower())
            
            if len(first_names) > 1:
                return {
                    'type': 'Name Inconsistency',
                    'severity': 'LOW',
                    'description': f"Found {len(names)} name variations",
                    'details': "Name variations may indicate different records or aliases",
                    'count': len(names),
                }
        return None
    
    def _calculate_consistency_score(self, inconsistencies: List[Dict]) -> float:
        """
        Calculate consistency score (0-100).
        Higher score = more consistent.
        """
        if not inconsistencies:
            return 100.0
        
        severity_weights = {
            'HIGH': 30,
            'MEDIUM': 15,
            'LOW': 5,
        }
        
        total_penalty = sum(
            severity_weights.get(inc.get('severity', 'LOW'), 5)
            for inc in inconsistencies
        )
        
        score = max(0, 100 - total_penalty)
        return round(score, 2)
