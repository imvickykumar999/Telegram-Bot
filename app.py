import os
import requests
from flask import Flask, request, jsonify
import subprocess
import threading

# set TELEGRAM_BOT_TOKEN=6165xxxx:xxxxxxxxxxxxxxxxxxxxxxzrx8uo
# loclx tunnel http --to localhost:8000

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token not found! Set the TELEGRAM_BOT_TOKEN environment variable.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Webhook URL (Replace with your actual HTTPS URL)
# WEBHOOK_URL = "https://monkey-related-kangaroo.ngrok-free.app/webhook"
WEBHOOK_URL = "https://lzjdpqykrs.loclx.io/webhook"

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
        output, error = process.communicate(input=message_text,
            # timeout=1000
        )
        print('🤖 AI output : ', output)
        return output.strip() if output else "https://blogforge.pythonanywhere.com/"

    except Exception as e:
        print(f"🔴 Exception in Ollama subprocess: {str(e)}")
        return f"⚠️ Error communicating with Ollama: {str(e)}"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    # Send a quick response to Telegram before processing
    response = jsonify({"status": "ok"})
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"].get("text", "")

        # Process the message in the background
        threading.Thread(target=process_message, args=(chat_id, message_text)).start()

    return response, 200

def process_message(chat_id, message_text):
    reply_text = generate_reply_from_ollama(message_text)
    send_message(chat_id, reply_text)

# Route to manually set webhook (for testing)
@app.route("/", methods=["GET"])
def set_webhook_route():
    result = set_webhook()
    return jsonify(result)

# https://monkey-related-kangaroo.ngrok-free.app
if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=8000, 
        debug=True
    )
