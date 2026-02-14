import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    welcome_message = (
        "👋 Hello! I'm a simple echo bot with metadata.\n\n"
        "Send me any message and I'll reply with confirmation "
        "including metadata about your message."
    )
    await update.message.reply_text(welcome_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages and reply with metadata."""
    message = update.message

    # Extract metadata
    metadata = {
        'message_id': message.message_id,
        'from_user.id': message.from_user.id,
        'from_user.username': message.from_user.username or 'N/A',
        'from_user.first_name': message.from_user.first_name,
        'chat.id': message.chat.id,
        'date': message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else 'N/A',
        'text': message.text or 'N/A'
    }

    # Format response message
    response = (
        "✅ Message received!\n\n"
        "📊 Metadata:\n"
        f"• Message ID: {metadata['message_id']}\n"
        f"• User ID: {metadata['from_user.id']}\n"
        f"• Username: @{metadata['from_user.username']}\n"
        f"• First Name: {metadata['from_user.first_name']}\n"
        f"• Chat ID: {metadata['chat.id']}\n"
        f"• Timestamp: {metadata['date']}\n"
        f"• Text: {metadata['text']}"
    )

    # Reply with confirmation and metadata
    await message.reply_text(response)

    # Log the message
    logger.info(f"Received message from {metadata['from_user.username']} ({metadata['from_user.id']})")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    # Get the bot token from environment variables
    token = os.getenv('BOT_TOKEN')

    if not token or token == 'your_token_here':
        logger.error("BOT_TOKEN is not set in .env file!")
        logger.error("Please get a token from @BotFather and add it to .env")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
