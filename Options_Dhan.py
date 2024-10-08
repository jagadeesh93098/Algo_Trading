from dhanhq import marketfeed
import pandas as pd
import datetime

option_dict = {0:["MIDCPNIFTY","BANKEX"],1:"FINNIFTY",2:"NIFTYBANK",3:"NIFTY50",4:"SENSEX"}

temp = datetime.date.today()
print(datetime.date.today())

print(temp + datetime.timedelta(days = 7 - temp.weekday()))

option_num = 0
underlying = option_dict[option_num][0]
underlying

next_expiry = datetime.datetime.strftime(temp + datetime.timedelta(days = 7 + option_num - temp.weekday()),'%d %b')
next_expiry.upper()


df = pd.read_csv('api-scrip-master.csv')

df.columns

df.loc[(df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SEM_TRADING_SYMBOL'].str.contains(underlying.upper())),['SEM_SMST_SECURITY_ID','SEM_TRADING_SYMBOL','SEM_CUSTOM_SYMBOL']]

df_underlying = df.loc[(df['SEM_INSTRUMENT_NAME'] == 'INDEX') & df['SEM_CUSTOM_SYMBOL'].str.contains(underlying),:].copy()
df_underlying

df_option_chain = df.loc[(df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_CUSTOM_SYMBOL'].str.contains(next_expiry.upper())) & (df['SEM_CUSTOM_SYMBOL'].str.contains(underlying)),['SEM_TRADING_SYMBOL','SEM_CUSTOM_SYMBOL','SEM_SMST_SECURITY_ID','SEM_SEGMENT','SEM_EXCH_INSTRUMENT_TYPE']].copy()
df_option_chain.reset_index(inplace = True, drop = True)
df_option_chain_call = df_option_chain.loc[df_option_chain['SEM_CUSTOM_SYMBOL'].str.contains('CALL'),:]
df_option_chain_call.reset_index(inplace = True, drop = True)
df_option_chain_call['STRIKE'] = [int(i.split(' ')[-2]) for i in df_option_chain_call['SEM_CUSTOM_SYMBOL']]
df_option_chain_call.sort_values(by = 'STRIKE', ascending = True,inplace = True)
df_option_chain_call.reset_index(inplace = True, drop = True)
df_option_chain_call.loc[df_option_chain_call['STRIKE'] == 13000,:]

client_id = "1104088864"
client_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI3NTE5ODQzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.XIKQpgBpDUa6CLjf67FjM-4c6lIfvURzU0Dob6RJIZUv3dyCmsZhXxiKMhSccdvCNdfPctU_vPSa6j8WclAfiA"

instrument = [(2,'64756',17)]

data = marketfeed.DhanFeed(client_id, client_token, instrument)
data.run_forever()
data.subscribe_symbols(instrument)
response = data.get_data()
response
data.disconnect()

from dhanhq import dhanhq

dhan = dhanhq(client_id,client_token)

response = dhan.intraday_minute_data('64756','NSE_FNO','OPTIDX')

df = pd.DataFrame(response['data'])

df











def get_list_of_options(unde)


df = pd.read_csv('api-scrip-master.csv',low_memory = False)
df.head()

df.columns

df['SM_SYMBOL_NAME'].unique()

instrument_name = 'OPTIDX'
exch_id = 'BSE'
symbol = 'NIFTY'

df.columns

df['SEM_INSTRUMENT_NAME'].unique()

df['SEM_CUSTOM_SYMBOL'].str.contains("Nifty") == True

df.loc[df['SEM_CUSTOM_SYMBOL'].str.contains("Nifty"),:]

temp=df.loc[(df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_TRADING_SYMBOL'].str.contains('MIDCPNIFTY')),:].copy()
temp.reset_index(inplace = True, drop = True)

temp.loc[0,:]

k = []
for i in temp.loc[:,'SEM_TRADING_SYMBOL']:
    k.append(i.split("-")[0])
print(k)
temp.loc[0,'SEM_TRADING_SYMBOL'].split("-")[0]

def get_security_id(option_type,strike,undelying,date_of_expiry)

df.loc[(df['SEM_EXM_EXCH_ID'] == 'NSE') & (df['SEM_INSTRUMENT_NAME'] == 'INDEX') & (df['SM_SYMBOL_NAME'] == 'NIFTY'),:]

df.loc[(df['SEM_EXM_EXCH_ID'] == 'BSE') & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_TRADING_SYMBOL'].str.contains(symbol)) & (df['SEM_EXPIRY_DATE'].str.contains('2024-09-13')) ,['SEM_SMST_SECURITY_ID','SEM_TRADING_SYMBOL','SEM_EXPIRY_DATE','SEM_CUSTOM_SYMBOL']]



