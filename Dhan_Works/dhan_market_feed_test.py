from dhanhq import marketfeed
import pandas as pd


client_id = '1104088864'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI2NTE2MzkwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.1ro6-2OzEiDH2XhaImfzGXBOF6ZR6OkxZ6cOn4xG0A7itc_AvdlXuIKAoJNsSxIgTVr924xUi37Ko9pqip1nzg'

security_url = "https://images.dhan.co/api-data/api-scrip-master.csv"

df = pd.read_csv(security_url,low_memory = False)

df.head()

df['SEM_INSTRUMENT_NAME'].unique()

df['SEM_EXM_EXCH_ID'].unique()

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE')]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_STRIKE_PRICE'] == 190),:].head()

instruments = [(5,'430268',15),(5,'436104',15)]

data = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
data.run_forever()

import time

df_opt = pd.DataFrame({"LTP":[],"LTT":[]})

df_fut = pd.DataFrame({"LTP":[],"LTT":[]})

try:
    while True:
        data.run_forever()
        response = data.get_data()
        response
        if response['security_id'] == 436104:
            df_opt.loc[len(df_opt.index)] = [eval(response['LTP']),response['LTT']]
            print(df_opt)
        else:
            df_fut.loc[len(df_fut.index)] = [eval(response['LTP']),response['LTT']]
            print(df_fut)

except Exception as e:
    print(e)

eval('192.3')

start = time.time()
for i in range(0,10):
    data.get_data()
print(f"Time Taken = {time.time() - start}")
data.close_connection()
