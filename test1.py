import pandas as pd
from dhanhq import marketfeed
import requests

df = pd.read_csv('Dhan_Works/security.csv',low_memory = False)

underlying_s_id = df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_INSTRUMENT_NAME'] == 'FUTCOM') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09')),'SEM_SMST_SECURITY_ID'].item()




df.loc[(df['SEM_EXM_EXCH_ID'] == 'MCX') & (df['SEM_INSTRUMENT_NAME'] == 'OPTFUT') & (df['SEM_TRADING_SYMBOL'].str.startswith('NATURALGAS')) & (df['SEM_EXPIRY_DATE'].str.startswith('2024-09-23')),:]
