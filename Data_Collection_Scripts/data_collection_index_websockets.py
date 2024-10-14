import websockets
import struct
import pandas as pd
import requests
import datetime
import os
import asyncio
import json

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

security_ids = {
        'MIDCPNIFTY':442,
        'BANKEX':69,
        'FINNIFTY':27,
        'BANKNIFTY':25,
        'NIFTY':13,
        'SENSEX':51,
    }

main_path = os.getcwd()

# Checking if there is data directory if not then creating one.
if 'data' not in [i for i in os.listdir() if os.path.isdir(i)]:
    print(f"data directory not found at the current path. Creating one.")
    os.mkdir('data')
else:
    print(f"data directory found.")

# Checking if there is Date (yyyymmdd) directory in data
today = datetime.datetime.today()
today_date = datetime.datetime.strftime(today,'%Y%m%d')
os.chdir('data')
if today_date in [i for i in os.listdir() if os.path.isdir(i)]:
    print(f"{today_date} directory not found in data. Creating one.")
    os.mkdir(today_date)
else:
    print(f"{today_date} directory found in data.")

# Checking if there is a directory for Indices in today_date we're gonna capture data about.
os.chdir(today_date)
for i in list(security_ids.keys()):
    if i not in [d for d in os.listdir() if os.path.isdir(d)]:
        print(f"{i} not found in {today_date}. Creating one.")
        os.mkdir(i)
    else:
        print(f"{i} directory found in {today_date}.")

# Going back to main path.
os.chdir(main_path)

df_securitys = pd.read_csv("temp_data/securitys.csv",low_memory=False)

print(f"Getting Data of the Following Underlyings")
print(f"{list(security_ids.keys())}")

# Getting LTPs of Indices using Market Quote
market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'IDX_I':list(security_ids.values())
}

response = requests.post(url = market_quote_url,headers = header,json = data)
result= response.json()['data']['IDX_I']

response.json()


ltps = {}
for i in list(result.keys()):
    underlying_names = list(security_ids.keys())
    underlying_names
    u_sid = list(security_ids.values())
    print(u_sid)
    print(result[i]['last_price'])
    ltps[underlying_names[u_sid.index(eval(i))]] = result[i]['last_price']

ltps

full_payload_data = []
d_instruments = []

for i in list(ltps.keys()):
    df_opt = pd.read_csv(f"temp_data/{i}.csv")
    print(df_opt)
    df_final_opt = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] <= ltps[i] * 1.02) & (df_opt['SEM_STRIKE_PRICE'] >= ltps[i] * 0.98),:].copy()
    df_final_opt.reset_index(inplace = True,drop = True)
    print(df_final_opt)
    for index in list(df_final_opt.index):
        temp = {}
        if i == 'NIFTY' or i == 'MIDCPNIFTY' or i == 'BANKNIFTY' or i == 'FINNIFTY':
            temp['ExchangeSegment'] = 'NSE_FNO'
        else:
            temp['ExchangeSegment'] = 'BSE_FNO'
        temp['SecurityId'] = df_final_opt.loc[index,'SEM_SMST_SECURITY_ID'].astype(str)
        print(temp)
        full_payload_data.append(temp)
        d_instruments.append({temp['SecurityId']:df_final_opt.loc[index,'SEM_CUSTOM_SYMBOL'].replace(" ","_")})

websockets_url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"

def message_structure(payload_data):
    payload = {
        "RequestCode":21,
        "InstrumentCount":len(payload_data),
        "InstrumentList":payload_data
    }
    r_json = json.dumps(payload)
    return r_json


async def subscribe_instruments(ws,payload_data):
    l = len(payload_data)
    if l > 100:
        n = l//100
        r = l%100
        for i in range(0,n):
            start = 100*i
            end = 100*(i+1)
            payload_chunk = payload_data[start:end]
            send_msg = message_structure(payload_chunk)
            await ws.send(send_msg)
        payload_chunk = payload_data[end:end+r]
        await ws.send(message_structure(payload_chunk))
    else:
        await ws.send(message_struct(payload_data))
    print("Subscription Packet(s) sent")

async def get_data(payload_data):
    global websockets_url
    async with websockets.connect(uri = websockets_url) as ws:
        await subscribe_instruments(ws,payload_data)
    while True:
        msg = await ws.recv()
        print(msg)

asyncio.run(get_data(payload_data=full_payload_data))
