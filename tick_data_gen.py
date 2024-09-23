import pandas as pd
from dhanhq import marketfeed
import time

url = 'security.csv'

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

df = pd.read_csv(url,low_memory = False)

exch = 'MCX'
instrument_name = 'OPTFUT'
underlying = 'NATURALGAS'

list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID']==exch) & (df['SEM_INSTRUMENT_NAME'] == instrument_name) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'].unique())

list_expiry.sort(reverse = False)

mr_expiry = list_expiry[0]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument_name) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'] == mr_expiry),:].copy()

df_opt.reset_index(inplace = True, drop = True)

strike = 210
option_type = 'PE'
trading_symbol = df_opt.loc[(df_opt['SEM_OPTION_TYPE'] == option_type) & (df_opt['SEM_STRIKE_PRICE'] == strike),'SEM_TRADING_SYMBOL'].item()
opt_sid = df_opt.loc[(df_opt['SEM_OPTION_TYPE'] == option_type) & (df_opt['SEM_STRIKE_PRICE'] == strike),'SEM_SMST_SECURITY_ID'].item()


instruments = [(5,str(opt_sid),15)]

feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)

tick_df = pd.DataFrame({'tick_num':[],'trading_symbol':[],'open':[],'high':[],'low':[],'close':[]})

try:
    feed.run_forever()
    tick = 0
    while True:
        start = time.time()
        count = 0
        response = feed.get_data()
        ltp = response['LTP']
        open = ltp
        close = ltp
        high = ltp
        low = ltp
        while count < 10:
            count += 1
            response = feed.get_data()
            ltp = response['LTP']
            if ltp >= high:
                high = ltp
            if ltp <= low:
                low = ltp
            if count == 9:
                close = ltp
        tick_df.loc[len(tick_df.index)] = [tick,trading_symbol,open,high,low,close]
        tick += 1
        print(tick_df)
        print(f"Time for a single tick (10 LTPS) = {time.time() - start}")
except KeyboardInterrupt:
    feed.close_connection()

tick_df.to_csv('test_tick_data.csv',index=False)
