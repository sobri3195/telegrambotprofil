"""
Author command handler.
"""
from telegram import Update
from telegram.ext import ContextTypes


async def author_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /author command."""
    author_message = """👨‍💻 *Developer & Author Information*

*Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE*

━━━━━━━━━━━━━━━━━━━━
📬 *Contact Information*
━━━━━━━━━━━━━━━━━━━━

📧 Email: muhammadsobrimaulana31@gmail.com
💻 GitHub: github.com/sobri3195

━━━━━━━━━━━━━━━━━━━━
🌐 *Social Media & Community*
━━━━━━━━━━━━━━━━━━━━

📺 YouTube: youtube.com/@muhammadsobrimaulana6013
✈️ Telegram: t.me/winlin_exploit
🎵 TikTok: tiktok.com/@dr.sobri
🌐 Website: muhammadsobrimaulana.netlify.app
💼 Portfolio: muhammad-sobri-maulana-kvr6a.sevalla.page

━━━━━━━━━━━━━━━━━━━━
💰 *Support & Donations*
━━━━━━━━━━━━━━━━━━━━

If you find this bot useful, consider supporting the development:

💳 Lynk.id: lynk.id/muhsobrimaulana
☕ Trakteer: trakteer.id/g9mkave5gauns962u07t
🛒 Gumroad: maulanasobri.gumroad.com
🎨 KaryaKarsa: karyakarsa.com/muhammadsobrimaulana
💸 Nyawer: nyawer.co/MuhammadSobriMaulana

━━━━━━━━━━━━━━━━━━━━
💬 *Community Support*
━━━━━━━━━━━━━━━━━━━━

Join our WhatsApp Group for updates and support:
chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl

Thank you for using this bot! 🙏
"""
    
    await update.message.reply_text(
        author_message,
        parse_mode='Markdown'
    )
