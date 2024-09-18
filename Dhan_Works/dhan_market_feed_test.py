from dhanhq import marketfeed
import pandas as pd
import time

# Path for the Security File
security_url = "Dhan_Works/security.csv"

df = pd.read_csv(security_url,low_memory = False)

df.head()

df['SEM_INSTRUMENT_NAME'].unique()

df['SEM_EXM_EXCH_ID'].unique()

df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_INSTRUMENT_NAME'] == 'FUTCOM'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_STRIKE_PRICE'] == 190),:].head()

instruments = [(5,'430268',15),(5,'436104',15)]

data = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
data.run_forever()
data.get_data()
data.close_connection()


df = pd.DataFrame({"Security_ID":[],"LTP":[],"LTT":[]})

""""
For Continous Data Flow
""""

try:
    data.run_forever()
    while True:
        response = data.get_data()
        df.loc[len(df.index)] = [response['security_id'],eval(response['LTP']),response['LTT']]
        print(df)
except Exception as e:
    print(e)

data.close_connection()
start = time.time()
for i in range(0,10):
    data.get_data()
print(f"Time Taken = {time.time() - start}")

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"
