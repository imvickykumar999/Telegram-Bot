import requests, os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Environment Variables (Ensure these are set)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Bot token not found! Set the TELEGRAM_BOT_TOKEN environment variable.")

if not GROQ_API_KEY:
    raise ValueError("Groq API key not found! Set the GROQ_API_KEY environment variable.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

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

# Function to generate AI-based reply using Groq
def generate_reply(message_text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.2-1b-preview",
            messages=[{"role": "user", "content": message_text}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return "Sorry, I'm having trouble processing your request."

# Webhook endpoint to receive messages
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"].get("text", "")

        # Generate and send AI-based response
        reply_text = generate_reply(message_text)
        send_message(chat_id, reply_text)

    return jsonify({"status": "ok"}), 200

# Route to manually set webhook (for testing)
@app.route("/", methods=["GET"])
def set_webhook_route():
    result = set_webhook()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
