import pandas as pd
import numpy as np
import re
from values_true import breweryid_city,breweryid_state
f = pd.read_csv('C:\\Users\\23500\\Desktop\\sapde数据\\sapde数据\\beers\\dirty.csv')
df = pd.DataFrame(f)
df = df.replace('', np.NaN)
for i in range(0, len(df)):
    abv=str(df.loc[i,'abv'])
    brewery_id=df.loc[i,'brewery_id']
    abv=abv.replace('%','')
    df.loc[i,'abv']=abv
    if df.loc[i,'abv']=='nan':
        df.loc[i,'abv']='0.05'
    if breweryid_city.__contains__(str(brewery_id)):
        df.loc[i,'city']=breweryid_city.get(str(brewery_id))
    if breweryid_state.__contains__(str(brewery_id)):
        df.loc[i,'state']=breweryid_state.get(str(brewery_id))
print(df)