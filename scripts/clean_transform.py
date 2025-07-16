import pandas as pd

df = pd.read_csv("J:/Projects/currency_pipeline_project_real_api/currency_pipeline_project/data/raw/exchanged_rates.csv")
df.dropna(inplace=True)
df["date"] = pd.to_datetime(df["date"])
df["rate"] = df["rate"].astype(float)
df = df[df["target"].isin(["INR", "EUR", "GBP", "CAD"])]
df.to_parquet("J:/Projects/currency_pipeline_project_real_api/currency_pipeline_project/data/processed/exchanged_rates_clean.parquet", index=False)
print("✅ Cleaned and saved as Parquet.")
