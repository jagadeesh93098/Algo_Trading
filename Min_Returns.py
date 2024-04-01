import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def my_data_min(s):
    e_d=datetime.today()-timedelta(days=1)
    end_date=e_d.strftime("%Y-%m-%d")
    s_d=e_d-timedelta(days=7)
    start_date=s_d.strftime("%Y-%m-%d")

    df=yf.download(s,start=start_date,end=end_date,interval='1m')

    for i in range(0,3):
        e_d=s_d
        end_date=e_d.strftime("%Y-%m-%d")
        s_d=e_d-timedelta(days=7)
        start_date=s_d.strftime("%Y-%m-%d")
        df_temp=yf.download(s,start=start_date,end=end_date,interval='1m')
        df=pd.concat([df_temp,df],axis=0)
    return df

def my_profit_prev_close(df):
    df.reset_index(inplace=True,drop=False)
    df.loc[:,"change_prev_close"]=0.00
    for i in range(1,df.shape[0]):
        df.loc[i,'change_prev_close']=round((df.loc[i,'Close']-df.loc[i-1,'Close'])*100/df.loc[i-1,'Close'],5)
    return df

df=my_data_min('JIOFIN.NS')

df=my_profit_prev_close(df)

6*60*df['change_prev_close'].loc[1:].mean()
6*60*df['change_prev_close'].loc[1:].var()

import matplotlib.pyplot as plt

plt.plot([i for i in range(1,df.shape[0])],df['change_prev_close'].loc[1:])
plt.savefig('output.png')

import seaborn as sns

sns.distplot(a=df.change_prev_close)
