import requests
import pandas as pd
from datetime import datetime


# Fetch data
response = requests.get("https://open.er-api.com/v6/latest/USD")
data = response.json()


# Convert JSON to DataFrame
rates = data["rates"]
date = data["time_last_update_utc"]
rows = [{"date": date, "base": "USD", "target": k, "rate": v} for k, v in rates.items()]
df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])

# Resolve final file path and save
df.to_csv("J:/Projects/currency_pipeline_project_real_api/currency_pipeline_project/data/raw/exchanged_rates.csv", index=False)
print("✅ Fetched and saved real exchange rate data.")
