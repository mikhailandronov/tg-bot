# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in polling mode (for development)
python bot.py

# Run in webhook mode (for production/testing)
python bot-webhook.py
```

## Architecture

This project implements a Telegram bot with **two deployment modes**, each in a separate file:

- **[bot.py](bot.py)** - Polling mode: Uses `application.run_polling()` to continuously poll Telegram servers. Suitable for local development and testing.
- **[bot-webhook.py](bot-webhook.py)** - Webhook mode: Uses `application.run_webhook()` to receive updates via HTTP callback. Suitable for production deployment with a VPS/domain.

Both files share identical handler logic but differ only in the startup method.

### Core Handler Functions

Both implementations use these async handlers (add new commands following this pattern):

- `start_command()` - Handles `/start` command
- `handle_message()` - Handles text messages (non-commands)
- `error_handler()` - Global error handling

### Type Safety Patterns

The webhook variant ([bot-webhook.py](bot-webhook.py:18-22)) demonstrates proper type narrowing with assertions:

```python
message = update.message
assert message is not None  # CommandHandler guarantees message exists
assert message.from_user is not None
assert message.chat is not None
```

Use assertions after accessing optional types to satisfy type checkers and document invariants.

### Handler Registration Pattern

Handlers are registered via the Application builder:

```python
application = Application.builder().token(token).build()
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_error_handler(error_handler)
```

## Environment Configuration

Create a `.env` file in the project root with:

**Required for both modes:**
- `BOT_TOKEN` - Telegram bot token from [@BotFather](https://t.me/BotFather)

**Required for webhook mode:**
- `WEBHOOK_URL` - Full domain URL (e.g., `https://yourdomain.com`)
- `WEBHOOK_PORT` - Port for webhook server (default: `8443`)
- `WEBHOOK_PATH` - Webhook endpoint path (default: `/telegram-webhook`)
- `LISTEN_ADDRESS` - Listen address (default: `0.0.0.0`)

See [README.md](README.md) for basic setup or [WEBHOOK_SETUP.md](WEBHOOK_SETUP.md) for complete production deployment guide.

## Code Patterns to Follow

### Type Annotations
All handlers must use proper type annotations from `telegram.ext`:
```python
async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
```

### Message Filters
Use `filters` combined with bitwise operators:
- `filters.TEXT & ~filters.COMMAND` - Text messages excluding commands
- `filters.PHOTO | filters.VOICE` - Photos or voice messages

### Logging
Configure logging at module level:
```python
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Response Formatting
The bot uses emoji prefixes for visual clarity:
- `👋` - Greetings
- `✅` - Confirmations
- `📊` - Metadata/information
- `•` - Bullet points

## Dependencies

- `python-telegram-bot==21.0` - Async Telegram Bot API wrapper
- `python-dotenv==1.0.0` - Environment variable management
