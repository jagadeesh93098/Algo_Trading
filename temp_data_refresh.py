import pandas as pd
import os

dirs = [i for i in os.listdir() if os.path.isdir(i)]

if "temp_data" not in dirs:
    os.mkdir("temp_data")

url = 'https://images.dhan.co/api-data/api-scrip-master.csv'
df = pd.read_csv(url,low_memory = False)
df.to_csv("temp_data/securitys.csv",index=False)

security_ids = {
        'MIDCPNIFTY':442,
        'BANKEX':69,
        'FINNIFTY':27,
        'BANKNIFTY':25,
        'NIFTY':13,
        'SENSEX':51,
    }

def get_option_chain(underlying):
    global df
    instrument = 'OPTIDX'
    exch = ""
    if underlying == 'NIFTY' or underlying == 'FINNIFTY' or underlying == 'BANKNIFTY' or underlying == 'MIDCPNIFTY':
        exch = 'NSE'
    else:
        exch = 'BSE'
    temp = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.split("-").str[0] == underlying),:].copy()
    temp
    underlying
    list_expiry = list(temp['SEM_EXPIRY_DATE'])
    list_expiry.sort()
    expiry_date = list_expiry[0]
    expiry_date
    df_opt = temp.loc[(temp['SEM_EXPIRY_DATE'] == expiry_date),:].copy()
    df_opt.reset_index(inplace = True, drop = True)
    return df_opt

for underlying in list(security_ids.keys()):
    option_chain = get_option_chain(underlying)
    option_chain.to_csv(f"temp_data/{underlying}.csv",index=False)
