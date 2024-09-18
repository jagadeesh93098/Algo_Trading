import requests
import numpy as np
import pandas as pd
import time
import datetime
import sys

def get_option_data():
    start = time.time()
    global headers,url_market_quote,df,idx_ltp,next_most_recent_expiry,Index_name,expiry_code

    today = datetime.date.today()

    compute_days = expiry_code[Index_name][1] - today.weekday()
    if compute_days <0:
        compute_days+=7
    next_most_recent_expiry = today + datetime.timedelta(days = compute_days)
    next_expiry_date = datetime.datetime.strftime(next_most_recent_expiry,format='%Y-%m-%d')

    print(f"Expiry Date = {next_most_recent_expiry}")

    required_columns = ['SEM_EXM_EXCH_ID', 'SEM_SEGMENT', 'SEM_SMST_SECURITY_ID','SEM_INSTRUMENT_NAME', 'SEM_TRADING_SYMBOL',
        'SEM_LOT_UNITS', 'SEM_CUSTOM_SYMBOL', 'SEM_EXPIRY_DATE',
        'SEM_STRIKE_PRICE', 'SEM_OPTION_TYPE', 'SEM_EXCH_INSTRUMENT_TYPE', 'SM_SYMBOL_NAME']

    if Index_name == 'SENSEX' or Index_name == 'BANKNIFTY' or Index_name == 'BANKEX':
        diff = 500
    else:
        diff = 300

    df_midcp_opt_call = df.loc[(df['SEM_TRADING_SYMBOL'].str.startswith(Index_name)) & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_EXPIRY_DATE'].str.startswith(next_expiry_date)) & (df['SEM_OPTION_TYPE'] == 'CE') & (df['SEM_STRIKE_PRICE']<= idx_ltp + diff) & (df['SEM_STRIKE_PRICE'] >= idx_ltp - diff),required_columns].copy()
    df_midcp_opt_call.sort_values(by = 'SEM_STRIKE_PRICE', ascending=True,inplace=True)
    df_midcp_opt_call.reset_index(inplace = True, drop = True)
    # df_midcp_opt_call

    df_midcp_opt_put = df.loc[(df['SEM_TRADING_SYMBOL'].str.startswith(Index_name)) & (df['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df['SEM_EXPIRY_DATE'].str.startswith(next_expiry_date)) & (df['SEM_OPTION_TYPE'] == 'PE') & (df['SEM_STRIKE_PRICE']<= idx_ltp + diff) & (df['SEM_STRIKE_PRICE'] >= idx_ltp - diff),required_columns].copy()
    df_midcp_opt_put.sort_values(by = 'SEM_STRIKE_PRICE', ascending=True,inplace=True)
    df_midcp_opt_put.reset_index(inplace = True, drop = True)

    df_option_chain = pd.concat([df_midcp_opt_call.loc[:,['SEM_SMST_SECURITY_ID','SEM_STRIKE_PRICE']],df_midcp_opt_put.loc[:,['SEM_SMST_SECURITY_ID']]],axis = 1).copy()
    df_option_chain.columns = ['CALL_SECURITY_ID','STRIKE_PRICE','PUT_SECURITY_ID']

    df_option_chain.loc[:,['CALL_I_VAL','CALL_T_VAL','CALL_LTP','PUT_I_VAL','PUT_T_VAL','PUT_LTP']]=np.nan

    df_option_chain = df_option_chain.loc[:,['CALL_SECURITY_ID','CALL_T_VAL','CALL_I_VAL','CALL_LTP','STRIKE_PRICE','PUT_LTP','PUT_I_VAL','PUT_T_VAL','PUT_SECURITY_ID']].copy()

    call_id = list(df_option_chain.loc[:,'CALL_SECURITY_ID'])
    put_id = list(df_option_chain.loc[:,'PUT_SECURITY_ID'])
    all_id = call_id
    all_id.extend(put_id)

    data_opt = {
        "NSE_FNO":all_id,
        "IDX_I":[idx_security_code]
    }
    response = requests.post(url_market_quote,headers=headers,json = data_opt)
    if response.status_code != 200:
        print("Error")
    result = response.json()
    # print(f"Result in Def = {result}")
    idx_ltp = result['data']['IDX_I'][str(idx_security_code)]['last_price']

    for i in result['data']['NSE_FNO'].keys():
        df_option_chain.loc[df_option_chain['PUT_SECURITY_ID'] == int(i),'PUT_LTP'] = result['data']['NSE_FNO'][i]['last_price']
        df_option_chain.loc[df_option_chain['CALL_SECURITY_ID'] == int(i),'CALL_LTP'] = result['data']['NSE_FNO'][i]['last_price']
    # df_option_chain

    df_option_chain['CALL_I_VAL'] = [max(idx_ltp - i,0) for i in df_option_chain['STRIKE_PRICE']]
    df_option_chain['CALL_T_VAL'] = df_option_chain['CALL_LTP'] - df_option_chain['CALL_I_VAL']

    df_option_chain['PUT_I_VAL'] = [max(i-idx_ltp,0) for i in df_option_chain['STRIKE_PRICE']]
    df_option_chain['PUT_T_VAL'] = df_option_chain['PUT_LTP'] - df_option_chain['PUT_I_VAL']

    print(df_option_chain)

    print(f"INDEX_LTP = {idx_ltp}")
    print(f"Time Taken = {time.time() - start}")

expiry_code = {'MIDCPNIFTY':[442,0],'BANKEX':[69,0],'FINNIFTY':[27,1],'BANKNIFTY':[25,2],'NIFTY':[13,3],'SENSEX':[51,4]}

# Index_name = str(input("Type the Index Name - "))
# Index_name = 'FINNIFTY'
Index_name = sys.argv[1]

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

url_market_quote = "https://api.dhan.co/v2/marketfeed/ltp"

headers = {
    "Accept":"application/json",
    "Content-Type":"application/json",
    "access-token":access_token,
    "client-id":client_id
}

# security_url = "https://images.dhan.co/api-data/api-scrip-master.csv"

security_url = "security.csv"

df = pd.read_csv(security_url, low_memory=False)

idx_security_code = expiry_code[Index_name][0]

data_idx = {'IDX_I':[idx_security_code]}

data_idx

# market_quote = f"curl --request POST --url https://api.dhan.co/v2/marketfeed/ltp --header 'Accept: application/json' --header 'Content-Type: application/json' --header 'access-token: {access_token}' --header 'client-id: {client_id}' --data '{data_idx}'"

# print(market_quote)

start = time.time()
response = requests.post(url = url_market_quote,headers= headers,json=data_idx)
# print(f"Time Taken to get Result = {time.time() - start}")
response.status_code
result = response.json()

result['data']

idx_ltp = result['data']['IDX_I'][str(idx_security_code)]['last_price']

idx_ltp

print(f"Sleeping for 1 sec.")
time.sleep(1)

get_option_data()


