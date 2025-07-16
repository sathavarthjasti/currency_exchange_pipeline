import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_sms_alert(message):
    dry_run = os.getenv("DRY_RUN_SMS", "false").lower() == "true"

    if dry_run:
        print("💬 [DRY RUN] SMS alert message that would be sent:")
        print(message)
        return

    phone = os.getenv("ALERT_PHONE_NUMBER")
    api_key = os.getenv("TEXTBELT_API_KEY")

    response = requests.post("https://textbelt.com/text", {
        'phone': phone,
        'message': message,
        'key': api_key,
    })

    data = response.json()
    if data.get("success"):
        print("✅ SMS sent successfully!")
    else:
        print("❌ SMS failed:", data)
