"""
Behavior analyzer module for profiling and pattern detection.
"""
from typing import Dict, List, Any


class BehaviorAnalyzer:
    """Analyze behavioral patterns and user profiling from data."""
    
    CHANNEL_CATEGORIES = {
        'technology': [
            'tech', 'developer', 'programming', 'coding', 'linux', 'python',
            'javascript', 'android', 'ios', 'software', 'hacker', 'cyber'
        ],
        'business': [
            'business', 'entrepreneur', 'startup', 'finance', 'investment',
            'trading', 'marketing', 'sales'
        ],
        'healthcare': [
            'health', 'medical', 'doctor', 'fitness', 'wellness', 'nutrition',
            'pharmacy', 'hospital'
        ],
        'education': [
            'education', 'university', 'course', 'learning', 'tutorial',
            'study', 'research'
        ],
        'entertainment': [
            'movie', 'music', 'game', 'gaming', 'entertainment', 'video',
            'stream', 'youtube'
        ],
        'news': [
            'news', 'berita', 'media', 'journal', 'press', 'update'
        ],
    }
    
    def analyze_behavior(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user behavior patterns from extracted data.
        
        Args:
            extracted_data: Dictionary containing all extracted data
            
        Returns:
            Behavior analysis report
        """
        telegram_info = extracted_data.get('telegram_info', {})
        channels = telegram_info.get('channels', [])
        
        channel_analysis = self._analyze_channels(channels)
        anomalies = self._detect_anomalies(extracted_data, channel_analysis)
        profile = self._build_user_profile(extracted_data, channel_analysis)
        
        return {
            'channel_analysis': channel_analysis,
            'anomalies': anomalies,
            'user_profile': profile,
            'behavior_score': self._calculate_behavior_score(anomalies),
        }
    
    def _analyze_channels(self, channels: List[str]) -> Dict[str, Any]:
        """Analyze Telegram channels to determine interests."""
        if not channels:
            return {
                'total_channels': 0,
                'categories': {},
                'top_category': None,
            }
        
        category_counts = {cat: 0 for cat in self.CHANNEL_CATEGORIES}
        categorized_channels = {cat: [] for cat in self.CHANNEL_CATEGORIES}
        
        for channel in channels:
            channel_lower = channel.lower()
            for category, keywords in self.CHANNEL_CATEGORIES.items():
                if any(keyword in channel_lower for keyword in keywords):
                    category_counts[category] += 1
                    categorized_channels[category].append(channel)
                    break
        
        top_category = max(category_counts.items(), key=lambda x: x[1])
        
        return {
            'total_channels': len(channels),
            'categories': {k: v for k, v in category_counts.items() if v > 0},
            'categorized_channels': {k: v for k, v in categorized_channels.items() if v},
            'top_category': top_category[0] if top_category[1] > 0 else None,
        }
    
    def _detect_anomalies(
        self,
        extracted_data: Dict[str, Any],
        channel_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect behavioral anomalies."""
        anomalies = []
        
        tech_channels = channel_analysis.get('categories', {}).get('technology', 0)
        hacker_keywords = ['kali', 'metasploit', 'exploit', 'pentest', 'hacking']
        
        channels = extracted_data.get('telegram_info', {}).get('channels', [])
        has_hacker_channels = any(
            any(keyword in ch.lower() for keyword in hacker_keywords)
            for ch in channels
        )
        
        if has_hacker_channels and tech_channels > 5:
            anomalies.append({
                'type': 'High Technical Interest',
                'severity': 'MEDIUM',
                'description': 'User shows strong interest in hacking/security topics',
                'detail': f"Following {tech_channels} technology channels including security-focused ones"
            })
        
        addresses = extracted_data.get('addresses', [])
        if len(addresses) > 2:
            cities = [addr.get('city', '') for addr in addresses if addr.get('city')]
            if len(set(cities)) > 1:
                anomalies.append({
                    'type': 'Geographic Inconsistency',
                    'severity': 'MEDIUM',
                    'description': 'Activity detected in multiple geographic locations',
                    'detail': f"Locations: {', '.join(set(cities))}"
                })
        
        if channel_analysis.get('total_channels', 0) > 50:
            anomalies.append({
                'type': 'High Activity Level',
                'severity': 'LOW',
                'description': 'User follows unusually high number of channels',
                'detail': f"Following {channel_analysis['total_channels']} channels"
            })
        
        return anomalies
    
    def _build_user_profile(
        self,
        extracted_data: Dict[str, Any],
        channel_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a user profile from available data."""
        interests = []
        categories = channel_analysis.get('categories', {})
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                interests.append({
                    'category': category.title(),
                    'level': self._interest_level(count),
                    'channel_count': count,
                })
        
        return {
            'primary_interest': interests[0]['category'] if interests else 'Unknown',
            'interests': interests,
            'activity_level': self._calculate_activity_level(
                channel_analysis.get('total_channels', 0)
            ),
            'data_richness': self._calculate_data_richness(extracted_data),
        }
    
    def _interest_level(self, count: int) -> str:
        """Determine interest level based on channel count."""
        if count >= 10:
            return 'High'
        elif count >= 5:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_activity_level(self, channel_count: int) -> str:
        """Calculate activity level from channel count."""
        if channel_count >= 50:
            return 'Very High'
        elif channel_count >= 30:
            return 'High'
        elif channel_count >= 15:
            return 'Medium'
        elif channel_count >= 5:
            return 'Low'
        else:
            return 'Very Low'
    
    def _calculate_data_richness(self, extracted_data: Dict[str, Any]) -> str:
        """Calculate how rich/complete the data is."""
        score = 0
        max_score = 7
        
        if extracted_data.get('names'):
            score += 1
        if extracted_data.get('emails'):
            score += 1
        if extracted_data.get('phones'):
            score += 1
        if extracted_data.get('addresses'):
            score += 1
        if extracted_data.get('dates'):
            score += 1
        if extracted_data.get('passwords'):
            score += 1
        if extracted_data.get('telegram_info', {}).get('channels'):
            score += 1
        
        percentage = (score / max_score) * 100
        
        if percentage >= 80:
            return 'Very Rich'
        elif percentage >= 60:
            return 'Rich'
        elif percentage >= 40:
            return 'Moderate'
        else:
            return 'Limited'
    
    def _calculate_behavior_score(self, anomalies: List[Dict]) -> float:
        """
        Calculate behavior score (0-100).
        Lower score = more anomalies/suspicious behavior.
        """
        if not anomalies:
            return 100.0
        
        severity_weights = {
            'HIGH': 25,
            'MEDIUM': 15,
            'LOW': 5,
        }
        
        total_penalty = sum(
            severity_weights.get(anom.get('severity', 'LOW'), 5)
            for anom in anomalies
        )
        
        score = max(0, 100 - total_penalty)
        return round(score, 2)
