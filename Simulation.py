# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
import pandas as pd
import numpy as np
import math

step = 0.05
I = 10000
lot_size = 50



def calculate_price(price,percentage):
    return step*(math.floor((1+percentage)*price/step)+1)

def calculate_qty(I,price):
    return lot_size * math.floor(I/(price*lot_size))


start = time.time()
test_d = pd.DataFrame({"Test Number":[],'Obs Num':[],'FUNDS':[],'Invested':[],'BUY_PRICE':[],"QTY":[],'LTP':[],"PP":[],"SLP":[],"TPP":[],"SL_PRICE":[],"TRIGGER_PRICE":[],'TP_PRICE':[],"SELL_VALUE":[],"P/L":[]})
for test in range(0,20*2):
    ltp = np.random.randint(10,100)
    r = np.random.rand()
    if r>=0.05:
        ltp = ltp + step * math.floor(r/step)
    else:
        ltp = ltp - step * math.floor(r/step)
    if test == 0:
        fund = I
    else:
        fund = test_d.loc[len(test_d.index)-1,'FUNDS'].item() + test_d.loc[len(test_d.index)-1,'P/L'].item()
    qty = calculate_qty(fund,ltp)
    Invest = qty*ltp    
    sl_price = calculate_price(ltp, -0.05)
    tp_price = calculate_price(ltp, 0.1)
    slp = (sl_price - ltp)/ltp
    tpp = (tp_price - ltp)/ltp
    df = pd.DataFrame({'INVESTED':[Invest],'BUY_PRICE':[ltp],"QTY":[qty],'LTP':[ltp],"PP":[0],"SLP":[slp],"TPP":[tpp],"SL_PRICE":[sl_price],"TRIGGER_PRICE":[sl_price+step],'TP_PRICE':[tp_price],"SELL_VALUE":[np.nan],'P/L':[np.nan]})
    for i in range(0,25):
        temp = np.random.rand()
        b_price = df.loc[i,'BUY_PRICE']
        ltp = df.loc[i,'LTP']
        pp = df.loc[i,'PP']
        slp = df.loc[i,'SLP']
        tpp = df.loc[i,'TPP']
        sl_price = df.loc[i,'SL_PRICE']
        tp_price = df.loc[i,'TP_PRICE']
        qty = df.loc[i,'QTY']
        trigger_price = df.loc[i,"TRIGGER_PRICE"]
        if temp < 0.5:
            ltp = ltp - step*math.floor((temp/0.05))
        else:
            ltp = ltp + step*math.floor((temp/0.05))
        pp = (ltp - b_price)/df.loc[i,'LTP']
        if tpp <= pp:
            tpp = pp + 0.05
            tp_price = calculate_price(b_price, tpp)
        if ltp <= trigger_price:
            ltp = sl_price
            slp = (sl_price - b_price)/b_price
            pp = slp
            df.loc[len(df.index)] = [Invest,b_price,qty,ltp,pp,pp,tpp,sl_price,trigger_price,tp_price,sl_price*qty - 40,sl_price*qty - b_price*qty - 40]
            # print(df)
            break
        slp = max(slp,(3*pp - tpp)/2)
        sl_price = calculate_price(b_price, slp)
        trigger_price = sl_price + step
        slp = (sl_price - b_price)/b_price
        if i==24:
            pp = slp
            sl_price = ltp
            df.loc[len(df.index)] = [Invest,b_price,qty,ltp,pp,pp,tpp,sl_price,trigger_price,tp_price,sl_price*qty - 40,sl_price*qty - b_price*qty - 40]
        else:
            df.loc[len(df.index)] = [Invest,b_price,qty,ltp,pp,pp,tpp,sl_price,trigger_price,tp_price,np.nan,np.nan]
    t = [test]
    t.append(i+1)
    t.append(fund)
    t.extend(list(df.loc[i+1,:]))
    test_d.loc[len(test_d.index)] = t  
    print(f'Test Number :{test+1} Completed')
    # print(df)
test_d
print("\n")

print(f"NUMBER OF TIMES PROFIT HAPPENED = {test_d.loc[test_d['P/L']>0,:].shape[0]}")
r = list(test_d.loc[test_d['PP']>0,'PP'])
print(f"Average Profit Per Trade = {sum(r)/len(r)}")
print("\n")
print(test_d.loc[test_d['PP']>0,:])

print("\n")

print(f"NUMBER OF TIMES LOSS HAPPENED = {test_d.loc[test_d['PP']<0,:].shape[0]}")
r = list(test_d.loc[test_d['PP']<0,'PP'])
print(f"Average Loss Per Trade = {sum(r)/len(r)}")
print("\n")
print(test_d.loc[test_d['PP']<0,:])

print(f"\nThe Entire Time Taken = {time.time()-start}")

test_d.loc[len(test_d.index)-1,'FUNDS'].item()/(100000)
