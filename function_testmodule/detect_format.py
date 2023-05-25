import pandas as pd
import numpy as np
abv_fault=[] #定义abv格式错误列表
f=pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df=df.replace('',np.NaN)
ex_df=df.dropna(subset=['abv']) #将abv列为空的行删除
fina_df=ex_df[ex_df['abv'].str.contains('%')] #寻找abv列中元素含有%元组

for i in range(0,len(fina_df)):
    list1=fina_df.iloc[i]
    index = list1['index']
    id=list1['id']
    beer_name=list1['beer_name']
    style=list1['style']
    ounces=list1['ounces']
    abv=list1['abv']
    brewery_id=list1['brewery_id']
    brewery_name=list1['brewery_name']
    city=list1['city']
    state = list1['state']
    combine_dict1={
        'index': index,
        'id':id,
        'beer_name':beer_name,
        'style':style,
        'ounces':ounces,
        'abv':abv,
        'brewery_id':brewery_id,
        'brewery_name':brewery_name,
        'city':city,
        'state':state
    }
    abv_fault.append(combine_dict1)



