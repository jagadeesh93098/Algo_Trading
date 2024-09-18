from dhanhq import marketfeed
import pandas as pd
import time

# Path for the Security File
security_url = "Dhan_Works/security.csv"

df = pd.read_csv(security_url,low_memory = False)

df.head()

df['SEM_INSTRUMENT_NAME'].unique()

df['SEM_EXM_EXCH_ID'].unique()

df.loc[(df['SEM_INSTRUMENT_NAME']=='EQUITY') & (df['SEM_TRADING_SYMBOL']).str.startswith('ITC') & (df['SEM_SERIES'] == 'EQ'),:]

df.loc[(df['SEM_INSTRUMENT_NAME']=='OPTIDX'),:]

df.loc[(df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NIFTY')),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_INSTRUMENT_NAME'] == 'FUTCOM'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_STRIKE_PRICE'] == 190),:].head()

df.loc[df['SEM_SMST_SECURITY_ID'] == 1333,:]

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

""

data = {
    "securityId": "1333",
    "exchangeSegment":"NSE_EQ",
    "instrument": "EQUITY",
    "expiryCode": 0,
    "fromDate": "2022-01-08",
    "toDate": "2022-02-08"
}

get_historical_data_curl = f"curl --request POST --url https://api.dhan.co/v2/charts/historical --header 'Content-Type: application/json' --header 'access-token: {access_token}' --data '{data}'"

print(get_historical_data_curl)



curl --request POST --url https://api.dhan.co/v2/charts/historical --header 'Content-Type: application/json' --header 'access-token: JWT' --data '{'securityId': '1333', 'exchangeSegment': 'NSE_EQ', 'instrument': 'EQUITY', 'expiryCode': 0, 'fromDate': '2022-01-08', 'toDate': '2022-02-08'}'
