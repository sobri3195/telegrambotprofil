"""
Search engine module for simulating database searches across platforms.
"""
import random
from typing import List, Dict, Any
from ..parsers.search_parser import SearchType


class SearchEngine:
    """Simulates searching across multiple data breach platforms."""
    
    PLATFORMS = [
        "Bhinneka", "BukalaPak", "Civil Registry", "Gravatar", 
        "Gravatar US 2020", "RedDoorz", "SlideTeam", "Telegram Chats",
        "Tokopedia", "Travelio", "Trello", "Wahana Express", 
        "Wattpad", "YouthManual", "LinkedIn", "Facebook",
        "Instagram", "Twitter", "MySpace", "Adobe", "Yahoo",
        "Dropbox", "Canva", "Shopee", "Lazada", "GoJek",
        "Grab", "OVO", "DANA", "Spotify", "Netflix"
    ]
    
    @classmethod
    def search(cls, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform search across platforms.
        
        Args:
            query_data: Parsed query data
            
        Returns:
            Search results with platform matches
        """
        query_type = query_data['type']
        query_value = query_data['value']
        
        num_platforms = cls._get_platform_count(query_type)
        selected_platforms = random.sample(cls.PLATFORMS, min(num_platforms, len(cls.PLATFORMS)))
        
        results = []
        total_data_points = 0
        
        for platform in selected_platforms:
            data_count = cls._get_data_count(query_type, platform)
            results.append({
                'platform': platform,
                'data_count': data_count
            })
            total_data_points += data_count
        
        return {
            'query': query_value,
            'query_type': query_type.value if isinstance(query_type, SearchType) else str(query_type),
            'platforms': sorted(results, key=lambda x: x['platform']),
            'total_platforms': len(results),
            'total_data_points': total_data_points
        }
    
    @classmethod
    def _get_platform_count(cls, query_type: SearchType) -> int:
        """Get number of platforms that might have data."""
        if query_type == SearchType.NAME:
            return random.randint(8, 15)
        elif query_type == SearchType.EMAIL:
            return random.randint(5, 12)
        elif query_type == SearchType.PHONE:
            return random.randint(3, 10)
        elif query_type == SearchType.COMBO:
            return random.randint(10, 18)
        elif query_type in [SearchType.CAR_PLATE, SearchType.CAR_VIN]:
            return random.randint(2, 6)
        elif query_type == SearchType.IP_ADDRESS:
            return random.randint(3, 8)
        else:
            return random.randint(1, 5)
    
    @classmethod
    def _get_data_count(cls, query_type: SearchType, platform: str) -> int:
        """Get simulated data count for a platform."""
        base_counts = {
            SearchType.NAME: (1, 10),
            SearchType.EMAIL: (1, 8),
            SearchType.PHONE: (1, 6),
            SearchType.COMBO: (2, 15),
            SearchType.CAR_PLATE: (1, 3),
            SearchType.CAR_VIN: (1, 2),
            SearchType.IP_ADDRESS: (1, 5)
        }
        
        min_count, max_count = base_counts.get(query_type, (1, 5))
        
        if platform == "Telegram Chats":
            max_count = max_count * 5
        elif platform in ["Facebook", "Instagram", "Twitter"]:
            max_count = max_count * 3
        
        return random.randint(min_count, max_count)
