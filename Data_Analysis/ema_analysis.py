import matplotlib.pyplot as plt
import pandas as pd
import os
import time

file_path = "data/20241018/MIDCPNIFTY/index_MIDCPNIFTY.xlsx"

graph_data = {"SNo":[],"LTP":[]}

n = [(i+1)*500 for i in range(0,10)]
k = [2/(i+1) for i in n]

for i in n:
    graph_data[f'EMA_{i}'] = []
graph_data


d_plt = pd.DataFrame(graph_data)

df = pd.read_excel(file_path)


for i in range(0,df.shape[0]):
    ltp = df.loc[i,'last_price'].item()
    if i == 0:
        for day in n:
            locals()[f"ema_{day}"] = ltp
    else:
        for day in n:
            locals()[f"ema_{day}"] = k[n.index(day)] * ltp + d_plt.loc[i-1,f'EMA_{day}'].item() * (1 - k[n.index(day)])
    temp = [i,ltp]
    for day in n:
        temp.append(locals()[f"ema_{day}"])
    d_plt.loc[len(d_plt.index)] = temp
    # print(d_plt)
    print(f"{i+1} Data Points Collected",end = "\r")

d_plt.to_excel('temp_graph_data.xlsx',index=False)