"""
Help command handler.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..utils.user_manager import user_manager


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user_id = update.effective_user.id
    credits = user_manager.get_credits(user_id)
    
    help_message = f"""📚 *Help - Data Breach Search Bot*

*Your Credits:* {credits}

*🔍 How to Search:*

Just send me any query directly - no commands needed!

*📧 Email Search:*
• `example@gmail.com` - full email
• `example@` - search by name part
• `@gmail.com` - search by domain

*📱 Phone Search:*
• `+79024196473` - with country code
• `79024196473` - local format

*🚗 Vehicle Search:*
• `O999МУ777` - license plate
• `XTA21150053965897` - VIN number

*📍 IP Address:*
• `127.0.0.1` - IPv4 address

*👤 Name Search:*
• `Muhammad Sobri Maulana` - full name
• `John Doe` - any name

*🔀 Combo Search:*
Combine name with other identifiers:
• `Sergio 79024196473`
• `Ivan Kuznetsov 09/18/1991`
• `example@gmail.com 889Kkt`

*🧠 Multi Query:*
Send multiple queries, one per line:
```
Muhammad Sobri Maulana
example@gmail.com
+79024196473
```

*💳 Credits:*
• Each search costs 1 credit
• You started with 51 free credits
• Contact admin to top up

*📊 Results Include:*
• Platforms where data was found
• Number of data points per platform
• Total summary statistics

*Need to start over?* Use /start

*Have questions?* Contact our support team.
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode='Markdown'
    )
