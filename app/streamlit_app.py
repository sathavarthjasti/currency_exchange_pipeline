import streamlit as st
import pandas as pd
import altair as alt

# Load processed data
df = pd.read_parquet("data/processed/exchanged_rates_clean.parquet")

# Title
st.title("💱 USD Exchange Rate Tracker")

# Select currency
currencies = ["INR", "EUR", "GBP", "JPY", "CAD", "AUD"]
selected = st.multiselect("Choose currencies to visualize", currencies, default=["INR", "EUR"])

# Filter data
filtered_df = df[df["target"].isin(selected)]

# Chart
st.subheader("📈 Exchange Rate Over Time")
chart = (
    alt.Chart(filtered_df)
    .mark_line(point=True)
    .encode(
        x="date:T",
        y="rate:Q",
        color="target:N",
        tooltip=["date:T", "target:N", "rate:Q"]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

# 📣 Alerts
st.subheader("🚨 Alerts")

thresholds = {
    "INR": 85.0,
    "EUR": 0.90,
    "JPY": 150.0,
}

latest_df = filtered_df.sort_values("date").groupby("target").tail(1)

for _, row in latest_df.iterrows():
    curr = row["target"]
    rate = row["rate"]
    date = row["date"].strftime("%Y-%m-%d")

    if curr in thresholds:
        if rate < thresholds[curr]:
            st.error(f"{date} – USD to {curr} is **{rate:.2f}**, which is **below threshold {thresholds[curr]}**")
        else:
            st.success(f"{date} – USD to {curr} is {rate:.2f} ✅")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
