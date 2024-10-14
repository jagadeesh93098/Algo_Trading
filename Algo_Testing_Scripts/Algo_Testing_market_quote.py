import pandas as pd
import math
import numpy as np
import datetime
import time
import subprocess
import GET_APL as GA

def to_epoch(a):
    dt = datetime.datetime.strptime(a,'%d/%m/%Y %H:%M:%S')
    return int(dt.timestamp())

call_desc = 'SENSEX_11_OCT_81500_CALL'
put_desc = 'SENSEX_11_OCT_81500_PUT'

df_put = pd.read_excel("data/20241011/SENSEX/SENSEX_11_OCT_81500_PUT.xlsx")
df_put.insert(1,'LTT',df_put['last_trade_time'].apply(to_epoch))
df_put
# df_put.drop_duplicates(subset=['last_price'],keep = 'last',inplace = True)
# df_put.reset_index(inplace = True,drop= True)
df_call = pd.read_excel("data/20241011/SENSEX/SENSEX_11_OCT_81500_CALL.xlsx")
df_call.insert(1,'LTT',df_call['last_trade_time'].apply(to_epoch))
df_call
# df_call.drop_duplicates(subset = ['last_price'],keep = 'last',inplace = True)
# df_call.reset_index(inplace = True, drop = True)


i_fund = 100000

lot_size = 10

max_quantity = 500

t0 = df_call.loc[0,'LTT']

step = 0.05
def calculate_qty(fund,ltp):
    global lot_size
    return lot_size * math.floor(fund/(ltp*lot_size))

def calculate_price(price,percent):
    return step * (math.floor(price*(1+percent)/step)-1)

df_final = pd.DataFrame({
    'FUND':[],
    "INSTRUMENT":[],
    "INVESTED":[],
    "BUY_PRICE":[],
    "BUY_TIME":[],
    "QTY":[],
    'ORDER_NUM':[],
    "SELL_PRICE":[],
    "SELL_TIME":[],
    "BROKERAGE":[],
    'P-L':[]
    })

file_name = 'temp_testing_algo_market_quote.csv'

def analysis(option_type,time_stamp):
    global df_call,df_trade,max_quantity,df_put,df_final,df_trade,file_name
    if option_type == 'call':
        i = df_call.loc[(df_call['LTT']>=time_stamp),:].index[0]
        ltp = df_call.loc[i,'last_price']
        option_desc = "SENSEX_11_OCT_81500_CALL"
    else:
        i = df_put.loc[(df_put['LTT']>=time_stamp),:].index[0]
        ltp = df_put.loc[i,'last_price']
        option_desc = "SENSEX_11_OCT_81500_PUT"
    if df_final.shape[0] == 0:
        fund = i_fund
    else:
        fund = df_final.loc[len(df_final.index)-1,'FUND'].item() + df_final.loc[len(df_final.index)-1,'P-L'].item()
    buy_price = ltp
    qty = calculate_qty(min(fund,200000),ltp)
    order_num = math.ceil(qty/max_quantity)
    brokerage = order_num * 40
    i_tpp = 0.1
    i_slp = -0.05
    tp_price = calculate_price(ltp,i_tpp)
    sl_price = calculate_price(ltp,i_slp)
    pp = 0
    slp = (sl_price - buy_price)/buy_price
    tpp = (tp_price - buy_price)/buy_price
    trigger = sl_price + step
    max_pp = 0
    buy_time = time_stamp
    df_trade = pd.DataFrame({
        'OPTION_DESC':[option_desc],
        'BUY_PRICE':[buy_price],
        'BUY_TIME':[buy_time],
        'QTY':[qty],
        'ORDER_NUM' : [order_num],
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
        'SELL_TIME':[np.nan],
        'BROKERAGE':[brokerage],
        'P-L':[np.nan]})
    exit = False
    while exit != True:
        time_stamp = time_stamp + 1
        ltp0 = ltp
        if option_type == 'call':
            i = df_call.loc[(df_call['LTT']>=time_stamp),:].index[0]
            ltp = df_call.loc[i,'last_price']
            option_desc = "SENSEX_11_OCT_81500_CALL"
        else:
            i = df_put.loc[(df_put['LTT']>=time_stamp),:].index[0]
            ltp = df_put.loc[i,'last_price']
            option_desc = "SENSEX_11_OCT_81500_PUT"
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
            pl = qty*(sl_price - buy_price) - brokerage
            # 40 Added considering the Brokering Charge.
            df_trade.loc[len(df_trade.index)] = [option_desc,buy_price,buy_time,qty,order_num,ltp,ltp_change,pp,max_pp,pp_change,slp,sl_price_risk,sl_pricemv,sl_price,trigger,tpp,tp_price,sell_price,time_stamp,brokerage,pl]
            df_final.loc[len(df_final.index)] = [fund,option_desc,buy_price*qty,buy_price,buy_time,qty,order_num,sell_price,time_stamp,brokerage,pl]
            print(df_trade)
            print("\n")
            print(df_final)
            df_final.to_csv(file_name)
            break
        sl_price0 = sl_price
        slp0 = slp
        if ltp_change < 0:
            sl_pricemv = min(sl_price0 + step * (1 + math.floor(math.exp((-ltp_change/abs(ltp_change))*400*pp_change))),ltp - 2*step)
        else:
            sl_pricemv = min(sl_price0 + step * (1 + math.floor(math.exp(200*(pp_change)))),ltp - 2*step)
        slp_risk = max(slp,(3*pp - tpp)/2)
        sl_price_risk = calculate_price(buy_price,slp_risk)
        sl_price = max(sl_pricemv,sl_price_risk,sl_price0)
        trigger = sl_price + step
        slp = (sl_price - buy_price)/buy_price
        df_trade.loc[len(df_trade.index)] = [
            option_desc,
            buy_price,
            buy_time,
            qty,
            order_num,
            ltp,
            ltp_change,
            pp,
            max_pp,
            pp_change,
            slp,
            sl_price_risk,
            sl_pricemv,
            sl_price,
            trigger,
            tpp,
            tp_price,
            np.nan,
            np.nan,
            brokerage,
            np.nan]
        print(df_trade)
        print("\n")
        # time.sleep(1)

option_type = "call"

while True:
    try:
        analysis(option_type,t0)
        df_temp,p = GA.get_apl("temp_testing_algo_market_quote.csv")
        print(f"Profit after Taxes = {p}")
        if p >= 100000:
            break
        if df_trade.loc[df_trade.shape[0]-1,'BUY_PRICE'] <= 15:
            break
        else:
            if df_trade.loc[len(df_trade.index)-1,'P-L'] <= 0:
                if option_type == 'call':
                    option_type = 'put'
                else:
                    option_type = 'call'
            t0 = df_final.loc[df_final.shape[0]-1,'SELL_TIME'] + 1
    except KeyboardInterrupt:
        break

