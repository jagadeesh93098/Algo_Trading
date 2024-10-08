import requests
import pandas as pd
import json
import my_lib


""" 
THINGS TO DO
    1. Try to test for Order Modification requests and the limitations that are present with it. 
    2. Figure out how to Incorporate when the Algo goes Live, meaning should we track the Position (or) LTP from Marketfeed?
"""

security_url = 'https://images.dhan.co/api-data/api-scrip-master.csv'

df = pd.read_csv(security_url)

exch = "NSE"
instrument = "OPTIDX"
underlying = "MIDCPNIFTY"

list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'].unique())

list_expiry.sort(reverse = False)

expiry_date = list_expiry[0]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'] == expiry_date),:].copy()

df_opt

strike = 13675
option_type = "CE"

opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']==strike) & (df_opt['SEM_OPTION_TYPE']==option_type),'SEM_SMST_SECURITY_ID'].item()


client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

data = {
    "dhanClientId": client_id,
    "correlationId": "a123c345",
    "transactionType": "BUY",
    "exchangeSegment": "NSE_FNO",
    "productType": "MARGIN",
    "orderType": "LIMIT",
    "validity": "DAY",
    "securityId": "87051",
    "quantity": 50,
    "disclosedQuantity": 50,
    "price": 0.20,
    "triggerPrice": "",
    "afterMarketOrder": True,
    "amoTime": "OPEN",
    "boProfitValue": "",
    "boStopLossValue": ""
}

url = "https://api.dhan.co/v2/orders/"

request_structure = {
    "Accept" : "application/json",
    "Content_Type" : "application/json",
    "access-token" : access_token
}

response = requests.post(url = url, headers= request_structure,json=data)

response.json()

df_orders = my_lib.get_order_book(access_token=access_token)

df_orders

client_id

order_id = df_orders.loc[df_orders['orderStatus']=='PENDING','orderId'].item()

order_id

# ORDER MODIFICATION
order_modify_url = f"https://api.dhan.co/v2/orders/{order_id}"

header = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "access-token" : access_token
}

data = {
    "dhanClientId":"1000000009",
    "orderId":"112111182045",
    "orderType":"LIMIT",
    "legName":"",
    "quantity":"40",
    "price":"3345.8",
    "disclosedQuantity":"10",
    "triggerPrice":"",
    "validity":"DAY"
}


response = requests.put(url = order_modify_url,headers=header,json = data)

response.json()


    # curl --request PUT \
    # --url https://api.dhan.co/v2/orders/{order-id} \
    # --header 'Content-Type: application/json' \
    # --header 'access-token: JWT' \
    # --data '{Request JSON}'



# count = 10



# for i in range(0,)

# my_lib.cancel_order(order_id=order_id,access_token=access_token)

