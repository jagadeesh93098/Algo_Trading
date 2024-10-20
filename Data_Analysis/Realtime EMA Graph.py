import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

file_name = 'temp_graph_data.csv'

def animate(i):
    global profit
    try :
        df = pd.read_csv(file_name)
        ltp = list(df['LTP'])
        for i in range(100,1100,100):
            locals()[f"ema_{i}"] = list(df[f"EMA_{i}"])
        
        X = [i+1 for i in range(0,len(ltp))]
        
        plt.scatter(X,ltp,c='black',marker='.',s=1)
        for i in range(100,1100,100):
            if i <= 500:
                plt.scatter(X,locals()[f"ema_{i}"],c='red',marker='.',s=1)
            else:
                plt.scatter(X,locals()[f"ema_{i}"],c='blue',marker='.',s=1)
    except:
        pass
    

animation.FuncAnimation(plt.gcf(),animate,interval = 5,save_count=1)
plt.show()