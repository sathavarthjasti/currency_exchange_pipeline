import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv("config/secrets.env")

df = pd.read_parquet("data/processed/exchange_rates_clean.parquet")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

cursor = conn.cursor()
cursor.execute("""
CREATE OR REPLACE TABLE EXCHANGE_RATES (
    DATE DATE,
    BASE STRING,
    TARGET STRING,
    RATE FLOAT
)
""")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO EXCHANGE_RATES (DATE, BASE, TARGET, RATE) VALUES (%s, %s, %s, %s)",
        (row["date"], row["base"], row["target"], row["rate"])
    )

print("✅ Data loaded into Snowflake.")
cursor.close()
conn.close()
