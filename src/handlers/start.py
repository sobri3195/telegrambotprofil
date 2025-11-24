"""
Start command handler.
"""
from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    welcome_message = """
🛡️ **Selamat Datang di Data Breach Analyzer Bot!**

Bot ini membantu Anda menganalisis dokumen pelanggaran data (data breach) dan melakukan profiling pengguna dengan fitur:

✅ **Ekstraksi Data Otomatis**
   • Email, telepon, alamat
   • Password hash analysis
   • Data sensitif (passport, dll)
   • Informasi Telegram

✅ **Analisis Mendalam**
   • Assessment risiko keamanan
   • Konsistensi data
   • Pola perilaku & anomali
   • Geolokasi

✅ **Laporan Terstruktur**
   • Format markdown
   • Data masking untuk privasi
   • Rekomendasi keamanan

**📖 Cara Menggunakan:**

1. Kirim perintah `/analyze`
2. Upload dokumen (PDF/TXT) atau kirim teks mentah
3. Dapatkan laporan analisis lengkap!

**Perintah Tersedia:**
/start - Tampilkan pesan ini
/help - Bantuan lengkap
/analyze - Mulai analisis data

⚠️ **Disclaimer**: Bot ini untuk tujuan edukasi dan penelitian keamanan.

Kirim `/analyze` untuk memulai!
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown'
    )
