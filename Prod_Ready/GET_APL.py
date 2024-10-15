import pandas as pd
import math
import sys

def get_apl(file_name):
    df = pd.read_csv(file_name)

    df['STT'] = df['SELL_PRICE'] * df['QTY'] * 0.1/100
    # df['STT'] = df['STT'].round(2)

    df['EXCH_TRANSACTION_CHARGES'] = (df['BUY_PRICE'] + df['SELL_PRICE']) * df['QTY'] * 0.03503/100
    # df['EXCH_TRANSACTION_CHARGES'] = df['EXCH_TRANSACTION_CHARGES'].round(2)

    df['SEBI_CHARGES'] = (df['BUY_PRICE']+df['SELL_PRICE'])*df['QTY']*10/100000000
    # df['SEBI_CHARGES'] = df['SEBI_CHARGES'].round(2)

    df['GST'] = 0.18 * (df['EXCH_TRANSACTION_CHARGES'] + df['SEBI_CHARGES'] + df['BROKERAGE'])
    # df['GST'] = df['GST'].round(2)

    df['STAMP_DUTY'] = df['BUY_PRICE'] * df['QTY'] * 0.003/100
    # df['STAMP_DUTY'] = df ['STAMP_DUTY'].round(2)

    df['TOTAL_CHARGES'] = df['STT'] + df['EXCH_TRANSACTION_CHARGES'] + df['SEBI_CHARGES'] + df['STAMP_DUTY'] + df['GST'] + df['BROKERAGE']
    df['TOTAL_CHARGES'] = df['TOTAL_CHARGES'].round(2)

    df['APL'] = df['P-L'] + df['BROKERAGE'] - df['TOTAL_CHARGES']

    return df,float(df['APL'].sum())

# file_name = sys.argv[1]
# df,p = get_apl(file_name=file_name)
# print('============================================')
# print("Order Book")
# print('============================================')
# print(df)
# print("\n")
# print(f"Final Profit = {p}")
