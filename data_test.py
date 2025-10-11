import yfinance as yf
df = yf.download("AAPL", period="6mo", interval="1d")
print("head:",df.head())
print("col", df.columns)