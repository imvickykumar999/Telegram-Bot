import requests
import time

# Replace with your bot token (Do not share publicly)
BOT_TOKEN = "xxxxx:xxxxxxxxxxxxxxxxxxxxxxxx"

# Function to get latest messages
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 30}  # Long polling
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response.json()

# Function to generate a response based on received message
def generate_reply(message_text):
    replies = {
        "hi": "How can I help you?",
        "hello": "Hey there! How can I assist you?",
        "help": "Sure! Please tell me what you need help with.",
    }
    return replies.get(message_text.lower(), "Sorry, I didn't understand. Can you rephrase?")

# Main loop to listen for new messages
def run_bot():
    last_update_id = None

    print("Bot is running... Listening for messages!")

    while True:
        updates = get_updates(last_update_id)

        if updates.get("result"):
            for item in updates["result"]:
                try:
                    update_id = item["update_id"]
                    message_text = item["message"]["text"]
                    chat_id = item["message"]["from"]["id"]
                    user_name = item["message"]["from"].get("username", "Unknown")

                    # Generate an appropriate reply
                    reply_text = generate_reply(message_text)

                    # Send reply
                    send_message(chat_id, reply_text)

                    # Print conversation to the command line
                    print("\n📩 New Message Received!")
                    print(f"👤 User ({user_name}, ID: {chat_id}): {message_text}")
                    print(f"🤖 Bot Reply: {reply_text}")

                    # Update last processed message
                    last_update_id = update_id + 1
                
                except KeyError:
                    # Skip non-text messages (like stickers, images, etc.)
                    continue

        time.sleep(2)  # Delay to prevent API spam

# Run the bot
if __name__ == "__main__":
    run_bot()

