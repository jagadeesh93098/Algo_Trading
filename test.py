import yfinance as yf
from datetime import datetime, timedelta

# Calculate the start date as 30 days ago from today
e_d = datetime.today()-timedelta(days=1)
end_date = e_d.strftime('%Y-%m-%d')
start_date = (e_d - timedelta(days=1)).strftime('%Y-%m-%d')

# Fetch historical intraday data for Jio Platforms Limited for the last 30 days
jiofin_data = yf.download("JIOFIN.NS", start=start_date, end=end_date, interval="1m")

print(jiofin_data.head())
