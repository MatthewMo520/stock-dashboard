# Stock Dashboard

Streamlit web application displaying historical data on a given stock

## Features

- display information on any given stock (given the ticker)
- able to select period, interval and which moving averages
- displays graph with moving averages and the closing price of the given interval and period
- displays the most recent 5 data points given interval including close, high, low, open, volume, moving average and daily percent change
- CSV download avaliable which downloads data of the given timeframe
- displays performance summary including :
    - daily drawdown graph
    - average daily return, volatility, total return and max drawdown of the period
    - cumulative return over the period

## Edge Cases:

- gives error message if the ticker symbol is not found
- gives warning if the moving average cannot be found due to the not having enough data/ time period too short

## Tools 

- Streamlit
- yfinance
- Plotly
- pandas

## How to run:

install the requirements:
pip install -r requirements.txt

run the program:
streamlit run app.py

Using the program:

1. Select stock by entering the ticker, e.g., AAPL
2. Select period fromdrop down, e.g., 6mo
3. Select interval from drop down, e.g., 1d
4. Select moving averages from multiselect, e.g., 50 and 200

To download CSV: click download CSV button


