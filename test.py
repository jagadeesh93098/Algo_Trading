import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Goal is Calculate Beta of Stocks as I've Entered and Exited my Stake in Them. For Estimating the Expected Returns.

def my_data(s):
    # Calculate the start date as 30 days ago from today
    e_d = datetime.today()-timedelta(days=1)
    end_date = e_d.strftime('%Y-%m-%d')
    s_d = e_d - timedelta(days=7)
    start_date=s_d.strftime("%Y-%m-%d")

    # Fetch historical intraday data for Jio Platforms Limited for the last 30 days
    df = yf.download(s, start=start_date, end=end_date, interval="1m")

    for i in range(0,3):
        e_d=s_d
        end_date = e_d.strftime('%Y-%m-%d')
        s_d = e_d - timedelta(days=7)
        start_date=s_d.strftime("%Y-%m-%d")

        # Fetch historical intraday data for Jio Platforms Limited for the last 30 days
        df_temp = yf.download(s, start=start_date, end=end_date, interval="1m")
        df=pd.concat([df_temp,df],axis=0)

    return df

jiofin_data=my_data("JIOFIN.NS")

nifty_data=my_data("^NSE")

jiofin_data.reset_index(inplace=True,drop=True)

jiofin_data['day_change']=jiofin_data['Close']-jiofin_data['Open']
jiofin_data['day_change_pu']=round(jiofin_data['day_change']/jiofin_data['Open'],5)

jiofin_data
