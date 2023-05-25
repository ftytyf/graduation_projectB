import pandas as pd
import numpy as np

f = pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
jaccardIndex_dict = {}  # 存储杰卡德系数的列表
union = 16  # 两行属性除去索引和缺失的属性（并集）
ex_df = df.loc[df.isnull().any(axis=1)]  # 将表中含有NaN值筛选出
list0 = ex_df.iloc[1]
for i in range(0, len(df)):
    intersection = 1
    list1 = df.iloc[i]
    if list0['id'] == list1['id']:
        intersection = intersection + 1
    if list0['beer_name'] == list1['beer_name']:
        intersection = intersection + 1
    if list0['style'] == list1['style']:
        intersection = intersection + 1
    if list0['ounces'] == list1['ounces']:
        intersection = intersection + 1
    if list0['brewery_id'] == list1['brewery_id']:
        intersection = intersection + 1
    if list0['brewery_name'] == list1['brewery_name']:
        intersection = intersection + 1
    if list0['city'] == list1['city']:
        intersection = intersection + 1
    if list0['state'] == list1['state']:
        intersection = intersection + 1
    if list0['index'] == list1['index']:
        continue
    else:
        jaccardIndex = intersection / union
    index = list1['index']
    jaccardIndex_dict[str(index)] = jaccardIndex

maxDistance = 0
firstIndex = 0
print(jaccardIndex_dict)
for key, value in jaccardIndex_dict.items():
    if maxDistance < value:
        maxDistance = value
        firstIndex = key
jaccardIndex_dict.pop(firstIndex)
maxDistance = 0
secondIndex = 0
if firstIndex == 0:
    secondIndex = 1
for key, value in jaccardIndex_dict.items():
    if maxDistance < value:
        maxDistance = value
        secondIndex = key
jaccardIndex_dict.pop(secondIndex)
maxDistance = 0
thirdIndex = 0
if secondIndex == 0 or secondIndex == 1:
    thirdIndex = 2
for key, value in jaccardIndex_dict.items():
    if maxDistance < value:
        maxDistance = value
        thirdIndex = key

print(firstIndex, secondIndex, thirdIndex)
print(list0)
