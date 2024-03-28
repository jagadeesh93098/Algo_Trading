import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Goal is Calculate Beta of Stocks as I've Entered and Exited my Stake in Them. For Estimating the Expected Returns.

def my_data_min(s):
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


def my_data_day(s):
    # Calculate the start date as 30 days ago from today
    e=datetime.today()
    end_date=e.strftime("%Y-%m-%d")
    s=e-timedelta(years=5)
    start_date=s.strftime("%Y-%m-%d")
    # Fetch historical intraday data for Jio Platforms Limited for the last 30 days
    df = yf.download(s, start=start_date, end=end_date, interval="1d")
    return df

def my_day_change(df):
    df_temp=df.copy()
    df_temp.reset_index(inplace=True)
    df_temp['day_change']=df_temp['Close']-df_temp['Open']
    df_temp['day_change_pu']=round(df_temp['day_change']*100/df_temp['Open'],8)
    return df_temp


l=["IREDA.NS","JSWINFRA.NS","JIOFIN.NS","TATAPOWER.NS","UNIONBANK.NS","EMIL.NS","L&TFH.NS"]

v=[39850,33355,67600,38325,14685,18295,14900]

from sklearn.linear_model import LinearRegression

import numpy as np


for i in l:
    s_data=my_day_change(my_data_min(i))
    nifty_data=my_day_change(my_data_min("^NSEI"))
    s_data=s_data.loc[s_data['Datetime'].isin(nifty_data['Datetime'])].copy()
    nifty_data=nifty_data.loc[nifty_data['Datetime'].isin(s_data['Datetime']),:].copy()
    Y=np.array(s_data['day_change_pu'])
    X=np.array(nifty_data['day_change_pu']).reshape(-1,1)
    model=LinearRegression().fit(X,Y)
    locals()['beta_m_{}'.format(i)]=model.coef_[0]

for i in l:
    print("Beta of min by min {} = {}\n".format(i,locals()['beta_m_{}'.format(i)]))

w=[round(i/sum(v),4) for i in v]

b_m=[]
for i in l:
    b_m.append(locals()['beta_m_{}'.format(i)])

beta_p_m=0
for i in range(0,len(w)):
    beta_p_m+=w[i]*b_m[i]

beta_p_m

for i in l:
    s_data=my_day_change(my_data_day(i))
    nifty_data=my_day_change(my_data_day("^NSEI"))
    s_data=s_data.loc[s_data['Date'].isin(nifty_data['Date'])].copy()
    nifty_data=nifty_data.loc[nifty_data['Date'].isin(s_data['Date']),:].copy()
    Y=np.array(s_data['day_change_pu'])
    X=np.array(nifty_data['day_change_pu']).reshape(-1,1)
    model=LinearRegression().fit(X,Y)
    locals()['beta_d_{}'.format(i)]=model.coef_[0]

for i in l:
    print("Beta of day by day {} = {}\n".format(i,locals()['beta_d_{}'.format(i)]))

b_d=[]
for i in l:
    b_d.append(locals()['beta_d_{}'.format(i)])

beta_p_d=0
for i in range(0,len(w)):
    beta_p_d+=w[i]*b_d[i]

beta_p_d

beta_p_m


nifty_data=my_day_change(my_data_min("^NSEI"))

import datetime
nifty_data=nifty_data.loc[nifty_data['Datetime']>pd.Timestamp("2024-03-12",tz="Asia/Kolkata")].copy()

nifty_data.reset_index(inplace=True,drop=True)

r_m=(nifty_data.loc[nifty_data.shape[0]-1,"Close"]-nifty_data.loc[0,"Open"])/nifty_data.loc[0,"Open"]

r_p=0.0326

r_f=(((1+0.1)**(1/365))-1)**(29-13)

round(r_p-r_f-beta_p_m*(r_m-r_f),5)

sum(v)

