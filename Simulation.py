# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
# import matp1lotlib.pyplot as plt
import math

def calculate_price(price,percentage):
    return step*(math.floor((1+percentage)*price/step)+1)

step = 0.05

test_d = pd.DataFrame({"Test Number":[],'Obs Num':[],'BUY_PRICE':[],'LTP':[],"PP":[],"SLP":[],"TPP":[],"SL_PRICE":[],'TP_PRICE':[]})
for test in range(0,1000):
    ltp = np.random.randint(10,100)
    r = np.random.rand()
    if r>=0.05:
        ltp = ltp + step * math.floor(r/step)
    else:
        ltp = ltp - step * math.floor(r/step)

    sl_price = calculate_price(ltp, -0.05)
    tp_price = calculate_price(ltp, 0.1)
    slp = (sl_price - ltp)/ltp
    tpp = (tp_price - ltp)/ltp
    df = pd.DataFrame({'BUY_PRICE':[ltp],'LTP':[ltp],"PP":[0],"SLP":[slp],"TPP":[tpp],"SL_PRICE":[sl_price],'TP_PRICE':[tp_price]})

    for i in range(0,50):
        temp = np.random.rand()
        b_price = df.loc[i,'BUY_PRICE']
        ltp = df.loc[i,'LTP']
        pp = df.loc[i,'PP']
        slp = df.loc[i,'SLP']
        tpp = df.loc[i,'TPP']
        sl_price = df.loc[i,'SL_PRICE']
        tp_price = df.loc[i,'TP_PRICE']
        if temp < 0.5:
            ltp = ltp - step*math.floor((temp/0.05))
        else:
            ltp = ltp + step*math.floor((temp/0.05))
        pp = (ltp - b_price)/df.loc[i,'LTP']
        if tpp <= pp:
            tpp = pp + 0.05
            tp_price = calculate_price(b_price, tpp)
        if ltp <= sl_price:
            pp = slp
            df.loc[len(df.index)] = [b_price,ltp,pp,pp,tpp,ltp,tp_price]
            # print(df)
            break
        slp = max(slp,(3*pp - tpp)/2)
        sl_price = calculate_price(b_price, slp)
        slp = (sl_price - b_price)/sl_price
        if i==59:
            slp = pp
            sl_price = ltp
        df.loc[len(df.index)] = [b_price,ltp,pp,slp,tpp,sl_price,tp_price]
    t = [test]
    t.append(i)
    t.extend(list(df.loc[i+1,:]))
    test_d.loc[len(test_d.index)] = t  
    # print(f'Test Number :{test+1} Completed')
    # print(df)
test_d
print("\n")

print(f"NUMBER OF TIMES PROFIT HAPPENED = {test_d.loc[test_d['PP']>0,:].shape[0]}")
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
