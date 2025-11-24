"""
Search handler for processing user queries.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import get_settings
from ..utils.user_manager import user_manager
from ..parsers.search_parser import SearchParser
from ..search import SearchEngine, ResultsFormatter

logger = logging.getLogger(__name__)


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle search queries from users."""
    settings = get_settings()
    user_id = update.effective_user.id
    query_text = update.message.text.strip()
    
    if not query_text:
        await update.message.reply_text(
            "❌ Please send a valid query.\n\nUse /help to see examples."
        )
        return
    
    queries = query_text.split('\n')
    queries = [q.strip() for q in queries if q.strip()]
    
    if len(queries) > settings.max_multi_query:
        await update.message.reply_text(
            f"❌ Too many queries! Maximum is {settings.max_multi_query} per message."
        )
        return
    
    is_multi_query = len(queries) > 1
    
    total_credits_needed = len(queries) * settings.credit_cost_per_search
    
    if not user_manager.has_sufficient_credits(user_id, total_credits_needed):
        current_credits = user_manager.get_credits(user_id)
        await update.message.reply_text(
            ResultsFormatter.format_insufficient_credits(
                total_credits_needed,
                current_credits
            ),
            parse_mode='Markdown'
        )
        return
    
    if is_multi_query:
        await process_multi_query(update, user_id, queries, settings)
    else:
        await process_single_query(update, user_id, queries[0], settings)


async def process_single_query(update: Update, user_id: int, query: str, settings) -> None:
    """Process a single search query."""
    waiting_msg = await update.message.reply_text(
        ResultsFormatter.format_waiting_message(query)
    )
    
    try:
        parsed_query = SearchParser.parse_query(query)
        
        logger.info(f"User {user_id} searching for: {query} (type: {parsed_query['type']})")
        
        search_results = SearchEngine.search(parsed_query)
        
        user_manager.deduct_credits(user_id, settings.credit_cost_per_search)
        
        credits_remaining = user_manager.get_credits(user_id)
        
        show_all = credits_remaining > 0
        
        results_message = ResultsFormatter.format_search_results(
            search_results,
            settings.credit_cost_per_search,
            credits_remaining,
            show_all
        )
        
        await waiting_msg.delete()
        
        await update.message.reply_text(
            results_message,
            parse_mode='Markdown'
        )
        
        if credits_remaining == 0:
            await update.message.reply_text(
                "⚠️ *Your credits have run out!*\n\n"
                "💳 Top up now to continue searching!",
                parse_mode='Markdown'
            )
        
    except Exception as e:
        logger.error(f"Error processing search: {str(e)}")
        await waiting_msg.delete()
        await update.message.reply_text(
            "❌ An error occurred while processing your search. Please try again."
        )


async def process_multi_query(update: Update, user_id: int, queries: list, settings) -> None:
    """Process multiple search queries."""
    await update.message.reply_text(
        f"🧠 *Multi Query Mode*\n\n"
        f"Processing {len(queries)} queries...",
        parse_mode='Markdown'
    )
    
    try:
        for idx, query in enumerate(queries, 1):
            waiting_msg = await update.message.reply_text(
                f"⏳ [{idx}/{len(queries)}] {ResultsFormatter.format_waiting_message(query)}"
            )
            
            parsed_query = SearchParser.parse_query(query)
            
            search_results = SearchEngine.search(parsed_query)
            
            user_manager.deduct_credits(user_id, settings.credit_cost_per_search)
            
            credits_remaining = user_manager.get_credits(user_id)
            
            show_all = credits_remaining > 0
            
            results_message = ResultsFormatter.format_search_results(
                search_results,
                settings.credit_cost_per_search,
                credits_remaining,
                show_all
            )
            
            await waiting_msg.delete()
            
            await update.message.reply_text(
                results_message,
                parse_mode='Markdown'
            )
            
            if credits_remaining == 0:
                remaining_queries = len(queries) - idx
                if remaining_queries > 0:
                    await update.message.reply_text(
                        f"⚠️ *Credits exhausted!*\n\n"
                        f"Stopped processing. {remaining_queries} queries remaining.\n\n"
                        f"💳 Top up to continue!",
                        parse_mode='Markdown'
                    )
                break
        
        credits_used = len(queries) * settings.credit_cost_per_search
        credits_remaining = user_manager.get_credits(user_id)
        
        summary = ResultsFormatter.format_multi_query_summary(
            queries,
            min(credits_used, settings.initial_credits),
            credits_remaining
        )
        
        await update.message.reply_text(
            summary,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error processing multi-query: {str(e)}")
        await update.message.reply_text(
            "❌ An error occurred while processing your queries. Please try again."
        )
