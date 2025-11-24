"""
Results formatter module for displaying search results.
"""
from typing import Dict, Any, List


class ResultsFormatter:
    """Formats search results for display."""
    
    @staticmethod
    def format_search_results(
        results: Dict[str, Any],
        credits_used: int,
        credits_remaining: int,
        show_all: bool = True
    ) -> str:
        """
        Format search results as markdown text.
        
        Args:
            results: Search results dictionary
            credits_used: Number of credits used
            credits_remaining: Remaining credits
            show_all: Whether user has credits to see all data
            
        Returns:
            Formatted message string
        """
        query = results['query']
        platforms = results['platforms']
        total_platforms = results['total_platforms']
        total_data_points = results['total_data_points']
        
        message = f"*Search Results for {query}*\n\n"
        
        if show_all:
            for platform_data in platforms:
                platform = platform_data['platform']
                count = platform_data['data_count']
                message += f"*Platform:* {platform}\n"
                message += f"*Data Count:* {count}\n\n"
        else:
            message += "⚠️ _Limited results shown due to insufficient credits_\n\n"
            shown_count = min(3, len(platforms))
            for platform_data in platforms[:shown_count]:
                platform = platform_data['platform']
                count = platform_data['data_count']
                message += f"*Platform:* {platform}\n"
                message += f"*Data Count:* {count}\n\n"
            
            if len(platforms) > shown_count:
                message += f"_...and {len(platforms) - shown_count} more platforms_\n\n"
        
        message += "\n\n*Summary of Activity*\n"
        message += f"*Total Platforms:* {total_platforms}\n"
        message += f"*Total Data Points:* {total_data_points}\n\n"
        
        message += f"*Credits Used:* {credits_used}\n"
        message += f"*Remaining Credits:* {credits_remaining}\n"
        
        if not show_all:
            message += "\n\n⚠️ *Your remaining credit amount is not able to display all data*\n"
            message += "💳 Top up now to see complete results!"
        
        return message
    
    @staticmethod
    def format_waiting_message(query: str) -> str:
        """
        Format waiting/processing message.
        
        Args:
            query: Search query
            
        Returns:
            Formatted message
        """
        return (
            f"Please wait. '{query}' search is in progress... "
            f"⏳\n\nIt usually takes a few seconds."
        )
    
    @staticmethod
    def format_insufficient_credits(required: int, current: int) -> str:
        """
        Format insufficient credits message.
        
        Args:
            required: Required credits
            current: Current credits
            
        Returns:
            Formatted message
        """
        return (
            f"❌ *Insufficient Credits*\n\n"
            f"Your current credit is *{current}*\n"
            f"This search requires *{required}* credits.\n\n"
            f"💳 Top up now!"
        )
    
    @staticmethod
    def format_multi_query_summary(
        queries: List[str],
        total_credits_used: int,
        credits_remaining: int
    ) -> str:
        """
        Format multi-query summary.
        
        Args:
            queries: List of processed queries
            total_credits_used: Total credits used
            credits_remaining: Remaining credits
            
        Returns:
            Formatted message
        """
        message = "*Multi-Query Complete* ✅\n\n"
        message += f"*Processed {len(queries)} queries*\n\n"
        
        for idx, query in enumerate(queries, 1):
            message += f"{idx}. {query}\n"
        
        message += f"\n*Total Credits Used:* {total_credits_used}\n"
        message += f"*Remaining Credits:* {credits_remaining}\n"
        
        return message
