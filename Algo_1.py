import pandas as pd
from dhanhq import marketfeed
# import requests
import datetime
import sys
import time
import math
import numpy as np

step = 0.05
def calculate_qty(fund,ltp):
    return lot_size * math.floor(fund/(ltp*lot_size))

def calculate_price(price,percent):
    return step * (math.floor(price*(1+percent)/step)-1)

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

""" IF the file is not present use the Below Link """
"""  """
url = "security.csv"

df = pd.read_csv(url,low_memory = False)

today = datetime.datetime.today().date()



underlying = 'NATURALGAS'
exch = 'MCX'
instrument = 'OPTFUT'
today_date = datetime.datetime.strftime(today,'%Y-%m')


# underlying = sys.argv[1]
# underlying = 'BANKEX'
# instrument = 'OPTIDX'
# today_date = datetime.datetime.strftime(today,'%Y-%m-%d')
# today_date

# df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'].str.startswith(today_date)),:]

temp = list(df.loc[(df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.contains(underlying)),'SEM_EXPIRY_DATE'].unique())

expiry_date = temp[0]

df_opt = df.loc[(df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.contains(underlying)) & (df['SEM_EXPIRY_DATE'] == expiry_date),:].copy()

df_opt

# my_strike = int(sys.argv[2])
# my_option_type = str(sys.argv[3])

my_strike = 210
my_option_type = 'CE'

my_option = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == my_strike) & (df['SEM_OPTION_TYPE']==my_option_type),:]
my_option
opt_sid = my_option.loc[:,'SEM_SMST_SECURITY_ID'].item()
lot_size = my_option.loc[:,'SEM_LOT_UNITS'].item()

if underlying == 'MIDCPNIFTY':
    instruments = [(2,str(opt_sid),15)]
else:
    instruments = [(5,str(opt_sid),15)]
feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
feed.run_forever()
response = feed.get_data()

response

ltp = eval(response['LTP'])
# ltp = 52.95
buy_price = ltp

ltp

fund = 10000
qty = calculate_qty(fund,ltp)

file_name = f'test_order_{datetime.datetime.strftime(today,'%Y_%m_%d')}.csv'
try :
    order_list = pd.read_csv(file_name)
    o=order_list.loc[len(order_list.index)-1,'order_id']
    order_id = f"O_{int(o.split('_')[1])+1}"
except FileNotFoundError:
    order_id = 'O_1'

# i_tpp = float(sys.argv[4])
# i_slp = float(sys.argv[5])

i_tpp = 0.2
i_slp = -0.1

sl_price = calculate_price(buy_price,i_slp)
tp_price = calculate_price(buy_price,i_tpp)
slp = (sl_price - buy_price)/buy_price
tpp = (tp_price - buy_price)/buy_price
trigger = sl_price + step
pp=0


# abs(pt - presentp)/abs(present_p - p)

# Open the Loop
# Keep Tracking LTP
# Set the Stop Loss based on Present Profit.
# If Number of Order Modificate increases 25, Cancel the order any place a new order.

test = pd.DataFrame({'LTT':[datetime.datetime.now()],'order_id':[order_id],'BUY_PRICE':[buy_price],'QTY':[qty],'LTP':[ltp],'PP':[pp],'SLP': [slp],"TPP":[tpp],"SL_PRICE":[sl_price],'TRIGGER_PRICE':[trigger],'TP_PRICE':[tp_price],"SELL_PRICE":[np.nan],"P/L":[np.nan]})
test
print(test.loc[[len(test.index)-1],:])
exit = False
while exit == False:
    response = feed.get_data()
    ltp = eval(response['LTP'])
    pp = (ltp - buy_price)/buy_price
    if ltp <= trigger:
        sell_price = ltp
        exit = True
        test.loc[len(test.index),:] = [datetime.datetime.now(),order_id,buy_price,qty,ltp,pp,slp,tpp,sl_price,trigger,tp_price,sl_price,(sl_price - buy_price)*qty - 40]
        print("\n Stop Loss HIT \n")
        print(test.loc[[len(test.index)-1],:])
        break
    if pp >= tpp:
        tpp = pp + 0.05
    slp_temp = max(slp,(3*pp - tpp)/2)
    # print(slp_temp)
    sl_price = max(sl_price,calculate_price(buy_price,slp_temp))
    trigger = sl_price + step
    slp = (sl_price - buy_price)/buy_price
    tp_price = calculate_price(buy_price,tpp)
    test.loc[len(test.index),:] = [datetime.datetime.now(),order_id,buy_price,qty,ltp,pp,slp,tpp,sl_price,trigger,tp_price,np.nan,np.nan]
    print(test.loc[[len(test.index)-1],:])
result = test.loc[[len(test.index)-1],:].copy()
result.reset_index(inplace=True,drop=True)
list(result.loc[0,:])
try :
    order_list = pd.read_csv(file_name)
    order_list.loc[len(order_list.index),:]=list(result.loc[0,:])
    print(order_list)
    order_list.to_csv(file_name,index=False)
except FileNotFoundError:
    result.to_csv(file_name,index=False)
feed.close_connection()
