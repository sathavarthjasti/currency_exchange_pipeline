import streamlit as st
import pandas as pd
import altair as alt

# Load Data
df = pd.read_parquet("data/processed/exchange_rates_clean.parquet")

# Sidebar filters
st.sidebar.title("💱 Currency Filter")
selected_currency = st.sidebar.selectbox("Select currency", df["target"].unique())

# Filtered data
filtered = df[df["target"] == selected_currency]

# Title
st.title("📊 USD Exchange Rate Tracker")
st.write(f"Showing rates for **USD → {selected_currency}**")

# Line Chart
chart = alt.Chart(filtered).mark_line(point=True).encode(
    x="date:T",
    y="rate:Q"
).properties(width=700, height=400)

st.altair_chart(chart)

# Latest value
latest = filtered.sort_values("date", ascending=False).iloc[0]
st.metric(label="Latest Rate", value=f"{latest['rate']:.4f}", delta=None)
