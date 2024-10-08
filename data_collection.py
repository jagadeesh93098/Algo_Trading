import websockets
import csv
import struct
import pandas as pd
import requests
import os
import datetime
import json
import FULL_PACKET as FP
import asyncio

today = datetime.datetime.today()
today_date = datetime.datetime.strftime(today,"%Y%m%d")
print(f"Today Date = {today_date}")

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

underlyings = list(security_ids.keys())
dirs = [i for i in os.listdir() if os.path.isdir(i)]

# if "data" not in dirs:
#     os.mkdir("data")

# os.chdir("data")

# temp_dir = [i for i in os.listdir() if os.path.isdir(i)]
# if today_date not in temp_dir:
#         os.mkdir(today_date)
# os.chdir(today_date)
# for i in underlyings:
#      if i not in [i for i in os.listdir() if os.path.isdir(i)]:
#           os.mkdir(i)

# os.chdir(main_path)

# GET MARKET QUOTE FOR UNDERLYINGS

underlyings_security_id = []
for underlying in underlyings:
    underlyings_security_id.append(security_ids[underlying])

underlyings_security_id

market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}
data = {
    'IDX_I':underlyings_security_id
}

response = requests.post(url = market_quote_url,headers = header,json = data)
# print(f"Status Code of Response = {response.status_code}")
result = response.json()['data']['IDX_I']

result_keys = [eval(i) for i in result.keys()]
security_names = list(security_ids.keys())
security_values = list(security_ids.values())

ltps = {}
for i in result_keys:
     idx_name = security_names[security_values.index(i)]
    #  print(idx_name)
     ltps[idx_name] = result[str(i)]['last_price']

for i in ltps.keys():
     print(i,round(ltps[i]*0.98,2),ltps[i],round(ltps[i]*1.02,2))
ltps

data =[]
for i in ltps.keys():
    df_a = pd.read_csv(f"temp_data/{i}.csv")
    df_temp = df_a.loc[(df_a['SEM_STRIKE_PRICE']<=ltps[i]*1.02) & (df_a['SEM_STRIKE_PRICE']>=ltps[i]*0.98),:].copy()
    df_temp.reset_index(inplace = True,drop = True)
    exch = ""
    if i == 'NIFTY' or i == 'FINNIFTY' or i == 'MIDCPNIFTY' or i == 'BANKNIFTY':
        exch = "NSE_FNO"
    else:
        exch = "BSE_FNO"
    for j in list(df_temp['SEM_SMST_SECURITY_ID']):
        temp = {"ExchangeSegment":exch,"SecurityId":str(j)}
        data.append(temp)

data

payload = {
    "RequestCode":21,
    "InstrumentCount":len(data),
    "InstrumentList":data
}


r_json = json.dumps(payload)


# os.chdir(f'data/{today_date}')

async def get_data(client_id,access_token):
    global opt_sid,r_json,msg,df
    url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"
    async with websockets.connect(uri = url,close_timeout=2) as ws:
        await ws.send(r_json)
        while True:
            try :
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            except TimeoutError:
                await ws.send(r_json)
                temp = await asyncio.wait_for(ws.recv(),timeout=2)
            if temp != msg:
                msg = temp
                result = FP.process_msg(temp)
                temp_name = df.loc[df['SEM_SMST_SECURITY_ID'] == result['SECURITY_ID'],'SEM_CUSTOM_SYMBOL'].item()
                print(f"{temp_name} - {result}")
                # name = temp_name.replace(" ","_")
                # sub_dir = f"{name.split('_')[0]}"
                # os.chdir(sub_dir)
                # file_name = f"{name}.csv"
                # if file_name in [i for i in os.listdir()]:
                #     with open(file_name,mode = 'a',new_line = '') as f:
                #         writer = csv.DictWriter(f,fieldnames = FP.field_names)
                #         writer.writerow(result)
                #     os.chdir(f"data/{today_date}")
                # else:
                #     with open(file_name,mode = 'w', new_line = '') as f:
                #         writer = csv.DictWriter(f,fieldnames=FP.field_names)
                #         writer.writeheader()
                #     os.chdir(f"data/{today_date}")

asyncio.run(get_data(client_id=client_id,access_token=access_token))
