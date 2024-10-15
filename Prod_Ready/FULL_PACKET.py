import pandas as pd
import ast
import csv
import struct
import datetime
import os

field_names = ['SECURITY_ID', 'LTP', 'LTQ', 'LTT', 'ATP', 'VOLUME', 'TOTAL_SELL_QTY', 'TOTAL_BUY_QTY', 'OI', 'HIGHEST_OI', 'LOWEST_OI', 'DAY_OPEN_VALUE', 'DAY_CLOSE_VALUE', 'DAY_HIGH_VALUE', 'DAY_LOW_VALUE', 'DEPTH_1', 'DEPTH_2', 'DEPTH_3', 'DEPTH_4', 'DEPTH_5']

def process_msg(msg):
    rep = struct.unpack("<BHBIfHIfIIIfffffff",msg[0:62])
    full_depth = []
    for i in range(0,5):
        s = 62 + i*20
        e = 62 + (i+1)*20
        depth = struct.unpack('<IIHHff',msg[s:e])
        # print(depth)
        k = {
            'BID_QTY' : depth[0],
            "ASK_QTY" : depth[1],
            "N_BID_ORDERS" : depth[2],
            "N_ASK_ORDERS" : depth[3],
            "BID_PRICE" : round(depth[4],2),
            "ASK_PRICE" : round(depth[5],2)
        }
        full_depth.append(k)

    # for i in range(0,5):
    #     print(f"Depth_{i+1} = {locals()[depth_{i+1}]}")

    final = {
        'SECURITY_ID':rep[3],
        'LTP':round(rep[4],2),
        'LTQ':rep[5],
        'LTT':rep[6],
        'ATP':rep[7],
        'VOLUME':rep[8],
        'TOTAL_SELL_QTY':rep[9],
        'TOTAL_BUY_QTY':rep[10],
        'OI':rep[11],
        'HIGHEST_OI':rep[12],
        'LOWEST_OI':rep[13],
        'DAY_OPEN_VALUE':rep[14],
        'DAY_CLOSE_VALUE':rep[15],
        'DAY_HIGH_VALUE':rep[16],
        'DAY_LOW_VALUE':rep[17],
        'DEPTH_1':full_depth[0],
        'DEPTH_2':full_depth[1],
        'DEPTH_3':full_depth[2],
        "DEPTH_4":full_depth[3],
        "DEPTH_5":full_depth[4]
    }
    return final
