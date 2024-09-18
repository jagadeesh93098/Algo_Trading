import pandas as pd

df = pd.read_csv('Dhan_Works/security.csv',low_memory = False)

df.columns


df.loc[(df['SEM_INSTRUMENT_NAME'] == 'FUTIDX') & (df['SEM_TRADING_SYMBOL'].str.startswith('NIFTY')) & (df['SEM_CUSTOM_SYMBOL'].str.contains('SEP')),:]
