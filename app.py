import os
import requests
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Bot token (Use an environment variable for security)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token not found! Set the TELEGRAM_BOT_TOKEN environment variable.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Webhook URL (Replace with your actual HTTPS URL)
WEBHOOK_URL = "https://animated-space-carnival-4wpx7rpqx7pcx-8080.app.github.dev/webhook"

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

# Function to generate a response from Ollama
def generate_reply_from_ollama(message_text):
    try:
        # Run Ollama as a subprocess
        process = subprocess.Popen(
            # ["ollama", "run", "blogforge"],
            ["ollama", "run", "llama3.2:1b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send user message to Ollama
        output, error = process.communicate(input=message_text, timeout=1000)
        print('output : ', output)

        # if error:
        #     print("🔴 Ollama Error:", error)

        return output.strip() if output else "🤖 No response from AI."

    except Exception as e:
        print(f"🔴 Exception in Ollama subprocess: {str(e)}")
        return f"⚠️ Error communicating with Ollama: {str(e)}"

# Webhook endpoint to receive messages
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"].get("text", "")
        print('📩 Received Message:', message_text)

        # Generate response using Ollama
        reply_text = generate_reply_from_ollama(message_text)
        print('🤖 AI Reply:', reply_text)

        # Send the response
        send_message(chat_id, reply_text)

    return jsonify({"status": "ok", "message" : reply_text}), 200

# Route to manually set webhook (for testing)
@app.route("/set_webhook", methods=["GET"])
def set_webhook_route():
    result = set_webhook()
    return jsonify(result)

# https://animated-space-carnival-4wpx7rpqx7pcx-8080.app.github.dev/set_webhook
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
