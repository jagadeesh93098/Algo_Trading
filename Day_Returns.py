import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def my_data_day(s):
    e_d=datetime.today()-timedelta(days=1)
    
