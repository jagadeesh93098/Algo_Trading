from dhanhq import marketfeed
import pandas as pd
import math
import numpy as np

step = 0.05
def calculate_qty(fund,ltp):
    global lot_size
    return lot_size * math.floor(fund/(ltp*lot_size))

def calculate_price(price,percent):
    return step * (math.floor(price*(1+percent)/step)-1)

# url = 'security.csv'
url = 'https://images.dhan.co/api-data/api-scrip-master.csv'

client_id = "1104088864"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI5MTExMjIxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDA4ODg2NCJ9.COQOjTvQ0Cmmjs660wwgYd1jnmi34_wla-keJue08L0-Gv4kGarBedXHOJ9i06kRprRqZOM4u1NtLleZcbKSRQ"

df = pd.read_csv(url,low_memory = False)

exch = 'NSE'
instrument = 'OPTIDX'
underlying = 'MIDCPNIFTY'

list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'].unique())

list_expiry.sort(reverse = False)

expiry_date = list_expiry[0]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE'] == expiry_date),:].copy()

df_opt

def analysis(strike,option_type):
    global df
    option_type = option_type
    strike = strike
    opt_sid = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']==strike) & (df_opt['SEM_OPTION_TYPE']==option_type),'SEM_SMST_SECURITY_ID'].item()
    print(opt_sid)
    option_desc = df_opt.loc[df_opt['SEM_SMST_SECURITY_ID'] == opt_sid,'SEM_CUSTOM_SYMBOL'].item()
    option_desc
    lot_size = df_opt.loc[(df_opt['SEM_STRIKE_PRICE']==strike) & (df_opt['SEM_OPTION_TYPE']==option_type),'SEM_LOT_UNITS'].item()

    instruments = [(2,str(opt_sid),15)]

    feed = marketfeed.DhanFeed(client_id = client_id, access_token = access_token, instruments = instruments)
    feed.run_forever()

    # feed.close_connection()
    response = feed.get_data()

    ltp = eval(response['LTP'])

    df_test = pd.DataFrame({"OPTION_DESC":[option_desc],"LTP":[ltp],"r_LTP":[np.nan],"r_change":[np.nan]})

    buy_price = ltp

    fund = 10000
    qty = calculate_qty(fund,ltp)
    i_tpp = 0.2
    i_slp = -0.1
    tp_price = calculate_price(ltp,i_tpp)
    sl_price = calculate_price(ltp,i_slp)
    pp = 0
    slp = (sl_price - buy_price)/buy_price
    tpp = (tp_price - buy_price)/buy_price

    trigger = sl_price + step
    max_pp = 0

    df = pd.DataFrame({
        'OPTION_DESC':[option_desc],
        'BUY_PRICE':[buy_price],
        'QTY':[qty],
        'LTP':[ltp],
        'LTP_CHANGE':[np.nan],
        'PP':[0],
        'MAX_PP':[0],
        'MAX_PP_CHANGE':[0],
        'SLP':[slp],
        'SL_PRICE_RISK':[sl_price],
        'SL_PRICEMV':[sl_price],
        'SL_PRICE':[sl_price],
        'TRIGGER':[sl_price + step],
        'TPP':[tpp],
        'TP_PRICE':[tp_price],
        'SELL_PRICE':[np.nan],
        'P-L':[np.nan]})
    len(df.columns)

    exit = False
    while exit != True:
        response = feed.get_data()
        ltp0 = ltp
        ltp = eval(response['LTP'])
        ltp_change = (ltp - ltp0)
        pp = (ltp - buy_price)/buy_price
        if pp >= max_pp:
            max_pp = pp
        pp_change = max_pp - pp
        if pp >= tpp:
            tpp = pp + 0.05
            tp_price = calculate_price(buy_price,tpp)
        if ltp <= trigger:
            exit = True
            sell_price = sl_price
            pl = qty*(sl_price - buy_price) - 40
            df.loc[len(df.index)] = [option_desc,buy_price,qty,ltp,ltp_change,pp,max_pp,pp_change,slp,sl_price_risk,sl_pricemv,sl_price,trigger,tpp,tp_price,sell_price,pl]
            print(df)
            break
        sl_price0 = sl_price
        slp0 = slp
        if ltp_change != 0:
            sl_pricemv = min(sl_price0 + step * (1 + math.floor(pp_change*math.exp(1000*(-(ltp_change/abs(ltp_change))*pp_change)))),ltp - 2*step)
        else:
            sl_pricemv = min(sl_price0 + step * (1 + math.floor(pp_change*math.exp(500*(pp_change)))),ltp - 2*step)
        slp_risk = max(slp,(3*pp - tpp)/2)
        sl_price_risk = calculate_price(buy_price,slp_risk)
        sl_price = max(sl_pricemv,sl_price_risk,sl_price0)
        trigger = sl_price + step
        slp = (sl_price - buy_price)/buy_price
        df.loc[len(df.index)] = [option_desc,buy_price,qty,ltp,ltp_change,pp,max_pp,pp_change,slp,sl_price_risk,sl_pricemv,sl_price,trigger,tpp,tp_price,np.nan,np.nan]
        print(df)

    feed.close_connection()

# sl_price = sl_price + step * math.floor(math.exp(pp_change*100 * max_pp_change*100))
option_type = 'CE'
strike = 54100
while True:
    analysis(strike,option_type)
    if df.loc[len(df.index)-1,'P-L'] <= 0:
        if option_type == 'CE':
            option_type = 'PE'
            strike = 54200
        else:
            option_type = 'CE'
            strike = 54100
df_opt
