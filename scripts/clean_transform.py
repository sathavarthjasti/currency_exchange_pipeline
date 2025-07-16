import pandas as pd

import os

raw_path = os.path.join("data", "raw", "exchange_rates.csv")
df = pd.read_csv(raw_path)  
df.dropna(inplace=True)
df["date"] = pd.to_datetime(df["date"])
df["rate"] = df["rate"].astype(float)
df = df[df["target"].isin(["INR", "EUR", "GBP", "CAD"])]
processed_path = os.path.join("data", "processed", "exchange_rates_clean.parquet")
os.makedirs(os.path.dirname(processed_path), exist_ok=True)
df.to_parquet(processed_path, index=False)
print("✅ Cleaned and saved as Parquet.")


