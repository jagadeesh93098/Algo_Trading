import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def my_data_day(s):
    e_d=datetime.today()-timedelta(days=1)
    end_date=e_d.strftime("%Y-%m-%d")
    s_d=e_d - timedelta(days=30*9)
    start_date=s_d.strftime("%Y-%m-%d")

    df=yf.download(s,start=start_date,end=end_date,interval='1d')

    return df

def my_profit_prev_close(df):
    df.reset_index(inplace=True,drop=False)
    df.loc[:,"change_prev_close"]=0
    for i in range(1,df.shape[0]):
        df.loc[i,'change_prev_close']=round((df.loc[i,'Close']-df.loc[i=1,'Close'])/df.loc[i-1,'Close'],5)
    return df


df=my_data_day("JIOFIN.NS")

df=my_profit_prev_close(df)

df
