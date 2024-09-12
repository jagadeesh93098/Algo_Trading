from dhanhq import marketfeed
import pandas as pd
import datettime



client_id = "1104088864"
client_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI2MTc4MzcwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.tEheq0yFTPEWpKayI9Hp95sS8SjosYYIYZtMLZUjKqVbXFnnjWFUAUhPP5N3pZXRBYOOmnajiqDpnbXs0jWhvA"

df = pd.read_csv('api-scrip-master.csv',low_memory = False)
df.head()

df.columns

df['SEM_INSTRUMENT_NAME'].unique()

instrument_name = 'OPTIDX'
exch_id = 'BSE'
symbol = 'SENSEX-'



def get_security_id(option_type,strike,undelying,date_of_expiry)

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE') & (df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SM_SYMBOL_NAME'] == 'NIFTY'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'BSE') & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_TRADING_SYMBOL'].str.contains(symbol)) & (df['SEM_EXPIRY_DATE'].str.contains('2024-09-13')) ,['SEM_SMST_SECURITY_ID','SEM_TRADING_SYMBOL','SEM_EXPIRY_DATE','SEM_CUSTOM_SYMBOL']]


instrument = [(0,'13',15)]

data = marketfeed.DhanFeed(client_id, client_token, instrument)
data.run_forever()
data.subscribe_symbols(instrument)
data.get_data()
data.disconnect()
