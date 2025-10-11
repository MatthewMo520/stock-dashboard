import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.title("Stock Dashboard")

#---- USER INPUT ----#
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, TSLA, AMZN):", "AAPL")
period = st.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"])
interval = st.selectbox("Select interval:", ["1d", "1wk", "1mo"])

#----DOWNLOAD DATA ----#
df = yf.download(ticker, period=period, interval=interval).reset_index()

#----FLATTEN COLUMNS ----#
df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

if f'Close {ticker}' in df.columns:
    df.rename(columns={f'Close {ticker}': 'Close', 'Date': 'Date'}, inplace=True)
if 'Date ' in df.columns:
    df.rename(columns={'Date ': 'Date'}, inplace=True)

#----CALCULATING MOVING AVERAGES AND DAILY CHANGES----#
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()
df['Daily Change %'] = df['Close'].pct_change() * 100

#----DISPLAY CHART----#
fig = px.line(df, x='Date', y=['Close', 'MA50', 'MA200'], title=f'{ticker} Stock Price with Moving Averages')
st.plotly_chart(fig)

#----DISPLAY DATA TABLE----#
st.subheader("Recent Data")
st.dataframe(df.tail())