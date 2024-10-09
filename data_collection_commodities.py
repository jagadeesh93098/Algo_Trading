import websockets
import pandas as pd
import json
import asyncio
import struct
import requests
import csv
import FULL_PACKET as FP

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

url = "temp_data/securitys.csv"
df_securitys = pd.read_csv(url,low_memory = False)

# GETTING THE CLOSEST COMMODITY FUTURE
underlyings = ['CRUDEOIL','GOLD','NATURALGAS']

# GET UNDERLYINGS SECURITYID
exch = 'MCX'
instrument_name = 'FUTCOM'
tickers = {}

for underlying in underlyings:
    df_temp = df_securitys.loc[(df_securitys['SEM_EXM_EXCH_ID'] == exch) & (df_securitys['SEM_INSTRUMENT_NAME'] == instrument_name) & (df_securitys['SEM_TRADING_SYMBOL'].str.split("-").str[0] == underlying),]
    list_expiry = list(df_temp['SEM_EXPIRY_DATE'].unique())
    list_expiry.sort()
    expiry_date = list_expiry[0]
    u_sid = df_temp.loc[(df_securitys['SEM_EXPIRY_DATE'] == expiry_date),'SEM_SMST_SECURITY_ID'].item()
    u_name = df_temp.loc[(df_securitys['SEM_EXPIRY_DATE'] == expiry_date),'SEM_CUSTOM_SYMBOL'].item()
    name = u_name.replace(" ","_")
    tickers[u_sid] = [name]

market_quote_data = list(tickers.keys())


# GETTING THE LTP
market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'MCX_COMM':market_quote_data
}

response =requests.post(url = market_quote_url,headers = header,json = data)
print(response.json())
result = response.json()
ltps = list(result['data'].values())
for i in ltps[0]:
    key = eval(i)
    tickers[key].append(ltps[0][i]['last_price'])

tickers

# GETTING OPTION DETAILS FOR EACH UNDERLYING

instrument_name = "OPTFUT"
opt_tickers = {}
for i in tickers.keys():
    ltp = tickers[i][1]
    u_name = tickers[i][0].split("_")[0]
    df_oc = df_securitys.loc[(df_securitys['SEM_EXM_EXCH_ID'] == exch) & (df_securitys['SEM_INSTRUMENT_NAME'] == instrument_name) & (df_securitys['SEM_TRADING_SYMBOL'].str.split("-").str[0] == u_name),:].copy()
    df_oc.reset_index(inplace = True,drop = True)
    list_expiry = list(df_oc['SEM_EXPIRY_DATE'].unique())
    list_expiry.sort()
    expiry_date = list_expiry[0]
    for j in df_oc.loc[(df_oc['SEM_EXPIRY_DATE'] == expiry_date) & (df_oc['SEM_STRIKE_PRICE'] <= 1.02*ltp) & (df_oc['SEM_STRIKE_PRICE'] >= 0.98*ltp),:].index:
        # print(f"{df_oc.loc[j,'SEM_CUSTOM_SYMBOL']} - {df_oc.loc[j,'SEM_SMST_SECURITY_ID']}")
        opt_tickers[df_oc.loc[j,'SEM_SMST_SECURITY_ID']] = df_oc.loc[j,'SEM_CUSTOM_SYMBOL'].replace(" ","_")
    # print(list(df_oc.loc[(df_oc['SEM_EXPIRY_DATE'] == expiry_date) & (df_oc['SEM_STRIKE_PRICE'] <= 1.02*ltp) & (df_oc['SEM_STRIKE_PRICE'] >= 0.98*ltp),['SEM_SMST_SECURITY_ID','SEM_CUSTOM_SYMBOL']].items()))
opt_tickers

payload_data = []

for i in list(opt_tickers.keys()):
    temp = {
        "ExchangeSegment":'MCX_COMM',
        "SecurityId":str(i)
    }
    payload_data.append(temp)

payload_data

payload = {
    "RequestCode":21,
    "InstrumentCount":len(payload_data),
    "InstrumentList":payload_data
}


# r_json = payload
r_json = json.dumps(payload)

print(r_json)
msg = 0

async def get_data(client_id,access_token):
    global r_json,msg,df_option_chain
    # url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    async with websockets.connect(uri = url,close_timeout=2) as ws:
        await ws.send(r_json)
        while True:
            try :
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            except TimeoutError:
                await ws.send(r_json)
                temp = await asyncio.wait_for(ws.recv(),timeout=20)
            if temp != msg:
                msg = temp
                # print(msg)
                result = FP.process_msg(msg)
                print(result)

asyncio.run(get_data(client_id=client_id,access_token=access_token))

