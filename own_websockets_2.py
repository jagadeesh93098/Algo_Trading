import asyncio
import websockets
import pandas as pd
import json
import struct
from asyncio import Queue
import datetime


""" 
Rough Idea : 
Start with CE Marketfeed. When Algo Quits, Unsubscribe that particular Option using Option SID. Wait till the Data Flow is stopped. 
Set Timeout for the recv() function. 
Post Time Out, subscribe for appropriate Option Data Flow based on the Output of Algo. Once Subscribed Let the Algo Run. 

EDGE CASES
    1. If there was profit in CE then would like to return back to CE. Should we Unsubscribe and Subscribe again? 

"""

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

# url = 'security.csv'
url = 'https://images.dhan.co/api-data/api-scrip-master.csv'

df = pd.read_csv(url,low_memory = False)

exch = 'MCX'
instrument = 'OPTFUT'
underlying = 'CRUDEOIL-'

list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'].unique())

list_expiry.sort(reverse = False)

expiry_date = list_expiry[0]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'] == expiry_date),:].copy()

def get_opt_sid(strike,option_type):
    global df_opt
    opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']==strike) & (df_opt['SEM_OPTION_TYPE']==option_type),'SEM_SMST_SECURITY_ID'].item()
    option_desc = df_opt.loc[df_opt['SEM_SMST_SECURITY_ID'] == opt_sid,'SEM_CUSTOM_SYMBOL'].item()
    print(f"\nInstrument = {option_desc} : Security_id = {opt_sid}")
    return [opt_sid,option_desc]

strike = 5750
option_type = "CE"
temp = get_opt_sid(strike,option_type)
opt_sid = temp[0]
opt_desc = temp[1]

request = {"RequestCode": 21,
        "InstrumentCount": 1,
        "InstrumentList": [
            {
                "ExchangeSegment": "MCX_COMM",
                "SecurityId": str(opt_sid)
            }
        ]
}

r_json = json.dumps(request)

ltt = 0
dt_b = datetime.datetime(year=1980,month=1,day=1,hour=5,minute=30)
dt_ltt = dt_b + datetime.timedelta(seconds = ltt)
dt_ltt

def client(access_token, client_id):
    async def get_data():
        global r_json, opt_sid, option_desc, df_opt,ltt,dt_b
        url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
        # Initialize a queue for FIFO message handling
        queue = Queue()
        async def message_handler():
            while True:
                # Get the next message from the queue (FIFO)
                msg = await queue.get()
                other = list(struct.unpack('<fHI', msg[8:18]))
                tick = {'LTP': round(other[0], 2), 'LTQ': other[1], 'LTT': other[2]}
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
                print("Tick Data:", tick)
                print("Depth Data:", depth_info)
                print("\n")
                queue.task_done()
        async with websockets.connect(url) as ws:
            # Start message handler as a background task
            asyncio.create_task(message_handler())
            # Send values to the server
            await ws.send(r_json)
            count = 0
            while True:
                if count == 20:
                   u_request = {
                       "RequestCode": 22,
                       "InstrumentCount": 1,
                       "InstrumentList": {
                           {
                               "ExchangeSegment": "MCX_COMM",
                               "SecurityId": str(opt_sid)
                           }
                       }
                   }
                   u_json = json.dumps(u_request)
                   ws.send(u_json)
                   msg = await ws.recv()
                   print(msg)
                # Receive data from websocket
                msg = await ws.recv()
                temp_ltt = struct.unpack('<I',msg[14:18])
                if temp_ltt[0] != ltt:
                    ltt = temp_ltt[0]
                    ltt_cal = datetime.datetime.utcfromtimestamp(ltt)
                    print(datetime.datetime.strftime(ltt_cal,'%Y-%m-%d  %H:%M:%S'))
                    # Put the message into the queue
                    await queue.put(msg)
                    print(count)
                    count+=1
    asyncio.run(get_data())


client(access_token, client_id)



from dhanhq import marketfeed





from dhanhq import dhanhq
