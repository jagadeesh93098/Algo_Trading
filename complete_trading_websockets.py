import websockets
import pandas as pd
import json
import asyncio
import struct
import requests
import csv

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

def get_option_chain(exch,instrument,underlying):
    global df
    url = 'temp_data/securitys.csv'
    df = pd.read_csv(url,low_memory = False)
    list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'])
    expiry_date = list_expiry[0]
    df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'] == expiry_date),:]
    return df_opt

def get_opt_details(strike,option_type):
    global df_opt
    opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == strike) & (df_opt['SEM_OPTION_TYPE'] == option_type),'SEM_SMST_SECURITY_ID'].item()
    opt_desc = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == strike) & (df_opt['SEM_OPTION_TYPE'] == option_type),'SEM_CUSTOM_SYMBOL'].item()
    temp = [opt_sid,opt_desc]
    return temp


temp = df.loc[(df['SEM_INSTRUMENT_NAME'] == 'FUTCOM') & (df['SEM_TRADING_SYMBOL'].str.startswith('CRUDEOIL-')),:].copy()
list_expiry = list(temp.loc[:,'SEM_EXPIRY_DATE'].unique())
list_expiry.sort()
expiry_date = list_expiry[0]

temp.loc[(temp['SEM_EXPIRY_DATE'] == expiry_date),:]

underlying_sid = temp.loc[(temp['SEM_EXPIRY_DATE'] == expiry_date),"SEM_SMST_SECURITY_ID"].item()
underlying_sid

market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'MCX_COMM':[underlying_sid]
}


response = requests.post(url = market_quote_url,headers = header,json = data)
print(f"Status Code of Response = {response.status_code}")
result = response.json()['data']['MCX_COMM']
response.json()
ltp = result[str(underlying_sid)]['last_price']

df_opt = get_option_chain('MCX','OPTFUT','CRUDEOIL-')
list_strike = list(df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] <= ltp),'SEM_STRIKE_PRICE'])
atm_strike = max(list_strike)
opt_sids = list(df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] <= ltp*1.02) & (df_opt['SEM_STRIKE_PRICE'] >= ltp*0.98),'SEM_SMST_SECURITY_ID'])
opt_desc = list(df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] <= ltp*1.02) & (df_opt['SEM_STRIKE_PRICE'] >= ltp*0.98),'SEM_CUSTOM_SYMBOL'])

opt_sids


data = []
for i in opt_sids:
    temp = {
        "ExchangeSegment":"MCX_COMM",
        "SecurityId":str(i)
    }
    data.append(temp)


payload = {
    "RequestCode":21,
    "InstrumentCount":len(data),
    "InstrumentList":data
}

r_json = json.dumps(payload)

r_json

msg = 0

async def get_data(client_id,access_token):
    global opt_sid,r_json,msg,strike,option_type,field_names
    url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    async with websockets.connect(uri = url,close_timeout=2) as ws:
        await ws.send(r_json)
        count = 0
        while True:
            try :
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            except TimeoutError:
                await ws.send(r_json)
                temp = await asyncio.wait_for(ws.recv(),timeout=20)
            if temp != msg:
                msg = temp
                sid = list(struct.unpack('<I',msg[4:8]))
                ticker = list(struct.unpack('<f', msg[8:12]))
                temp = {'sid':sid[0],'ticker':ticker[0],'msg':msg}
                print(temp)
                with open("test_data_collection.csv",mode = 'a',newline = "") as f:
                    writer = csv.DictWriter(f,fieldnames=field_names)
                    writer.writerow(temp)

asyncio.run(get_data(client_id=client_id,access_token=access_token))

