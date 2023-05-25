import pandas as pd
import numpy as np


def jaccardDistance(x, y, w=None):
    inter = set(x).intersection(set(y))
    union = set(x).union(set(y))
    if w is None:
        sum_inter = len(inter)
        sum_union = len(union)
    else:
        sum_inter = sum([w[s] for s in inter])
        sum_union = sum([w[s] for s in union])
    d = 1 - sum_inter / (sum_union + 1e-9)
    return d


f = pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
ex_df = df.loc[df.isnull().any(axis=1)]  # 将表中含有NaN值筛选出
jaccardIndex_list = []  # 存储杰卡德系数的列表
x = ex_df.iloc[0]
for i in range(0, len(df)):
    y = df.iloc[i]
    if x['index'] == y['index']:
        continue
    else:
        jaccardindex = jaccardDistance(x, y)
    index=y['index']
    combine_dict={index:jaccardindex}
    jaccardIndex_list.append(combine_dict)
print(x)
print(jaccardIndex_list)