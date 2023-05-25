import pandas as pd
import numpy as np
from function_testmodule.values_true import breweryid_city
from modelmodule.models import DataModel
city_fault = []  # 定义city错误列表
f = pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')

df = pd.DataFrame(f)
df = df.replace('', np.NaN)
for i in range(0, len(df)):
    list1 = df.iloc[i]
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
    if breweryid_city.__contains__(str(brewery_id)) and city != breweryid_city[str(brewery_id)]:
        combine_dict1 = {
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
        city_fault.append(combine_dict1)
for j in range(0, len(city_fault)):
    print(city_fault[j])
