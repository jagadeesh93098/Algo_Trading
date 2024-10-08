import math
import pandas as pd

buy_price = 0.1
max_sl = -0.05
max_tp = 0.1
step = 0.05
n = math.floor((abs(max_sl))*buy_price/step)
real_sl = ((buy_price - n*step)/buy_price)-1
if n==0:
    print(f'Setting an SL is not Possible for Max_SL = {max_sl}')
else:
    print(f"If Buy_Price = {i} then Real SL% possible is {real_sl} with Real SL being {buy_price - n*step}")

df = pd.DataFrame({'BUY_PRICE':[],'SL':[],'REAL_SL_P':[]})

step = 0.05
for i in range(1,1001):
    buy_price = round(0+i*step,2)
    max_sl = -0.05
    max_tp = 0.1
    n = math.floor((abs(max_sl))*buy_price/step)
    real_sl = ((buy_price - n*step)/buy_price)-1
    if n==0:
        print(f'If Buy_Price = {buy_price}, Setting an SL is not Possible for Max_SL = {max_sl}')
    else:
        print(f"If Buy_Price = {buy_price} then Real SL% possible is {real_sl} with Real SL being {round(buy_price - n*step,2)}")
