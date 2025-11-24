"""
Start command handler.
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import get_settings
from ..utils.user_manager import user_manager


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    settings = get_settings()
    user_id = update.effective_user.id
    user_data = user_manager.get_user(user_id)
    
    if user_data['is_new']:
        welcome_message = f"""*What can this bot do?*

Visit our website: {settings.website_url}

🎉 *Congratulations, you get {settings.initial_credits} free credits!*

🕵️ *Search anything*
balance is *{user_data['credits']}*

📧 *Search by Email*
• example@gmail.com – full email
• example@ – name only
• @gmail.com – domain only

📱 *Search by Phone*
• +79024196473 – with country code
• 79024196473 – local format

🚗 *Search by Car*
• Plate: O999МУ777
• VIN: XTA21150053965897

📍 *IP Address*
• 127.0.0.1

🔀 *Combo Searches*
• Sergio 79024196473
• Dmitri Aleksandr 127.0.0.1
• Ivan Kuznetsov 09/18/1991
• Andrey112 example@gmail.com
• example@gmail.com 889Kkt

🧠 *Multi Query*
Put each query on a new line. All will be processed.

Just send me any query to start searching! 🔍
"""
    else:
        welcome_message = f"""*Welcome back!* 👋

Your balance: *{user_data['credits']} credits*
Total searches: *{user_data['total_searches']}*

Just send me any query to search:
📧 Email • 📱 Phone • 🚗 Car • 📍 IP • 👤 Name

Need help? Use /help
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown'
    )
