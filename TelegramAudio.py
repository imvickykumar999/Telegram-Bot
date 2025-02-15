import os
import requests
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Environment Variables (Ensure these are set)
BOT_TOKEN = '6165xxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxrx8uo'
GROQ_API_KEY = 'gsk_5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxw9RPf'

if not BOT_TOKEN:
    raise ValueError("Bot token not found! Set the TELEGRAM_BOT_TOKEN environment variable.")

if not GROQ_API_KEY:
    raise ValueError("Groq API key not found! Set the GROQ_API_KEY environment variable.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
# Replace with your actual HTTPS URL for production.
WEBHOOK_URL = "https://free-camel-deadly.ngrok-free.app/webhook"

def set_webhook():
    """Set the Telegram webhook."""
    url = f"{BASE_URL}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    return response.json()

def send_message(chat_id, text):
    """Send a message to the specified Telegram chat."""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def generate_reply(message_text):
    """Generate an AI-based reply using Groq for text messages."""
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

def transcribe_voice(file_name, file_content):
    """Transcribe an audio file using Groq's audio transcription API."""
    try:
        transcription = client.audio.transcriptions.create(
            file=(file_name, file_content),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        return transcription.text
    except Exception as e:
        return "Sorry, I'm having trouble transcribing your audio."

@app.route("/webhook", methods=["POST"])
def webhook():
    """Telegram webhook endpoint that handles text and voice messages."""
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]

        # Check if the update contains a voice message
        if "voice" in message:
            voice = message["voice"]
            file_id = voice["file_id"]

            # Retrieve file information from Telegram
            get_file_url = f"{BASE_URL}/getFile?file_id={file_id}"
            file_info_response = requests.get(get_file_url)
            file_info = file_info_response.json()

            if file_info.get("ok"):
                file_path = file_info["result"]["file_path"]
                download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                file_response = requests.get(download_url)
                file_content = file_response.content

                # Telegram voice messages are usually in OGG format.
                transcription_text = transcribe_voice("voice.ogg", file_content)
                reply_text = generate_reply(transcription_text)
                send_message(chat_id, reply_text)
            else:
                send_message(chat_id, "Sorry, could not retrieve the audio file.")
        
        # If it's a text message, generate an AI-based reply.
        elif "text" in message:
            message_text = message.get("text", "")
            reply_text = generate_reply(message_text)
            send_message(chat_id, reply_text)

    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def set_webhook_route():
    """A simple route to set the webhook manually."""
    result = set_webhook()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
