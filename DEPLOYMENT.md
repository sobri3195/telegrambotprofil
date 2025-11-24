# 🚀 Deployment Guide

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (obtain from @BotFather on Telegram)
- pip package manager

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd project
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` and add your Telegram Bot Token:

```env
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

### 5. Run the Bot

```bash
python bot.py
```

The bot will start and you'll see:
```
INFO - Starting Data Breach Analyzer Bot...
INFO - Bot is running. Press Ctrl+C to stop.
```

## Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided by BotFather
5. Paste it in your `.env` file

## Testing the Bot

### Run Unit Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_parsers.py

# Run with coverage
pytest --cov=src tests/
```

### Test with Example Script

```bash
python example_usage.py
```

This will demonstrate the analysis pipeline without requiring a Telegram bot.

### Test with Sample Data

```bash
# The sample_data.txt file is provided for testing
# Upload this file to your bot to see a full analysis
```

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/breach-analyzer-bot.service`:

```ini
[Unit]
Description=Telegram Data Breach Analyzer Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable breach-analyzer-bot
sudo systemctl start breach-analyzer-bot
sudo systemctl status breach-analyzer-bot
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t breach-analyzer-bot .
docker run -d --name breach-bot --env-file .env breach-analyzer-bot
```

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

Run:

```bash
docker-compose up -d
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | - | ✅ Yes |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO | No |
| `MAX_FILE_SIZE` | Maximum file size in bytes | 20971520 (20MB) | No |
| `ALLOWED_EXTENSIONS` | Comma-separated file extensions | pdf,txt | No |
| `HIGH_RISK_THRESHOLD` | Threshold for HIGH risk score | 7 | No |
| `MEDIUM_RISK_THRESHOLD` | Threshold for MEDIUM risk score | 4 | No |

## Monitoring

### View Logs

```bash
# If running directly
tail -f bot.log

# If using systemd
sudo journalctl -u breach-analyzer-bot -f

# If using Docker
docker logs -f breach-bot
```

### Health Check

The bot should respond to `/start` command. If it doesn't:

1. Check bot token is valid
2. Check internet connectivity
3. Check logs for errors
4. Verify all dependencies are installed

## Troubleshooting

### Bot doesn't respond

**Issue**: Bot starts but doesn't respond to commands

**Solutions**:
- Verify bot token is correct
- Check if bot is blocked by firewall
- Ensure bot has proper permissions in Telegram

### Import errors

**Issue**: `ModuleNotFoundError` when running bot

**Solutions**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify Python version
python --version  # Should be 3.8+
```

### File parsing errors

**Issue**: Cannot parse PDF files

**Solutions**:
```bash
# Reinstall PyPDF2
pip install --upgrade PyPDF2

# Check file is not corrupted
file document.pdf
```

### Memory issues with large files

**Issue**: Bot crashes with large files

**Solutions**:
- Reduce `MAX_FILE_SIZE` in `.env`
- Increase system memory
- Add swap space

## Security Considerations

1. **Protect Bot Token**: Never commit `.env` file to version control
2. **File Size Limits**: Enforce reasonable limits to prevent abuse
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Data Privacy**: Bot doesn't store data permanently, but ensure secure transmission
5. **Access Control**: Consider restricting bot access to specific users/groups

## Backup and Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run tests after updates
pytest
```

### Monitoring Checklist

- [ ] Bot responds to commands
- [ ] File parsing works correctly
- [ ] Reports generate successfully
- [ ] No errors in logs
- [ ] Server has sufficient resources
- [ ] Dependencies are up to date

## Support

For issues or questions:
1. Check logs for error messages
2. Review this documentation
3. Run test suite: `pytest -v`
4. Check GitHub issues (if applicable)

## License

MIT License - See LICENSE file for details
