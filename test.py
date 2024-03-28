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

jiofin_data

nifty_data=my_data("^NSEI")

nifty_data

def my_day_change(df):
    df_temp=df.copy()
    df_temp.reset_index(inplace=True)
    df_temp['day_change']=df_temp['Close']-df_temp['Open']
    df_temp['day_change_pu']=round(df_temp['day_change']*100/df_temp['Open'],8)
    return df_temp


jiofin_data=my_day_change(jiofin_data)

nifty_data=my_day_change(nifty_data)

jiofin_data=jiofin_data.loc[jiofin_data['Datetime'].isin(nifty_data['Datetime'])].copy()

jiofin_data

nifty_data=nifty_data.loc[nifty_data['Datetime'].isin(jiofin_data['Datetime']),:].copy()

nifty_data


a=np.stack((jiofin_data['day_change_pu'],nifty_data['day_change_pu']),axis=0)

np.cov(a)
