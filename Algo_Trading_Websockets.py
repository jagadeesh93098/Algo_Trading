import websockets
import pandas as pd
import json
import asyncio
import struct
import csv

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

def get_option_chain(exch,instrument,underlying):
    url = 'https://images.dhan.co/api-data/api-scrip-master.csv'
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


df_opt = get_option_chain('MCX','OPTFUT','CRUDEOIL-')

strike = 6200
option_type = 'CE'
opt = get_opt_details(strike,option_type)
opt_sid = opt[0]
opt_desc = opt[1]

payload = {
    "RequestCode":21,
    "InstrumentCount":1,
    "InstrumentList":[
        {
            "ExchangeSegment":"MCX_COMM",
            "SecurityId":str(opt_sid)
        }
    ]
}

r_json = json.dumps(payload)

field_names = ['LTT','LTP','LTQ','BID QTY','N BID ORDERS', 'BEST BID PRICE','ASK QTY','N ASK ORDERS','BEST ASK PRICE']
with open('temp_data.csv',mode = 'a',newline = '') as file:
    writer = csv.DictWriter(file,fieldnames=field_names)
    writer.writeheader()

msg = 0
async def get_data(client_id,access_token):
    global opt_sid,r_json,msg,strike,option_type
    url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    async with websockets.connect(uri = url,close_timeout=2) as ws:
        await ws.send(r_json)
        count = 0
        while True:
            try :
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            except TimeoutError:
                await ws.send(r_json)
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            if temp != msg:
                msg = temp
                print(f"Packet Received : {msg}")
                ticker = list(struct.unpack('<fHI', msg[8:18]))
                tick = {'LTP':round(ticker[0],2),'LTQ':ticker[1],'LTT':ticker[2]}
                # print(tick)
                p = 62
                l = 62 + 20
                depth = msg[p:l]
                temp = list(struct.unpack("<IIHHff", depth))
                depth_info = {
                    'BID QTY': temp[0],
                    'ASK QTY': temp[1],
                    'N BID ORDERS': temp[2],
                    'N ASK ORDERS': temp[3],
                    'BEST BID PRICE': round(temp[4], 2),
                    'BEST ASK PRICE': round(temp[5], 2)
                }
                # print(depth_info)
                full_data = tick | depth_info
                count+=1
                print(f"Count = {count}",end = "\r")
                with open('temp_data.csv',mode='a',newline="") as file:
                    writer = csv.DictWriter(file,fieldnames=field_names)
                    writer.writerow(full_data)

asyncio.run(get_data(client_id=client_id,access_token=access_token))





































# async def get_data(client_id,access_token):
#     global opt_sid,r_json,msg,strike,option_type
#     url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
#     async with websockets.connect(uri = url,close_timeout=2) as ws:
#         await ws.send(r_json)
#         count = 0
#         while True:
#             temp = await asyncio.wait_for(ws.recv(),timeout=2)
#             if temp != msg:
#                 msg = temp
#                 ticker = list(struct.unpack('<fHI', msg[8:18]))
#                 tick = {'LTP':round(ticker[0],2),'LTQ':ticker[1],'LTT':ticker[2]}
#                 print(tick)
#                 p = 62
#                 l = 62 + 20
#                 depth = msg[p:l]
#                 temp = list(struct.unpack("<IIHHff", depth))
#                 depth_info = {
#                     'BID QTY': temp[0],
#                     'ASK QTY': temp[1],
#                     'N BID ORDERS': temp[2],
#                     'N ASK ORDERS': temp[3],
#                     'BEST BID PRICE': round(temp[4], 2),
#                     'BEST ASK PRICE': round(temp[5], 2)
#                 }
#                 print(depth_info)
#                 print(f"Count = {count}")
#                 count+=1
#             if count == 20:
#                 payload = {
#                         "RequestCode":22,
#                         "InstrumentCount":1,
#                         "InstrumentList":[
#                             {
#                                 "ExchangeSegment":"MCX_COMM",
#                                 "SecurityId":str(opt_sid)
#                             }
#                         ]
#                     }
#                 r_json = json.dumps(payload)
#                 while True:
#                     try :
#                         await ws.send(r_json)
#                         k = await asyncio.wait_for(ws.recv(),timeout = 2)
#                     except:
#                         print('Instrument Unsubscribed')
#                         if option_type == "CE":
#                             option_type = 'PE'
#                         else:
#                             option_type = "CE"
#                         put_opt = get_opt_details(strike,option_type)
#                         opt_sid = put_opt[0]
#                         opt_desc = put_opt[1]
#                         new_payload = {
#                                 "RequestCode":21,
#                                 "InstrumentCount":1,
#                                 "InstrumentList":[
#                                     {
#                                         "ExchangeSegment":"MCX_COMM",
#                                         "SecurityId":str(opt_sid)
#                                     }
#                                 ]
#                             }
#                         r_json = json.dumps(new_payload)
#                         count = 0
#                         await ws.send(r_json)
#                         break

