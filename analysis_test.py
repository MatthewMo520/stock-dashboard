import pandas as pd
import yfinance as yf
import plotly.express as px

df = yf.download("AAPL", period="6mo", interval="1d").reset_index()

df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
df.rename(columns={'Close AAPL': 'Close', 'Date': 'Date'}, inplace=True)

print(df.head())

df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()
df['Daily Change %'] = df['Close'].pct_change() * 100

print(df[['Date', 'Close', 'MA50', 'MA200', 'Daily Change %']].tail())

fig = px.line(df, x='Date', y =['Close', 'MA50', 'MA200'], title='AAPL Stock Price with Moving Averages')
fig.show()