import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.title("📈 Stock Dashboard")

# --- User input ---
ticker = st.text_input("Enter a stock ticker:", "AAPL")

# --- Download data ---
df = yf.download(ticker, period="6mo", interval="1d").reset_index()

# Flatten columns in case yfinance returns multi-index
df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
if f'Close {ticker}' in df.columns:
    df.rename(columns={f'Close {ticker}': 'Close', 'Date ': 'Date'}, inplace=True)

# Quick check: make sure dataframe has data
st.write("### Raw Data Preview")
st.dataframe(df.head())

# --- Compute moving averages ---
df['MA50'] = df['Close'].rolling(50).mean()
df['MA200'] = df['Close'].rolling(200).mean()

# --- Plot chart ---
fig = px.line(df, x='Date', y=['Close','MA50','MA200'], title=f"{ticker} Price with Moving Averages")
st.plotly_chart(fig)

st.write("✅ Dashboard loaded successfully")