import os
import logging
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


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001 (unused context)
    """Handle the /start command."""
    message = update.message
    assert message is not None  # CommandHandler guarantees message exists
    welcome_message = (
        "👋 Hello! I'm a simple echo bot with metadata.\n\n"
        "Send me any message or location and I'll reply with confirmation "
        "including metadata about your message."
    )
    await message.reply_text(welcome_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001 (unused context)
    """Handle incoming text messages and reply with metadata."""
    message = update.message
    assert message is not None  # filters.TEXT guarantees message exists
    assert message.from_user is not None
    assert message.chat is not None

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


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001 (unused context)
    """Handle location messages and reply with location metadata."""
    message = update.message
    assert message is not None  # filters.LOCATION guarantees message exists
    assert message.from_user is not None
    assert message.chat is not None
    assert message.location is not None

    # Extract location metadata
    metadata = {
        'message_id': message.message_id,
        'from_user.id': message.from_user.id,
        'from_user.username': message.from_user.username or 'N/A',
        'from_user.first_name': message.from_user.first_name,
        'chat.id': message.chat.id,
        'date': message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else 'N/A',
        'latitude': message.location.latitude,
        'longitude': message.location.longitude,
        'heading': message.location.heading or 'N/A',
        'horizontal_accuracy': message.location.horizontal_accuracy or 'N/A'
    }

    # Format response message
    response = (
        "📍 Location received!\n\n"
        "📊 Metadata:\n"
        f"• Message ID: {metadata['message_id']}\n"
        f"• User ID: {metadata['from_user.id']}\n"
        f"• Username: @{metadata['from_user.username']}\n"
        f"• First Name: {metadata['from_user.first_name']}\n"
        f"• Chat ID: {metadata['chat.id']}\n"
        f"• Timestamp: {metadata['date']}\n\n"
        f"🌍 Location:\n"
        f"• Latitude: {metadata['latitude']}\n"
        f"• Longitude: {metadata['longitude']}\n"
        f"• Heading: {metadata['heading']}\n"
        f"• Accuracy: {metadata['horizontal_accuracy']} m"
    )

    # Reply with confirmation and metadata
    await message.reply_text(response)

    # Log the message
    logger.info(f"Received location from {metadata['from_user.username']} ({metadata['from_user.id']})")


async def error_handler(update: object | None, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")  # type: ignore[attr-defined]


def main() -> None:
    """Start the bot with webhook."""
    # Get configuration from environment variables
    token = os.getenv('BOT_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL')
    webhook_port = int(os.getenv('WEBHOOK_PORT', '8443'))
    webhook_path = os.getenv('WEBHOOK_PATH', '/telegram-webhook')
    listen_address = os.getenv('LISTEN_ADDRESS', '0.0.0.0')

    # Validate required configuration
    if not token or token == 'your_token_here':
        logger.error("BOT_TOKEN is not set in .env file!")
        logger.error("Please get a token from @BotFather and add it to .env")
        return

    if not webhook_url:
        logger.error("WEBHOOK_URL is not set in .env file!")
        logger.error("Please set your webhook URL (e.g., https://yourdomain.com)")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_error_handler(error_handler)

    # Start the bot with webhook
    logger.info(f"Starting webhook on port {webhook_port}")
    logger.info(f"Webhook URL: {webhook_url}{webhook_path}")

    # Run the webhook server
    application.run_webhook(
        listen=listen_address,
        port=webhook_port,
        url_path=webhook_path,
        webhook_url=f"{webhook_url}{webhook_path}",
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == '__main__':
    main()
