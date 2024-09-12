from dhanhq import marketfeed
import pandas as pd

client_id = "1104088864"
client_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI2MTc4MzcwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.tEheq0yFTPEWpKayI9Hp95sS8SjosYYIYZtMLZUjKqVbXFnnjWFUAUhPP5N3pZXRBYOOmnajiqDpnbXs0jWhvA"

df = pd.read_csv('api-scrip-master.csv',low_memory = False)
df.head()

df.columns

df['SEM_INSTRUMENT_NAME'].unique()

instrument_name = 'OPTIDX'
exch_id = 'NSE'
symbol = 'NIFTY50'

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE') & (df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SM_SYMBOL_NAME'] == 'NIFTY'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE') & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_TRADING_SYMBOL'].str.contains('NIFTY-')) & (df['SEM_EXPIRY_DATE'].str.contains('2024-09-12')) ,['SEM_TRADING_SYMBOL','SEM_EXPIRY_DATE']]


instrument = [(0,'13',15)]

data = marketfeed.DhanFeed(client_id, client_token, instrument)
data.run_forever()
data.subscribe_symbols(instrument)
data.get_data()
data.disconnect()
