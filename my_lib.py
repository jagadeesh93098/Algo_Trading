import requests
import pandas as pd
import json

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

# fund_limit = f"time curl --request GET --url https://api.dhan.co/v2/fundlimit --header 'Content-Type: application/json' --header 'access-token:{access_token}'"


def get_fund_limit(access_token):
    fund_limit_url = "https://api.dhan.co/v2/fundlimit"
    headers = {'Content-Type':'application/json',
        'access-token':access_token,
    }
    response = requests.get(url=fund_limit_url,headers = headers)
    if response.status_code != 200:
        print("Error : Check the Output")
    result = response.json()
    data = {'Field_Name':[i for i in result.keys()],'Output':[result[i] for i in result.keys()]}
    df = pd.DataFrame(data)
    return df

get_fund_limit(access_token)

def get_order_book(access_token):
    order_book_url = "https://api.dhan.co/orders"
    headers = {'Content-Type':'application/json',
        'access-token':access_token
    }
    response = requests.get(url = order_book_url,headers=headers)
    if response.status_code != 200:
        print("Error : Check the Output")
    result = response.json()
    data = {}
    for i in result:
        for j in i.keys():
            if j in data.keys():
                data[j].append(i[j])
            else:
                data[j] = [i[j]]
    df = pd.DataFrame(data)
    required_columns = ['orderId', 'correlationId', 'orderStatus', 'transactionType', 'productType', 'orderType', 'tradingSymbol', 'securityId', 'quantity', 'disclosedQuantity', 'price', 'triggerPrice', 'afterMarketOrder','createTime', 'updateTime', 'exchangeTime', 'drvExpiryDate', 'drvOptionType', 'drvStrikePrice', 'omsErrorCode', 'omsErrorDescription', 'filled_qty']
    return df.loc[:,required_columns].copy()

def cancel_order(order_id,access_token):
    url = f'https://api.dhan.co/v2/orders/{order_id}'
    headers = {
        'Content-Type':'application/json',
        'access-token':access_token
    }

    response = requests.delete(url,headers=headers)
    if response.status_code != 200:
        print("Error : Check output")
    return response.json()

def get_positions(access_token):
    url = "https://api.dhan.co/v2/positions"
    headers = {
        'Content-Type':'application/json',
        'access-token':access_token
    }

    response = requests.get(url = url, headers= headers)
    if response.status_code != 200:
        print("Error : Check Output")
    result = response.json()
    data = {}
    for i in result:
        for j in i.keys():
            if j in data.keys():
                data[j].append(i[j])
            else:
                data[j] = [i[j]]
    df = pd.DataFrame(data)
    return df.loc[:,['tradingSymbol', 'securityId', 'positionType','productType', 'buyAvg', 'costPrice', 'buyQty', 'sellAvg', 'sellQty', 'netQty', 'realizedProfit', 'unrealizedProfit', 'dayBuyQty', 'daySellQty', 'dayBuyValue', 'daySellValue']].copy()


# def modify_order(order_id,client_id,)

def curent_atm_strike(client_id,access_token,underlying_security_id):
    market_quote_url = "https://api.dhan.co/v2/marketfeed/ltp"

    header = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "client-id":client_id,
        "access-token":access_token
    }

    data = {
        "IDX_I":[underlying_security_id]
        # "IDX_I":[442]
    }
    
    df_temp = pd.read_csv("today_opt_chain.csv")

    strikes = list(df_temp.loc[:,"SEM_STRIKE_PRICE"])

    strikes.sort(reverse=False)

    response = requests.post(url = market_quote_url,headers=header,json = data)
    result = response.json()
    ltp = result['data']['IDX_I'][str(underlying_security_id)]['last_price']

    atm_strike  = min([x for x in strikes if x > ltp],default= None)
    return atm_strike