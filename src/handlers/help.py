"""
Help command handler.
"""
from telegram import Update
from telegram.ext import ContextTypes


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_message = """
📚 **Panduan Lengkap Data Breach Analyzer Bot**

**🎯 Apa yang Bisa Dianalisis?**

Bot ini dapat mengekstrak dan menganalisis:

1. **Data Pribadi**
   • Nama lengkap
   • Email address
   • Nomor telepon
   • Tanggal lahir
   • Alamat fisik

2. **Data Keamanan**
   • Password hash (MD5, SHA-1, SHA-256, bcrypt, Argon2)
   • Assessment kualitas password storage
   • Identifikasi kelemahan keamanan

3. **Data Sensitif**
   • Nomor passport
   • ID Telegram
   • Channel Telegram
   • Informasi identitas lainnya

4. **Analisis Lanjutan**
   • Konsistensi data cross-reference
   • Pola perilaku pengguna
   • Profiling berdasarkan aktivitas
   • Deteksi anomali

**📥 Format Input yang Didukung:**

• PDF Document (.pdf)
• Text File (.txt)
• Teks mentah (copy-paste)

**🔒 Keamanan & Privasi:**

✅ Semua data di-mask dalam laporan
✅ Tidak ada penyimpanan data permanen
✅ Proses dilakukan di memory
✅ Logs hanya menyimpan metadata

**📊 Contoh Output:**

Laporan mencakup:
• Status risiko (HIGH/MEDIUM/LOW)
• Data pribadi (masked)
• Sumber data breach
• Temuan kritis
• Rekomendasi tindakan

**⚡ Cara Cepat:**

1. `/analyze` - Mulai analisis
2. Upload file atau paste text
3. Tunggu beberapa detik
4. Dapatkan laporan lengkap!

**❓ Butuh Bantuan?**

Jika ada pertanyaan atau masalah, hubungi administrator bot.

Ketik `/analyze` untuk memulai analisis sekarang!
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode='Markdown'
    )
