import pandas as pd
import datetime

today = datetime.datetime.today()

file_name = f"test_order_{datetime.datetime.strftime(today,'%Y_%m_%d')}.csv"
file_name
df = pd.read_csv(file_name)


print(f"\nTotal Profit Today = {df['P/L'].sum()}\n")
