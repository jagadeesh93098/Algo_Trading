import pandas as pd
from dhanhq import marketfeed
import requests
import datetime
import sys
import time

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

df = pd.read_csv('Dhan_Works/security.csv',low_memory = False)

today = datetime.datetime.today().date()

today_date = datetime.datetime.strftime(today,'%Y-%m-%d')

today_date

underlying = 'CRUDE'
exch = 'MCX'
instrument = 'FUTCOM'

# df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09')) ,'SEM_SMST_SECURITY_ID']

underlying_sid = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09')) ,'SEM_SMST_SECURITY_ID'].item()

underlying_sid

instrument = 'OPTFUT'

today_date

df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-10')),:]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-10')),:].copy()

df_opt

# instruments = [(0,str(underlying_sid),15)]
# instruments



my_strike = int(sys.argv[1])
my_option_type = str(sys.argv[2])
# my_strike = 5950
# my_option_type = 'CE'
count = 0

df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == my_strike) & (df['SEM_OPTION_TYPE']==my_option_type),:]

opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == my_strike) & (df['SEM_OPTION_TYPE'] == my_option_type) & (df['SM_SYMBOL_NAME'] == 'CRUDEOIL'),'SEM_SMST_SECURITY_ID'].item()

opt_sid

instruments = [(5,str(opt_sid),15)]

feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
feed.run_forever()
response = feed.get_data()
# feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
# feed.run_forever()
# get_opt_ltp = False
# while get_opt_ltp == False:
# response = feed.get_data()
    # if response['security_id'] == opt_sid:
    #     get_opt_ltp = True

# if response['security_id'] == opt_sid:
ltp = eval(response['LTP'])
ltp
# buy_price = 198.0
buy_price = ltp
test = pd.DataFrame({'order_id':[],'buyPrice':[],'buyqty':[],'sell_price':[],'ltp':[],'remark' : []})
test.loc[len(test.index)] = ['t1',buy_price,1,None,ltp,None]
test
# abs(pt - presentp)/abs(present_p - p)

p_t = 0.03
p_l = -0.01
exit = False
target_breached = 0
while exit == False:
    response = feed.get_data()
    ltp = eval(response['LTP'])
    test.loc[test['order_id'] == 't1','ltp'] = ltp
    present_p = (ltp - buy_price)/buy_price
    if present_p >= p_t:
        p_t = present_p + 0.001
        target_breached = 1
    if target_breached == 1:
        p_l = max((p_t - 3*present_p)/2, p_l)
    if ltp - buy_price > p_t*buy_price :
        test.loc[test['order_id'] == 't1','sell_price'] = ltp
        print('Sold')
        test.loc[test['order_id'] == 't1','remark'] =f'Profit_Booked at {p_t}'
        print(test)
        exit = True
        break
    if ltp - buy_price < p_l*buy_price:
        test.loc[test['order_id'] == 't1','ltp'] = ltp
        print('Sold based on Stop Loss')
        print(f"Profit/Loss Booked = {p_l}")
        test.loc[test['order_id']=='t1','remark'] = 'Stop Loss'
        print(test)
        exit = True
        break
    print(test)
    print(f"Present Profit = {(ltp - buy_price)/(buy_price)}")
    print(f"Present Stop Loss = {p_l}")
    print(f"Present Target Profit = {p_t}")

feed.close_connection()
