import pandas as pd
import datetime as datetime
import struct
import ast

df = pd.read_csv("temp_test_data_2.csv")

temp = df.loc[3,'msg']

len(ast.literal_eval(temp))
struct.unpack("<BHBI",ast.literal_eval(temp)[0:8])
