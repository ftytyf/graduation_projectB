import pandas as pd
import numpy as np
import re
f=pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df=df.replace('',np.NaN)
ex1_df=df.dropna(subset=['ounces']) #将ounces列为空的行删除
for j in range(0,len(ex1_df)):
    list2=ex1_df.iloc[j]
    ounces = list2['ounces']
    list2['ounces']= re.sub("([a-zA-Z])", "", ounces)
    ex1_df.iloc[j]=list2