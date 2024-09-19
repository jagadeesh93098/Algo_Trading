import pandas as pd
from dhanhq import marketfeed
import requests

df = pd.read_csv('Dhan_Works/security.csv',low_memory = False)

underlying_s_id = df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_INSTRUMENT_NAME'] == 'FUTCOM') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09')),'SEM_SMST_SECURITY_ID'].item()

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_INSTRUMENT_NAME'] == 'OPTFUT') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09-23')),:].copy()

strike = 190

opt_s_id = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']==190) & (df_opt['SEM_OPTION_TYPE'] == 'CE'),'SEM_SMST_SECURITY_ID'].item()

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

instruments = [(5,str(opt_s_id),15)]

instruments


response = feed.get_data()

ltp = eval(response['LTP'])

ltp

test = pd.DataFrame({'order_id':[],'buyPrice':[],'buyqty':[],'sell_price':[],'ltp':[]})
buy_price = ltp
test.loc[len(test.index)] = ['t1',buy_price,1,None,ltp]

while True:
    feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
    feed.run_forever()
    response = feed.get_data()
    ltp = eval(response['LTP'])
    if ltp-buy_price >= 0.02*buy_price:
        test.loc[test['order_id'] == 't1','sell_price'] = ltp
        test.loc[test['order_id'] == 't2','ltp'] = 






