"""
Analyze command handler for processing data breach documents.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ..parsers import DataExtractor, DocumentParser
from ..analyzers import RiskAssessor, ConsistencyChecker, BehaviorAnalyzer
from ..reporters import ReportGenerator
from ..utils import Validators, format_file_size
from config import get_settings

logger = logging.getLogger(__name__)

WAITING_FOR_INPUT = 1

settings = get_settings()


async def analyze_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /analyze command - start the analysis flow."""
    message = """
🔍 **Analisis Data Breach - Siap Memproses!**

Silakan kirim data yang ingin dianalisis:

📄 **Upload dokumen** (PDF atau TXT, max 20MB)
   atau
📝 **Kirim teks mentah** (copy-paste langsung)

Saya akan menganalisis dan memberikan laporan lengkap dengan:
• Ekstraksi data otomatis
• Assessment risiko
• Analisis konsistensi
• Profiling pengguna
• Rekomendasi keamanan

Kirim dokumen atau teks Anda sekarang...

(Ketik /cancel untuk membatalkan)
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')
    return WAITING_FOR_INPUT


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle document uploads."""
    document = update.message.document
    
    if not document:
        await update.message.reply_text("❌ Tidak ada dokumen yang diterima. Coba lagi.")
        return WAITING_FOR_INPUT
    
    if not Validators.is_valid_extension(document.file_name, settings.allowed_extensions_list):
        await update.message.reply_text(
            f"❌ Format file tidak didukung. Gunakan: {', '.join(settings.allowed_extensions_list)}"
        )
        return WAITING_FOR_INPUT
    
    if not Validators.is_valid_file_size(document.file_size, settings.max_file_size):
        max_size_str = format_file_size(settings.max_file_size)
        await update.message.reply_text(
            f"❌ File terlalu besar. Maksimal: {max_size_str}"
        )
        return WAITING_FOR_INPUT
    
    processing_msg = await update.message.reply_text(
        "⏳ Memproses dokumen...\n"
        "🔄 Mengekstrak data...",
        parse_mode='Markdown'
    )
    
    try:
        file = await document.get_file()
        file_content = await file.download_as_bytearray()
        
        extension = document.file_name.rsplit('.', 1)[1].lower()
        
        await processing_msg.edit_text(
            "⏳ Memproses dokumen...\n"
            "✅ Ekstraksi data selesai\n"
            "🔄 Menganalisis...",
            parse_mode='Markdown'
        )
        
        text_content = DocumentParser.parse_document(bytes(file_content), extension)
        
        report = await process_analysis(text_content)
        
        await processing_msg.edit_text(
            "✅ Analisis selesai!\n"
            "📊 Mengirim laporan...",
            parse_mode='Markdown'
        )
        
        await update.message.reply_text(report, parse_mode='Markdown')
        
        await processing_msg.delete()
        
        logger.info(f"Analysis completed for document: {document.file_name}")
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        await update.message.reply_text(
            f"❌ Terjadi kesalahan saat memproses dokumen:\n{str(e)}\n\n"
            "Coba lagi atau gunakan format lain."
        )
    
    return ConversationHandler.END


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle raw text input."""
    text = update.message.text
    
    if not text or len(text) < 10:
        await update.message.reply_text(
            "❌ Teks terlalu pendek. Kirim data yang lebih lengkap."
        )
        return WAITING_FOR_INPUT
    
    processing_msg = await update.message.reply_text(
        "⏳ Memproses teks...\n"
        "🔄 Menganalisis data...",
        parse_mode='Markdown'
    )
    
    try:
        report = await process_analysis(text)
        
        await processing_msg.edit_text(
            "✅ Analisis selesai!\n"
            "📊 Mengirim laporan...",
            parse_mode='Markdown'
        )
        
        await update.message.reply_text(report, parse_mode='Markdown')
        
        await processing_msg.delete()
        
        logger.info("Analysis completed for text input")
        
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        await update.message.reply_text(
            f"❌ Terjadi kesalahan saat memproses teks:\n{str(e)}\n\n"
            "Coba lagi dengan format yang berbeda."
        )
    
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle cancellation of analysis."""
    await update.message.reply_text(
        "❌ Analisis dibatalkan.\n\n"
        "Ketik /analyze untuk memulai lagi."
    )
    return ConversationHandler.END


async def process_analysis(text: str) -> str:
    """
    Process the analysis pipeline.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Formatted report string
    """
    extractor = DataExtractor()
    risk_assessor = RiskAssessor()
    consistency_checker = ConsistencyChecker()
    behavior_analyzer = BehaviorAnalyzer()
    report_generator = ReportGenerator()
    
    extracted_data = extractor.extract_all(text)
    
    risk_assessment = risk_assessor.assess_overall_risk(extracted_data)
    
    consistency_check = consistency_checker.check_consistency(extracted_data)
    
    behavior_analysis = behavior_analyzer.analyze_behavior(extracted_data)
    
    report = report_generator.generate_full_report(
        extracted_data,
        risk_assessment,
        consistency_check,
        behavior_analysis
    )
    
    return report
