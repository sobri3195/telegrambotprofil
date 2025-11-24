"""
Main entry point for the Telegram Data Breach Analyzer Bot.
"""
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config import get_settings
from src.handlers import (
    start_handler,
    help_handler,
    analyze_handler,
    document_handler,
    text_handler,
)
from src.handlers.analyze import cancel_handler, WAITING_FOR_INPUT

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
    
    logger.info("Starting Data Breach Analyzer Bot...")
    
    application = Application.builder().token(settings.telegram_bot_token).build()
    
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("analyze", analyze_handler)],
        states={
            WAITING_FOR_INPUT: [
                MessageHandler(filters.Document.ALL, document_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
    )
    
    application.add_handler(conv_handler)
    
    logger.info("Bot is running. Press Ctrl+C to stop.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
