import pandas as pd
import os
import datetime


today = datetime.datetime.today()
today_date = datetime.datetime.strftime(today,'%Y%m%d')

os.chdir('data_websocket')
os.chdir(today_date)

for i in os.listdir():
    files = os.listdir(i)
    for file in files:
        if ".csv" in file:
            df = pd.read_csv(f"{i}/{file}")
            file_name = file.split(".csv")[0]
            df.to_excel(f"{i}/{file_name}.xlsx",index=False)
            print(f"{i}/{file_name}.xlsx Created.")
            os.remove(f"{i}/{file}")
