import pandas as pd

url = 'https://images.dhan.co/api-data/api-scrip-master.csv'

exch = "NSE"
instrument = "OPTIDX"
underlying = "MIDCPNIFTY"

df = pd.read_csv(url,low_memory = False)

list_expiry = list(df.loc[(df['SEM_EXM_EXCH_ID'] == exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)),'SEM_EXPIRY_DATE'].unique())
list_expiry.sort(reverse = False)
expiry_date = list_expiry[0]

df_opt = df.loc[(df['SEM_EXM_EXCH_ID']==exch) & (df['SEM_INSTRUMENT_NAME'] == instrument) & (df['SEM_TRADING_SYMBOL'].str.startswith(underlying)) & (df['SEM_EXPIRY_DATE']==expiry_date),:].copy()

df_opt.reset_index(inplace = True,drop = True)

df_opt.to_csv("today_opt_chain.csv",index=False)


df.loc[(df['SEM_EXM_EXCH_ID']==exch) & (df['SEM_INSTRUMENT_NAME']=='INDEX') & (df['SEM_TRADING_SYMBOL'] == 'MIDCPNIFTY'),:]