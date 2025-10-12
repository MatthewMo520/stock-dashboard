import yfinance as yf
df = yf.download("AAPL", period="6mo", interval="1d")
print(df.head())
print(df.columns)