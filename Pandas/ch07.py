# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 10:37:46 2015

@author: jzhu0922
"""

from __future__ import division
from numpy.random import randn
import numpy as np
import os
import matplotlib.pyplot as plt
np.random.seed(12345)
plt.rc('figure', figsize=(10, 6))
from pandas import Series, DataFrame
import pandas as pd
np.set_printoptions(precision=4, threshold=500)
pd.options.display.max_rows = 100

# Database-style DataFrame merges, just like join in database==================
df3 = DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
df4 = DataFrame({'rkey': ['a', 'b', 'd'],
                 'data2': range(3)})
pd.merge(df3, df4, left_on='lkey', right_on='rkey') #default is merge on the same column
pd.merge(df3, df4, left_on='lkey', right_on='rkey', how='left')

#merge on multiple key
left = DataFrame({'key1': ['foo', 'foo', 'bar'],
                  'key2': ['one', 'two', 'one'],
                  'lval': [1, 2, 3]})
right = DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                   'key2': ['one', 'one', 'one', 'two'],
                   'rval': [4, 5, 6, 7]})
pd.merge(left, right, on=['key1', 'key2'], how='outer')

# Merging on index
left1 = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'],
                  'value': range(6)})
right1 = DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
pd.merge(left1, right1, left_on='key', right_index=True)

# Concatenating along an axis==================================================
s1 = Series([0, 1], index=['a', 'b'])
s2 = Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = Series([5, 6], index=['f', 'g'])
pd.concat([s1, s2, s3]) #no overlap, default on axis = 0, union index
pd.concat([s1, s2, s3], axis=1) #on axis = 1 return a DataFrame, union index

s4 = pd.concat([s1 * 5, s3])
pd.concat([s1, s4], axis=1)
pd.concat([s1, s4], axis=1, join='inner')
pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']])

#say after join, you still need to know where the data come from
result = pd.concat([s1, s1, s3], keys=['one', 'two', 'three'])  #multi-index

df1 = DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'],
                columns=['one', 'two'])
df2 = DataFrame(5 + np.arange(4).reshape(2, 2), index=['a', 'c'],
                columns=['three', 'four'])
pd.concat([df1, df2], axis=1, keys=['level1', 'level2'])

#ignore index
df1 = DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df2 = DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
pd.concat([df1, df2])
pd.concat([df1, df2], ignore_index=True)

# Combining data with overlap==================================================
a = Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b = Series(np.arange(len(a), dtype=np.float64),
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b[-1] = np.nan
b[:-2].combine_first(a[2:])
#combine first align and try to fill NAN from second obj to first obj
df1 = DataFrame({'a': [1., np.nan, 5., np.nan],
                 'b': [np.nan, 2., np.nan, 6.],
                 'c': range(2, 18, 4)})
df2 = DataFrame({'a': [5., 4., np.nan, 3., 7.],
                 'b': [np.nan, 3., 4., 6., 8.]})
df1.combine_first(df2)

# Reshaping with hierarchical indexing=========================================
data = DataFrame(np.arange(6).reshape((2, 3)),
                 index=pd.Index(['Ohio', 'Colorado'], name='state'),
                 columns=pd.Index(['one', 'two', 'three'], name='number'))
result = data.stack()    #stack a DataFrame to a Muliti-index Series, can inverse
result.unstack(0)
result.unstack('state')

# Pivoting "long" to "wide" format
data = pd.read_csv('macrodata.csv')
periods = pd.PeriodIndex(year=data.year, quarter=data.quarter, name='date')
data = DataFrame(data.to_records(),columns=pd.Index(['realgdp', 'infl', 'unemp'], name='item'),index=periods.to_timestamp('D', 'end'))

ldata = data.stack().reset_index().rename(columns={0: 'value'})
wdata = ldata.pivot('date', 'item', 'value')

# Removing duplicates===============================
data = DataFrame({'k1': ['one'] * 3 + ['two'] * 4,'k2': [1, 1, 2, 3, 3, 4, 4]})

data.duplicated()
data.drop_duplicates()
data['v1'] = range(7)
data.drop_duplicates(['k1'])
data.drop_duplicates(['k1', 'k2'], take_last=True)

# Replacing values-------------------------------
data = Series([1., -999., 2., -999., -1000., 3.])
data.replace(-999, np.nan)
data.replace([-999, -1000], np.nan)
data.replace([-999, -1000], [np.nan, 0])
data.replace({-999: np.nan, -1000: 0})

# Discretization and binning
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']

cats = pd.cut(ages, bins, labels=group_names)   #labels can be ommit
cats
cats.codes
cats.categories
pd.value_counts(cats)

data = np.random.rand(20)
pd.cut(data, 4, precision=2)    #input the number of the bins

data = np.random.randn(1000) # Normally distributed
cats = pd.qcut(data, 4) # Cut into quartiles
cats
pd.value_counts(cats)
pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])

# Permutation and random sampling
df = DataFrame(np.arange(5 * 4).reshape((5, 4)))

df.take(np.random.permutation(5))
df.take(np.random.permutation(len(df))[:3])

# Computing indicator / dummy variables
df = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                'data1': range(6)})
pd.get_dummies(df['key'])

# String manipulation==========================================================
val = 'a,b,  guido'
val.split(',')
pieces = [x.strip() for x in val.split(',')]
pieces
'::'.join(pieces)
'guido' in val
val.index(',')
val.find(':')   #return -1 when not find
val.index(':')
val.count(',')
val.replace(',', '::')
val.replace(',', '')

#regular expression
import re
text = "foo    bar\t baz  \tqux"
re.split('\s+', text)

regex = re.compile('\s+')
regex.split(text)
regex.findall(text)

text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex = re.compile(pattern, flags=re.IGNORECASE)
regex.findall(text)

pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)
regex.findall(text)

# Vectorized string functions in pandas
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = Series(data)
#str funtions can skip NA values
data.str.contains('gmail')
data.str.findall(pattern, flags=re.IGNORECASE)
data.str[:5]

matches = data.str.match(pattern, flags=re.IGNORECASE)
matches
matches.str.get(1)
matches.str[0]
















