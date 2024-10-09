import pandas as pd
import datetime as datetime
import struct
import ast

df = pd.read_csv("temp_test_data_2.csv")

temp = df.loc[2,'msg']

len(ast.literal_eval(temp))
list(struct.unpack("<B",ast.literal_eval(temp)[0:1]))
