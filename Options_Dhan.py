from dhanhq import marketfeed
import pandas as pd
import datetime

option_dict = {0:["MIDCAP","BANKEX"],1:"FINNIFTY",2:"NIFTYBANK",3:"NIFTY50",4:"SENSEX"}

temp = datetime.date.today()
print(datetime.date.today())

print(temp + datetime.timedelta(days = 7 - temp.weekday()))


underlying = option_dict[1]
next_expiry = datetime.datetime.strftime(temp + datetime.timedelta(days = 7 + 1 - temp.weekday()),'%d %b')
next_expiry




def get_list_of_options(unde)




client_id = "1104088864"
client_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI2MTc4MzcwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.tEheq0yFTPEWpKayI9Hp95sS8SjosYYIYZtMLZUjKqVbXFnnjWFUAUhPP5N3pZXRBYOOmnajiqDpnbXs0jWhvA"

df = pd.read_csv('api-scrip-master.csv',low_memory = False)
df.head()

df.columns

df['SM_SYMBOL_NAME'].unique()

instrument_name = 'OPTIDX'
exch_id = 'BSE'
symbol = 'NIFTY'

df['SEM_CUSTOM_SYMBOL'].str.contains("Nifty") == True

df.loc[df['SEM_CUSTOM_SYMBOL'].str.contains("Nifty"),:]

df.loc[(df['SM_SYMBOL_NAME'].str.contains('MIDCAP'))==True,['SM_SYMBOL_NAME','SEM_TRADING_SYMBOL','SEM_CUSTOM_SYMBOL']]

def get_security_id(option_type,strike,undelying,date_of_expiry)

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE') & (df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SM_SYMBOL_NAME'] == 'NIFTY'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'BSE') & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_TRADING_SYMBOL'].str.contains(symbol)) & (df['SEM_EXPIRY_DATE'].str.contains('2024-09-13')) ,['SEM_SMST_SECURITY_ID','SEM_TRADING_SYMBOL','SEM_EXPIRY_DATE','SEM_CUSTOM_SYMBOL']]


instrument = [(0,'13',15)]

data = marketfeed.DhanFeed(client_id, client_token, instrument)
data.run_forever()
data.subscribe_symbols(instrument)
data.get_data()
data.disconnect()

