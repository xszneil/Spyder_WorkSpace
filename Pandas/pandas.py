# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:51:50 2015

@author: ZhuJiaqi
"""

import pandas as pd
sd

s = pd.Series([1,3,5,np.nan,6,8])
dates = pd.date_range('20130101', periods=6)

#create dataframe
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

df2 = pd.DataFrame({ 'A' : 1.,
'B' : pd.Timestamp('20130102'),
'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
'D' : np.array([3] * 4,dtype='int32'),
'E' : pd.Categorical(["test","train","test","train"]),
'F' : 'foo' })

df2.dtypes

#read dataframe
df.head()
df.tail(n=3)
df.index
df.columns
df.values
df.describe()

df.T

#sorting by an axis
df.sort_index(axis=1, ascending=False)
#sorting by values
df.sort(columns='B')

#selection
df['A'] #df.A
df[0:3]
df['20130102':'20130104']
#select by label
df.loc[dates[0]]
df.loc[:,['A','B']]
df.loc['20130102':'20130104',['A','B']]
df.loc['20130102',['A','B']]
df.loc[dates[0],'A']
df.at[dates[0],'A']
#select by position
df.iloc[3]
df.iloc[3:5,0:2]
df.iloc[[1,2,4],[0,2]]
df.iloc[1:3,:]
df.iloc[:,1:3]
df.iloc[1,1]
df.iat[1,1]

#boolean indexing
df[df.A > 0]
df[df > 0]
df2 = df.copy()
df2['E']=['one', 'one','two','three','four','three']
df2
df2[df2['E'].isin(['two','four'])]

#setting
s1 = pd.Series([1,2,3,4,5,6],index=pd.date_range('20130102',periods=6))
df['F'] = s1
df.at[dates[0],'A'] = 0
df.loc[:,'D'] = np.array([5] * len(df))

df2 = df.copy()
df2[df2 > 0] = -df2

#missing data
df1 = df.reindex(index=dates[0:4],columns=list(df.columns) + ['E'])
df1.loc[dates[0]:dates[1],'E'] = 1
df1.dropna(how='any')
df1.fillna(value=5)
pd.isnull(df1)

#Operations


#apply
df.apply(np.cumsum)
df.apply(np.cumsum, axis=1)
df.apply(lambda x: x.max()-x.min())

