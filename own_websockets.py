import time
import websockets
import asyncio
import struct
import json
import pandas as pd

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
option_type = 'CE'
temp = get_opt_sid(strike,option_type)
opt_sid = temp[0]
option_desc = temp[1]

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"



import asyncio
import websockets
import struct
import time
import json
from asyncio import Queue
from concurrent.futures import TimeoutError

# Initialize global variables to track data points and option type
data_point_count = 0
option_type = "PE"  # Initial option type
subscribed_sid = None  # To track currently subscribed SecurityId
timeout_duration = 1  # Timeout for detecting no data flow (in seconds)

def get_opt_sid(strike, option_type):
    global df_opt
    opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE'] == strike) & (df_opt['SEM_OPTION_TYPE'] == option_type), 'SEM_SMST_SECURITY_ID'].item()
    option_desc = df_opt.loc[df_opt['SEM_SMST_SECURITY_ID'] == opt_sid, 'SEM_CUSTOM_SYMBOL'].item()
    print(f"\nInstrument = {option_desc} : Security_id = {opt_sid}")
    return [opt_sid, option_desc]

def switch_option_type():
    global option_type
    # Toggle between "PE" and "CE"
    if option_type == "PE":
        option_type = "CE"
    else:
        option_type = "PE"

async def subscribe(ws, opt_sid):
    """Function to subscribe to an option."""
    subscribe_request = {
        "RequestCode": 21,
        "InstrumentCount": 1,
        "InstrumentList": [
            {
                "ExchangeSegment": "MCX_COMM",
                "SecurityId": str(opt_sid)
            }
        ]
    }
    r_json = json.dumps(subscribe_request)
    await ws.send(r_json)
    print(f"Subscribed to SecurityId: {opt_sid}")

async def unsubscribe(ws, opt_sid):
    """Function to unsubscribe from an option."""
    unsubscribe_request = {
        "RequestCode": 22,
        "InstrumentCount": 1,
        "InstrumentList": [
            {
                "ExchangeSegment": "MCX_COMM",
                "SecurityId": str(opt_sid)
            }
        ]
    }
    r_json = json.dumps(unsubscribe_request)
    await ws.send(r_json)
    print(f"Unsubscribed from SecurityId: {opt_sid}")

async def wait_for_unsubscribe(ws):
    """Function to wait for data stop or an error after unsubscribe."""
    try:
        # Wait for a message with a timeout
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=timeout_duration)
                print(f"Still receiving data after unsubscribe, message: {msg}")
            except TimeoutError:
                # If no message is received within the timeout, assume data flow has stopped
                print("No data received within the timeout. Assuming unsubscription successful.")
                break
    except Exception as e:
        # Once an error occurs, this indicates data has stopped flowing
        print("Error detected, assuming unsubscription successful.")
        return

async def message_handler(queue, ws, strike):
    global data_point_count, option_type, subscribed_sid

    while True:
        try:
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
            print(f"Option Type: {option_type}")
            print("Tick Data:", tick)
            print("Depth Data:", depth_info)
            print("\n")
            # Update data point count
            data_point_count += 1
            print(f'Data Point Count = {data_point_count}')
            # Switch option type after every 20 data points
            if data_point_count >= 20:
                # Unsubscribe from the current option
                await unsubscribe(ws, subscribed_sid)
                # Wait for unsubscription to complete (i.e., data stops or error)
                await wait_for_unsubscribe(ws)
                # Switch the option type
                switch_option_type()
                # Fetch new opt_sid and option_desc based on the new option_type
                opt_sid, option_desc = get_opt_sid(strike, option_type)
                # Subscribe to the new option
                await subscribe(ws, opt_sid)
                # Update subscribed_sid with the new SecurityId
                subscribed_sid = opt_sid
                # Reset the counter after switching
                data_point_count = 0
            queue.task_done()

        except Exception as e:
            print(f"Error: {e}")
            continue

def client(access_token, client_id, strike):
    async def get_data():
        global subscribed_sid
        url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
        # Initialize a queue for FIFO message handling
        queue = Queue()
        async with websockets.connect(url) as ws:
            # Get the initial opt_sid and option_desc for the default option_type
            opt_sid, option_desc = get_opt_sid(strike, option_type)
            # Subscribe to the initial option
            await subscribe(ws, opt_sid)
            # Set the current subscribed SecurityId
            subscribed_sid = opt_sid
            # Start message handler as a background task
            asyncio.create_task(message_handler(queue, ws, strike))
            # Receive data from websocket and add to queue
            while True:
                try:
                    msg = await ws.recv()
                    await queue.put(msg)
                except websockets.ConnectionClosed:
                    print("Connection closed, retrying...")
                    break
    asyncio.run(get_data())

# Example Usage:
# Set the strike price you are interested in
# strike_price = 15000
# client(access_token, client_id, strike_price)



# Example Usage:
# Set the strike price you are interested in
strike_price = 5700
client(access_token, client_id, strike_price)


from dhanhq import marketfeed























































































r = {"RequestCode" : 21,
    "InstrumentCount" : 1,
    "InstrumentList" : [
        {
            "ExchangeSegment" : "MCX_COMM",
            "SecurityId" : str(opt_sid)
        }
    ]
}

r_json = json.dumps(r)



def client(access_token,client_id):
    async def get_data():
        global r_json,opt_sid,option_desc,df_opt
        url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
        async with websockets.connect(url) as ws:
        # Send values to the server
            count = 0
            await ws.send(r_json)
            while True:
                # exit = False
                start = time.time()
                msg = await ws.recv()
                # print(len(msg[8:18]))
                other = list(struct.unpack('<fHI',msg[8:18]))
                tick = {'LTP':round(other[0],2),'LTQ':other[1],'LTT':other[2]}
                # print(option_desc,tick,end = '-----')
                p = 62
                l = 62 + 20
                depth = msg[p:l]
                temp = list(struct.unpack("<IIHHff",depth))
                depth = {'BID QTY =':temp[0],'ASK QTY =':temp[1],'N BID ORDERS =':temp[2],'N ASK ORDERS =':temp[3],'BEST BID PRICE':round(temp[4],2),'BEST ASK PRICE':round(temp[5],2)}
                print(depth)
                print("\n" )
                # print(f"Time Taken = {time.time() - start} and Count = {count}\n")
                count +=1
    asyncio.run(get_data())

client(access_token,client_id)




# CHATGPT CODE

import asyncio
import websockets
import struct
import time
from asyncio import Queue

def client(access_token, client_id):
    async def get_data():
        global r_json, opt_sid, option_desc, df_opt
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

            while True:
                # Receive data from websocket
                msg = await ws.recv()

                # Put the message into the queue
                await queue.put(msg)

    asyncio.run(get_data())

client(access_token, client_id)


