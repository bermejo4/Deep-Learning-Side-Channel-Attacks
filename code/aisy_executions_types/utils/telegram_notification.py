import os
import requests
from dotenv import load_dotenv

# Loanding env variables from .env
load_dotenv()

# Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def telegram_notification(MESSAGE):
    # sending notification to Telegram
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={'chat_id': CHAT_ID, 'text': MESSAGE}
    )

    if response.status_code == 200:
        print("message sent")
    else:
        print("Error sending message.")
