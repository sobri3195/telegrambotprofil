"""
Telegram bot command handlers.
"""

from .start import start_handler
from .help import help_handler
from .analyze import analyze_handler, document_handler, text_handler

__all__ = [
    'start_handler',
    'help_handler',
    'analyze_handler',
    'document_handler',
    'text_handler',
]
