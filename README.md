# tg-bot

Simple Telegram bot that accepts messages and returns confirmation with metadata.

## Features

- Echo bot functionality with message confirmation
- Displays metadata for each received message:
  - Message ID
  - User ID
  - Username
  - First Name
  - Chat ID
  - Timestamp
  - Message text
- Built with modern async/await support

## Setup

### 1. Get Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send the command `/newbot`
3. Follow the prompts to choose a name and username for your bot
4. Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. (Optional) Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Bot Token

1. Create a `.env` file in the project directory
2. Add your bot token:

```env
BOT_TOKEN=your_actual_token_here
```

Replace `your_actual_token_here` with the token you received from BotFather.

### 5. Run the Bot

```bash
python bot.py
```

You should see a message like:
```
Bot is starting...
```

### 6. Test the Bot

1. Open Telegram and search for your bot by its username
2. Send `/start` to see the welcome message
3. Send any text message
4. Receive a confirmation with message metadata

## Project Structure

```
tg-bot/
├── bot.py              # Main bot logic
├── requirements.txt    # Python dependencies
├── .env               # Bot token configuration (not in git)
└── README.md          # This file
```

## Dependencies

- `python-telegram-bot==21.0` - Modern Telegram bot API wrapper with async support
- `python-dotenv==1.0.0` - Environment variable management

## Usage

The bot responds to:
- `/start` - Welcome message with instructions
- Any text message - Confirmation with metadata

## Stopping the Bot

Press `Ctrl+C` in the terminal where the bot is running.
