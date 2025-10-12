import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

#----PAGE CONFIGURATION ----#
st.set_page_config(page_title="Stock Dashboard", initial_sidebar_state="expanded")
st.title("Stock Dashboard")

#---- USER INPUT ----#
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, TSLA, AMZN):", "AAPL")
period = st.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=3)
interval = st.selectbox("Select interval:", ["1d", "1wk", "1mo"])

#----DOWNLOAD DATA ----#
df = yf.download(ticker, period=period, interval=interval).reset_index()

#----CHECK IF DATA IS EMPTY ----#
if df.empty:
    st.error("No data found for the given ticker. Please check the ticker symbol and try again.")
    st.stop()

#----FLATTEN COLUMNS ----#
df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

if f'Close {ticker}' in df.columns:
    df.rename(columns={f'Close {ticker}': 'Close', 'Date': 'Date'}, inplace=True)
if 'Date ' in df.columns:
    df.rename(columns={'Date ': 'Date'}, inplace=True)


#----CALCULATING MOVING AVERAGES AND DAILY CHANGES----#
ma_options = st.multiselect("Select moving averages to display:", [20, 50, 100, 200], default=[50, 200])

#----CHECK IF PERIOD TOO SHORT FOR MOVING AVERAGES ----#
min_ma = max(ma_options) if ma_options else 0
if len(df) < min_ma:
    st.warning(f"Not enough data to compute the selected moving averages. Please select a longer period or fewer moving averages.")
    st.stop()

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
col1, col2 = st.columns([7, 3])
with col1:
    st.plotly_chart(fig, use_container_width=True)
    fig.update_traces(mode='lines+markers', hovertemplate='Date: %{x}<br>Price: %{y:.2f}')

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
    st.dataframe(
        df.tail(7).style.applymap(daily_change_colour, subset=['Daily Change %']), 
        use_container_width=True, 
        height = 285
        )

    #----CONVERT TO CSV----#
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{ticker}_data.csv',
        mime='text/csv',
    )

st.markdown("---")

#----PERFORMANCED SUMMARY----#
st.subheader("Performance Summary")
if not df['Daily Change %'].dropna().empty:

    #----CALCULATE METRICS----#
    avg_daily_return = df['Daily Change %'].mean()
    volatility = df['Daily Change %'].std()
    total_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
    rolling_max = df['Close'].cummax()
    df['Drawdown %'] = ((df['Close'] - rolling_max) / rolling_max) * 100
    max_drawdown = df['Drawdown %'].min()

    #----DRAWDOWN CHART----#
    drawdown_fig = px.area(
        df,
        x = 'Date',
        y = 'Drawdown %',
        title = f'{ticker} Drawdown Over Time',
        color_discrete_sequence=['red']
    )
    drawdown_fig.update_traces(fill='tozeroy')
    drawdown_fig.update_yaxes(title_text='Drawdown (%)')
    st.plotly_chart(drawdown_fig, use_container_width=True)

    #----DISPLAY METRICS IN COLUMNS----#
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Average Daily Return (%)", value=f"{avg_daily_return:.2f}%")
    col2.metric(label="Volatility (Std Dev of Daily Return %)", value=f"{volatility:.2f}%")
    col3.metric(label="Total Return (%)", value=f"{total_return:.2f}%")
    col4.metric(label="Max Drawdown (%)", value=f"{max_drawdown:.2f}%")

    #----CUMULATIVE RETURN CHART----#
    df['Cumulative Return %'] = ((1 + df['Close'].pct_change()).cumprod() - 1) * 100
    cumreturn_fig = px.line(
        df,
        x='Date',
        y='Cumulative Return %',
        title=f'{ticker} Cumulative Return Over Time'
    )
    st.plotly_chart(cumreturn_fig, use_container_width=True)

    #----HOVER INFO----#
    cumreturn_fig.update_traces(mode='lines+markers', hovertemplate='Date: %{x}<br>Cumulative Return: %{y:.2f}%')
    drawdown_fig.update_traces(mode='lines+markers', hovertemplate='Date: %{x}<br>Drawdown: %{y:.2f}%')

else:
    st.write("Not enough data to calculate performance metrics.")
