import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('temp_graph_data.xlsx')

temp = list(df.columns)

temp

for i in range(1,df.shape[1]):
    locals()[temp[i]] = list(df[temp[i]])
    if i == 1:
        plt.scatter(df.index,locals()[temp[i]],s=1,c='black')
    elif i <=6:
        plt.scatter(df.index,locals()[temp[i]],s=1,c='red',marker=".")
    else:
        plt.scatter(df.index,locals()[temp[i]],s=1,c='blue',marker=".")

plt.show()