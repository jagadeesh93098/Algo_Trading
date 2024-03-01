import yfinance as yf
from datetime import datetime, timedelta

# Calculate the start date as 30 days ago from today
e_d = datetime.today()-timedelta(days=1)
end_date = e_d.strftime('%Y-%m-%d')
start_date = (e_d - timedelta(days=7)).strftime('%Y-%m-%d')

# Fetch historical intraday data for Jio Platforms Limited for the last 30 days
jiofin_data = yf.download("JIOFIN.NS", start=start_date, end=end_date, interval="1m")

for i in range(0,4):
    e_d=start_date
    start_date = (e_d - timedelta(days=7)).strftime('%Y-%m-%d')

    # Fetch historical intraday data for Jio Platforms Limited for the last 30 days
    df_temp = yf.download("JIOFIN.NS", start=start_date, end=end_date, interval="1m")
    jiofin_data=pd.concat([df_temp,jiofin_data],axis=0)

print(jiofin_data.head())

print(jiofin_data.tail())
