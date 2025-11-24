"""
Main entry point for the Telegram Data Breach Search Bot.
"""
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import get_settings
from src.handlers import (
    start_handler,
    help_handler,
    search_handler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    try:
        settings = get_settings()
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        logger.error("Please ensure .env file exists with TELEGRAM_BOT_TOKEN set")
        sys.exit(1)
    
    logger.info("Starting Data Breach Search Bot...")
    
    application = Application.builder().token(settings.telegram_bot_token).build()
    
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler)
    )
    
    logger.info("Bot is running. Press Ctrl+C to stop.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
