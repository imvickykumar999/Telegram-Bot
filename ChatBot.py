import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Bot token (Use an environment variable for security)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token not found! Set the TELEGRAM_BOT_TOKEN environment variable.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Webhook URL (Replace with your actual HTTPS URL)
WEBHOOK_URL = "https://telegramchatbot.pythonanywhere.com/webhook"

# Function to set webhook
def set_webhook():
    url = f"{BASE_URL}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    return response.json()

# Function to send a message
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Function to generate a reply
def generate_reply(message_text):
    responses = {
        "hi": "How can I assist you today?",
        "hello": "Hello! How can I help you?",
        "help": "I'm here to assist you. What do you need?",
        "bye": "Goodbye! Have a great day! 😊",
        "thanks": "You're welcome! Let me know if you need more help. 🙌",
    }
    return responses.get(message_text.lower(), "I'm not sure I understand. Can you rephrase?")

# Webhook endpoint to receive messages
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"].get("text", "")

        # Generate and send response
        reply_text = generate_reply(message_text)
        send_message(chat_id, reply_text)

    return jsonify({"status": "ok"}), 200

# Route to manually set webhook (for testing)
@app.route("/set_webhook", methods=["GET"])
def set_webhook_route():
    result = set_webhook()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
