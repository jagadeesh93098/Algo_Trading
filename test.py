import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Goal is Calculate Beta of Stocks as I've Entered and Exited my Stake in Them. For Estimating the Expected Returns.

# Calculate the start date as 30 days ago from today
e_d = datetime.today()-timedelta(days=1)
end_date = e_d.strftime('%Y-%m-%d')
s_d = e_d - timedelta(days=7)
start_date=s_d.strftime("%Y-%m-%d")

# Fetch historical intraday data for Jio Platforms Limited for the last 30 days
jiofin_data = yf.download("JIOFIN.NS", start=start_date, end=end_date, interval="1m")

for i in range(0,3):
    e_d=s_d
    end_date = e_d.strftime('%Y-%m-%d')
    s_d = e_d - timedelta(days=7)
    start_date=s_d.strftime("%Y-%m-%d")

    # Fetch historical intraday data for Jio Platforms Limited for the last 30 days
    df_temp = yf.download("JIOFIN.NS", start=start_date, end=end_date, interval="1m")
    jiofin_data=pd.concat([df_temp,jiofin_data],axis=0)


j=yf.Ticker('^NSEI')
for i in list(j.info.keys()):
    if "beta"in i:
        print(i)



jiofin_data.reset_index(inplace=True,drop=True)

jiofin_data['day_change']=jiofin_data['Close']-jiofin_data['Open']
jiofin_data['Day_Change']=round(jiofin_data['Day_Change']/jiofin_data['Open'],5)

jiofin_data
