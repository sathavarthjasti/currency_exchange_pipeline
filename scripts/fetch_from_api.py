import requests
import pandas as pd
import os
from datetime import datetime
from send_sms_textbelt import send_sms_alert
from dotenv import load_dotenv

load_dotenv()

# ======= Step 1: Fetch Data =======
response = requests.get("https://open.er-api.com/v6/latest/USD")
data = response.json()

# ======= Step 2: Convert JSON to DataFrame =======
rates = data["rates"]
date = data["time_last_update_utc"]
rows = [{"date": date, "base": "USD", "target": k, "rate": v} for k, v in rates.items()]
df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])

# Create output directory if it doesn't exist
output_dir = os.path.join("data", "raw")
os.makedirs(output_dir, exist_ok=True)

# Save CSV using relative path
output_path = os.path.join(output_dir, "exchange_rates.csv")
df.to_csv(output_path, index=False)

print(f"✅ Fetched and saved real exchange rate data at {output_path}")

# ======= Step 4: Threshold Check =======
ALERT_THRESHOLD = {
    "INR": 88.0
}

def check_thresholds(df):
    alerts = []
    row = df[df["target"] == "INR"]
    if not row.empty:
        rate = float(row["rate"].values[0])
        print(rate)
        if rate > 90.00:
            alerts.append(f"🚨 Exchange Alert: USD to INR is {rate:.2f} (above 99.00)")
    return alerts


# ======= Step 5: Send Alert if Needed =======
alerts = check_thresholds(df)
if alerts:
    message = "\n".join(alerts)
    send_sms_alert(message)  # Let this function decide based on DRY_RUN_SMS
