import pandas as pd
import numpy as np

abv_isnull_list = []  # abv缺失列表
state_isnull_list = []  # state缺失列表
f = pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
ex_df = df.loc[df.isnull().any(axis=1)]  # 将表中含有NaN值筛选出
abv_lost = ex_df[ex_df['abv'].isin([np.NAN])]  # 分出abv列是NaN
state_lost = ex_df[ex_df['state'].isin([np.NAN])]  # 分出state列是NaN

for i in range(0, len(abv_lost)):
    list1 = abv_lost.iloc[i]
    index = list1['index']
    id = list1['id']
    beer_name = list1['beer_name']
    style = list1['style']
    ounces = list1['ounces']
    abv = list1['abv']
    brewery_id = list1['brewery_id']
    brewery_name = list1['brewery_name']
    city = list1['city']
    state = list1['state']
    combine_dict1 = {  # 将abv缺失的行组成字典
        'index': index,
        'id': id,
        'beer_name': beer_name,
        'style': style,
        'ounces': ounces,
        'abv': abv,
        'brewery_id': brewery_id,
        'brewery_name': brewery_name,
        'city': city,
        'state': state
    }
    abv_isnull_list.append(combine_dict1)

for j in range(0, len(state_lost)):
    list2 = state_lost.iloc[j]
    index = list2['index']
    id = list2['id']
    beer_name = list2['beer_name']
    style = list2['style']
    ounces = list2['ounces']
    abv = list2['abv']
    brewery_id = list2['brewery_id']
    brewery_name = list2['brewery_name']
    city = list2['city']
    state = list2['state']
    combine_dict2 = {  # 将state缺失的行组成字典
        'index': index,
        'id': id,
        'beer_name': beer_name,
        'style': style,
        'ounces': ounces,
        'abv': abv,
        'brewery_id': brewery_id,
        'brewery_name': brewery_name,
        'city': city,
        'state': state
    }
    state_isnull_list.append(combine_dict2)
