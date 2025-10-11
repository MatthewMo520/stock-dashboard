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
ma_options = st.multiselect("Select moving averages to display:", [20, 50, 100, 200], default=[50, 200])
for ma in ma_options:
    df[f'MA{ma}'] = df['Close'].rolling(window=ma).mean()
df['Daily Change %'] = df['Close'].pct_change() * 100

#----PREPARE COLUMNS FOR PLOTTING----#
plot_cols = ['Close']
for ma in ma_options:
    plot_cols.append(f'MA{ma}')

#----DISPLAY CHART----#
fig = px.line(df, x='Date', y=plot_cols, title=f'{ticker} Stock Price with Moving Averages')

#----COLUMN LAYOUT----#
col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Recent Data")
    
    #----COLOUR CHANGES----#
    def daily_change_colour(val):
        if val > 0:
            colour = 'green'
        elif val < 0:
            colour = 'red'
        else:
            colour = 'black'
        return f'color: {colour}'

    #----DISPLAY DATA TABLE----#
    st.dataframe(df.tail().style.applymap(daily_change_colour, subset=['Daily Change %']))

    #----CONVERT TO CSV----#
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{ticker}_data.csv',
        mime='text/csv',
    )