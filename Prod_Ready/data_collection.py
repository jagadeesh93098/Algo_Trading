import csv
import pandas as pd
import requests
import os
import datetime
import time


today = datetime.datetime.today()
today_date = datetime.datetime.strftime(today,"%Y%m%d")
print(f"Today Date = {today_date}")

security_url = 'https://images.dhan.co/api-data/api-scrip-master.csv'

field_names = [
    'last_trade_time',
    'last_price',
    'last_quantity',
    'average_price',
    'buy_quantity',
    'sell_quantity',
    'oi',
    'volume',
    'depth',
]

df_securitys = pd.read_csv(security_url,low_memory=False)

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzMxMjE2NTIyLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.Omk-jrneTsP4Cz3lDC7qn23xiKd0mgH34o4qY4FViHglS86x9sfapJsXyb6KBTysd3ZnyLmggLsPnRQ5j2zQTg"

security_ids = {
        'MIDCPNIFTY':442,
        'BANKEX':69,
        'FINNIFTY':27,
        'BANKNIFTY':25,
        'NIFTY':13,
        'SENSEX':51,
    }

# CHECKING IF DATE FOLDER IS PRESENT IN DATA
main_path = os.getcwd()
os.chdir('data')
if today_date not in [i for i in os.listdir() if os.path.isdir(i)]:
    os.mkdir(today_date)
os.chdir(today_date)

# underlyings = ['SENSEX']
underlyings = list(security_ids.keys())

print("\nUnderlyings Selected are as Follows")
print(underlyings)
print("\n")

# CHECKING IF EACH FOLDER FOR UNDERLYING IS PRESENT IN DATE FOLDER
for i in underlyings:
    if i not in [i for i in os.listdir() if os.path.isdir(i)]:
        print(f"{i} not Found in Date Folder. Making one")
        os.mkdir(i)

# GET MARKET QUOTE FOR UNDERLYINGS
underlyings_security_id = []
for underlying in underlyings:
    underlyings_security_id.append(security_ids[underlying])

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
start = time.time()

# print(f"Status Code of Response = {response.status_code}")
result = response.json()['data']['IDX_I']


result_keys = [eval(i) for i in result.keys()]
security_names = list(security_ids.keys())
security_values = list(security_ids.values())

ltps = {}
for i in result_keys:
     idx_name = security_names[security_values.index(i)]
     print(idx_name)
     ltps[idx_name] = result[str(i)]['last_price']

print("LTPs of the UNDERLYINGS SELECTED")
print(f"{ltps}\n")

print("Ranges between which strikes are considered for Collection of Data")
for i in ltps.keys():
    print(i,round(ltps[i]*0.98,2),ltps[i],round(ltps[i]*1.02,2),"\n")

option_desc = {}

# payload_data =[]
for i in ltps.keys():
    df_oc = df_securitys.loc[(df_securitys['SEM_INSTRUMENT_NAME'] == 'OPTIDX') & (df_securitys['SEM_TRADING_SYMBOL'].str.split("-").str[0] == i),:].copy()
    list_expiry = list(df_oc['SEM_EXPIRY_DATE'].unique())
    expiry_date = min(list_expiry)
    df_opt = df_oc.loc[(df_oc['SEM_EXPIRY_DATE'] == expiry_date),:].copy()
    df_temp = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']<=ltps[i]*1.02) & (df_opt['SEM_STRIKE_PRICE']>=ltps[i]*0.98),:].copy()
    df_temp.reset_index(inplace = True,drop = True)
    exch = ""
    if i == 'NIFTY' or i == 'FINNIFTY' or i == 'MIDCPNIFTY' or i == 'BANKNIFTY':
        exch = "NSE_FNO"
    else:
        exch = "BSE_FNO"
    for j in list(df_temp.index):
        opt_sid = df_temp.loc[j,'SEM_SMST_SECURITY_ID'].item()
        temp_name = df_temp.loc[j,'SEM_CUSTOM_SYMBOL']
        opt_desc = temp_name.replace(" ","_")
        option_desc[opt_sid] = opt_desc

option_desc

print(f"The Total Number of Instruments = {len(list(option_desc.keys()))}\n")
print(option_desc)

for i in list(option_desc.values()):
    file_name = f"{i}.csv"
    sub_dir = f"{i.split("_")[0]}"
    file_path = f"{sub_dir}/{file_name}"
    print(file_path)
    with open(file_path,mode = 'w',newline = "") as f:
        writer = csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()

for i in list(security_ids.values()):
    file_name = f"index_{i}.csv"
    sub_dir = 'Index'
    file_path = f"{sub_dir}/{file_name}"
    print(file_path)
    with open(file_path,mode = 'w',newline = '') as f:
        writer = csv.DictWriter(f,fieldnames=field_names)
        writer.writeheader()

os.getcwd()

market_quote_url = "https://api.dhan.co/v2/marketfeed/quote"
header = {
    "Accept":"application/json",
    "Content-Type":'application/json',
    'client-id':client_id,
    'access-token':access_token
}


data_nse_fno = []
data_bse_fno = []

for i in option_desc.keys():
    if "NIFTY" in option_desc[i] or "BANKNIFTY" in option_desc[i] or "MIDCPNIFTY" in option_desc[i] or "FINNIFTY" in option_desc[i]:
        data_nse_fno.append(i)
    else:
        data_bse_fno.append(i)

data = {
    'BSE_FNO':data_bse_fno,
    'NSE_FNO':data_nse_fno,
    'IDX_I':list(security_ids.values())
}

data

if time.time() - start < 1:
    time.sleep(1 - time.time() + start)

while True:
    # print(f"Status Code of Response = {response.status_code}")
    response = requests.post(url = market_quote_url,headers = header,json = data)
    bse_result = response.json()['data']['BSE_FNO']
    nse_result = response.json()['data']['NSE_FNO']
    idx_results = response.json()['data']['IDX_I']
    result = {**bse_result,**nse_result}
    for i in list(result.keys()):
        file_name = f"{option_desc[eval(i)]}.csv"
        sub_dir = f"{option_desc[eval(i)].split("_")[0]}"
        file_path = f"{sub_dir}/{file_name}"
        print(file_path,end = " ;")
        output = {}
        for fname in field_names:
            output[fname] = result[i][fname]
        with open(file_path,mode = 'a',newline = '') as f:
            writer = csv.DictWriter(f,fieldnames=field_names)
            writer.writerow(output)
    for i in list(idx_results.keys()):
        sub_dir = security_names[security_values.index(eval(i))]
        file_name = f"index_{sub_dir}.csv"
        file_path = f"{sub_dir}/{file_name}"
        output= {}
        for fname in field_names:
            output[fname] = idx_results[i][fname]
        with open(file_path,mode = 'a',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=field_names)
            writer.writerow(output)
    time.sleep(1)
