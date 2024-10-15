import websockets
import struct
import pandas as pd
import requests
import datetime
import os
import asyncio
import json
import FULL_PACKET as FP
import csv

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
if 'data_websocket' not in [i for i in os.listdir() if os.path.isdir(i)]:
    print(f"data directory not found at the current path. Creating one.")
    os.mkdir('data_websocket')
else:
    print(f"data directory found.")

# Checking if there is Date (yyyymmdd) directory in data
today = datetime.datetime.today()
today_date = datetime.datetime.strftime(today,'%Y%m%d')
os.chdir('data_websocket')
if today_date not in [i for i in os.listdir() if os.path.isdir(i)]:
    print(f"{today_date} directory not found in data_websocket. Creating one.")
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
    # underlying_names
    u_sid = list(security_ids.values())
    # print(u_sid)
    print(result[i]['last_price'])
    ltps[underlying_names[u_sid.index(eval(i))]] = result[i]['last_price']

ltps

full_payload_data = []
d_instruments = {}

for i in list(ltps.keys()):
    df_opt = pd.read_csv(f"temp_data/{i}.csv")
    # print(df_opt)
    df_final_opt = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] <= ltps[i] * 1.02) & (df_opt['SEM_STRIKE_PRICE'] >= ltps[i] * 0.98),:].copy()
    df_final_opt.reset_index(inplace = True,drop = True)
    # print(df_final_opt)
    for index in list(df_final_opt.index):
        temp = {}
        if i == 'NIFTY' or i == 'MIDCPNIFTY' or i == 'BANKNIFTY' or i == 'FINNIFTY':
            temp['ExchangeSegment'] = 'NSE_FNO'
        else:
            temp['ExchangeSegment'] = 'BSE_FNO'
        temp['SecurityId'] = df_final_opt.loc[index,'SEM_SMST_SECURITY_ID'].astype(str)
        # print(temp)
        full_payload_data.append(temp)
        d_instruments[temp['SecurityId']] = df_final_opt.loc[index,'SEM_CUSTOM_SYMBOL'].replace(" ","_")

d_instruments
# CREATING CSV FILES WITH HEADERS IN APPROPRIATE FOLDERS
os.chdir('data_websocket')
os.chdir(f'{today_date}')

field_names = ['SECURITY_ID', 'LTP', 'LTQ', 'LTT', 'ATP', 'VOLUME', 'TOTAL_SELL_QTY', 'TOTAL_BUY_QTY', 'OI', 'HIGHEST_OI', 'LOWEST_OI', 'DAY_OPEN_VALUE', 'DAY_CLOSE_VALUE', 'DAY_HIGH_VALUE', 'DAY_LOW_VALUE', 'DEPTH_1', 'DEPTH_2', 'DEPTH_3', 'DEPTH_4', 'DEPTH_5']

for i in d_instruments.keys():
    instrument_name = d_instruments[i]
    sub_dir = instrument_name.split("_")[0]
    file_name = f"{instrument_name}.csv"
    file_path = f"{sub_dir}/{file_name}"
    with open(file_path,mode = 'w',newline = '') as f:
        writer = csv.DictWriter(f,fieldnames = field_names)
        writer.writeheader()

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
    while True:
        try :
            async with websockets.connect(uri = websockets_url,max_queue = None) as ws:
                await subscribe_instruments(ws,payload_data)
                while True:
                    msg = await ws.recv()
                    if struct.unpack('<B',msg[0:1])[0] == 8:
                        # print(len(msg))
                        result = FP.process_msg(msg)
                        print(result,end="\n\n")
                        temp_security_id = result['SECURITY_ID']
                        instrument_name = d_instruments[str(temp_security_id)]
                        sub_dir = instrument_name.split("_")[0]
                        file_name = f"{instrument_name}.csv"
                        file_path = f"{sub_dir}/{file_name}"
                        with open(file_path,mode = 'a',newline='') as f:
                            writer = csv.DictWriter(f,fieldnames=field_names)
                            writer.writerow(result)
                        print(f"Written data into {file_name}")
        except websockets.ConnectionClosedError:
                break

asyncio.run(get_data(payload_data=full_payload_data))
