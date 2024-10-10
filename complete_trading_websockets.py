import websockets
import pandas as pd
import json
import asyncio
import struct
import requests
import csv
import sys

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

# underlying = sys.argv[1]
underlying = 'NIFTY'

security_ids = {
        'MIDCPNIFTY':442,
        'BANKEX':69,
        'FINNIFTY':27,
        'BANKNIFTY':25,
        'NIFTY':13,
        'SENSEX':51,
    }

exch = ""
if underlying == 'NIFTY' or underlying == 'BANKNIFTY' or underlying == 'FINNIFTY' or underlying == 'MIDCPNIFTY':
    exch = 'NSE'
else:
    exch = 'BSE'

underlying_sid = security_ids[underlying]

# GET MARKET QUOTE
market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'IDX_I':[underlying_sid]
}

response = requests.post(url = market_quote_url,headers = header,json = data)

result = response.json()['data']['IDX_I']

ltp = result[str(underlying_sid)]['last_price']

ltp

df_securitys = pd.read_csv("temp_data/securitys.csv",low_memory=False)

instrument_name = 'OPTIDX'
df_oc = pd.read_csv(f'temp_data/{underlying}.csv')
df_oc.reset_index(inplace=True,drop=True)

strikes = list(df_oc.loc[df_oc['SEM_STRIKE_PRICE']<=ltp,'SEM_STRIKE_PRICE'])

atm_strike = max(strikes)

atm_strike

call_strike_sid = df_oc.loc[(df_oc['SEM_STRIKE_PRICE'] == atm_strike) & (df_oc['SEM_OPTION_TYPE'] == 'CE'),'SEM_SMST_SECURITY_ID'].item()

put_strike_sid = df_oc.loc[(df_oc['SEM_STRIKE_PRICE'] == atm_strike) & (df_oc['SEM_OPTION_TYPE'] == 'PE'),'SEM_SMST_SECURITY_ID'].item()

exch_segment = ""
if exch == "NSE":
    exch_segment = "NSE_FNO"
else:
    exch_segment = 'BSE_FNO'

payload = {
    "RequestCode":15,
    "InstrumentCount":1,
    "InstrumentList":[
        {
            "ExchangeSegment":exch_segment,
            "SecurityId":str(all_strike_sid)
        }
    ]
}

r_json = json.dumps(payload)

msg = ""

async def get_data(client_id,access_token):
    global opt_sid,r_json,msg,strike,option_type,field_names
    url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    async with websockets.connect(uri = url,close_timeout=2) as ws:
        await ws.send(r_json)
        while True:
            try :
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
                if temp != msg:
                    msg = temp
                    sid = list(struct.unpack('<I',msg[4:8]))
                    ticker = list(struct.unpack('<f', msg[8:12]))
                    temp = {'sid':sid[0],'ticker':ticker[0],'msg':msg}
                    print(temp)
                    with open("test_data_collection.csv",mode = 'a',newline = "") as f:
                        writer = csv.DictWriter(f,fieldnames=field_names)
                        writer.writerow(temp)
            except TimeoutError:
                await ws.send(r_json)
            continue

asyncio.run(get_data(client_id=client_id,access_token=access_token))

