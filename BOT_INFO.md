# 🤖 Bot Information

## Telegram Bot Details

This project is connected to a live Telegram bot with the following details:

### Bot Credentials

- **Bot Name**: Pegasus Profil Bot
- **Bot Username**: [@pegasus_profil_bot](https://t.me/pegasus_profil_bot)
- **Bot Link**: https://t.me/pegasus_profil_bot
- **Bot Token**: `8573088419:AAEWZCeDvY9srasrAXprVOPDzinPJWxjGVI`

### Bot Status

✅ **Bot is registered and ready to use**

The bot token has been configured in the `.env` file and is ready for deployment.

## Quick Start

To start using the bot immediately:

```bash
# 1. Activate virtual environment (if not already active)
source venv/bin/activate

# 2. Run the bot
python bot.py
```

The bot will start and be available at: https://t.me/pegasus_profil_bot

## Security Reminders

⚠️ **IMPORTANT**: 
- Keep the bot token secure and private
- Never share the token publicly
- The `.env` file is already in `.gitignore` to prevent accidental commits
- If the token is compromised, regenerate it via @BotFather

## Bot Features

Once running, users can interact with the bot using:

- `/start` - Get 51 free credits and welcome message
- `/help` - View usage instructions and examples
- `/author` - View author information and donation links
- **Direct messages** - Send queries to search for data breaches

### Supported Search Types

1. **Email**: `example@gmail.com`, `example@`, `@gmail.com`
2. **Phone**: `+79024196473`, `79024196473`
3. **Car**: `O999МУ777` (plate), `XTA21150053965897` (VIN)
4. **IP Address**: `127.0.0.1`
5. **Name**: `Muhammad Sobri Maulana`
6. **Combo**: `Sergio 79024196473`, `Ivan Kuznetsov 09/18/1991`
7. **Multi-query**: Multiple queries, one per line

## Configuration

The bot is configured with these default settings (can be changed in `.env`):

- Initial credits: 51
- Cost per search: 1 credit
- Max multi-query: 10 searches per message
- Log level: INFO
- Website URL: https://scanyour.name

## Customizing the Bot

You can customize the bot via @BotFather:

1. `/setdescription` - Set bot description
2. `/setabouttext` - Set about text
3. `/setuserpic` - Set profile picture
4. `/setcommands` - Set command list
5. `/setname` - Change bot name (if needed)

### Suggested Commands List

Send to @BotFather with `/setcommands`:

```
start - Mulai bot dan dapatkan kredit gratis
help - Panduan penggunaan bot
author - Informasi developer dan donasi
```

## Monitoring

To monitor the bot:

```bash
# View real-time logs
tail -f bot.log

# Check if bot is running
ps aux | grep bot.py

# Stop the bot
pkill -f bot.py
```

## Support

For any issues:

1. Check the logs: `tail -f bot.log`
2. Verify token is correct in `.env`
3. Ensure all dependencies are installed
4. Test with `/start` command in Telegram

## Developer Information

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

- Email: muhammadsobrimaulana31@gmail.com
- GitHub: [github.com/sobri3195](https://github.com/sobri3195)
- Telegram: [@winlin_exploit](https://t.me/winlin_exploit)

## Documentation

For more detailed information, see:

- `README.md` - Full project documentation
- `DEPLOYMENT.md` - Deployment guide
- `CHANGELOG_AUTHOR_INFO.md` - Author information changelog
