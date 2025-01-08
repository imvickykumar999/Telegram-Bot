# Get Chat ID:

```python
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Replace this with your bot's token
BOT_TOKEN = "YOUR_BOT_TOKEN"

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Extract and send the chat ID as a JSON response."""
    chat_id = update.message.chat_id
    print(f"Chat ID: {chat_id}")
    # Send JSON response back to the user
    await update.message.reply_text(f"{{\"chat_id\": {chat_id}}}")

def main():
    """Main function to set up the bot."""
    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a handler to listen to all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_chat_id))

    # Run the bot
    print("Bot is running. Send a message to the bot to get the chat ID.")
    application.run_polling()

if __name__ == "__main__":
    main()
```

### Changes Made:
1. **Replaced `await application.start()` and `await application.idle()`**:
   - Instead of manually handling the event loop, I used `application.run_polling()` to start polling and keep the bot running.
2. **Synchronous `main()`**:
   - The `main()` function is now synchronous since `application.run_polling()` manages the loop automatically.

### How to Run:
1. Save the script.
2. Install or ensure you have the latest version of the library:
   ```bash
   pip install python-telegram-bot --upgrade
   ```
3. Run the script:
   ```bash
   python3 cliend_id.py
   ```
4. Send a message to your bot, and it will reply with the `chat_id` in JSON format.
