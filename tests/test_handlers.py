"""
Tests for Telegram bot handlers.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.handlers import start_handler, help_handler, author_handler


@pytest.mark.asyncio
class TestStartHandler:
    """Test start command handler."""
    
    async def test_start_handler_new_user(self):
        """Test start handler for new users."""
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_text = AsyncMock()
        
        await start_handler(update, context)
        
        update.message.reply_text.assert_called_once()
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "Congratulations" in message
        assert "51" in message
        assert "Author Information" in message
    
    async def test_start_handler_returning_user(self):
        """Test start handler for returning users."""
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_text = AsyncMock()
        
        await start_handler(update, context)
        await start_handler(update, context)
        
        assert update.message.reply_text.call_count == 2
        second_call_args = update.message.reply_text.call_args
        message = second_call_args[0][0]
        
        assert "Welcome back" in message


@pytest.mark.asyncio
class TestHelpHandler:
    """Test help command handler."""
    
    async def test_help_handler(self):
        """Test help handler displays usage information."""
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_text = AsyncMock()
        
        await help_handler(update, context)
        
        update.message.reply_text.assert_called_once()
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "Help" in message
        assert "Email Search" in message
        assert "Phone Search" in message
        assert "Author Information" in message
        assert "/author" in message


@pytest.mark.asyncio
class TestAuthorHandler:
    """Test author command handler."""
    
    async def test_author_handler(self):
        """Test author handler displays developer information."""
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = AsyncMock()
        
        await author_handler(update, context)
        
        update.message.reply_text.assert_called_once()
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "Muhammad Sobri Maulana" in message
        assert "muhammadsobrimaulana31@gmail.com" in message
        assert "github.com/sobri3195" in message
    
    async def test_author_handler_contains_social_media(self):
        """Test author handler includes social media links."""
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = AsyncMock()
        
        await author_handler(update, context)
        
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "youtube.com/@muhammadsobrimaulana6013" in message
        assert "t.me/winlin_exploit" in message
        assert "tiktok.com/@dr.sobri" in message
        assert "muhammadsobrimaulana.netlify.app" in message
    
    async def test_author_handler_contains_donation_links(self):
        """Test author handler includes donation links."""
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = AsyncMock()
        
        await author_handler(update, context)
        
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "lynk.id/muhsobrimaulana" in message
        assert "trakteer.id" in message
        assert "gumroad.com" in message
        assert "karyakarsa.com" in message
        assert "nyawer.co" in message
    
    async def test_author_handler_contains_whatsapp_group(self):
        """Test author handler includes WhatsApp group link."""
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = AsyncMock()
        
        await author_handler(update, context)
        
        call_args = update.message.reply_text.call_args
        message = call_args[0][0]
        
        assert "chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl" in message
    
    async def test_author_handler_markdown_format(self):
        """Test author handler uses markdown formatting."""
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = AsyncMock()
        
        await author_handler(update, context)
        
        call_args = update.message.reply_text.call_args
        kwargs = call_args[1]
        
        assert kwargs.get('parse_mode') == 'Markdown'
