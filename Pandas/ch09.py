# -*- coding: utf-8 -*-
"""
Created on Fri Jun 05 11:42:44 2015

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
np.set_printoptions(precision=4)

df = DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                'key2' : ['one', 'two', 'one', 'two', 'one'],
                'data1' : np.random.randn(5),
                'data2' : np.random.randn(5)})
df

grouped = df['data1'].groupby(df['key1'])
grouped
grouped.mean()

means = df['data1'].groupby([df['key1'], df['key2']]).mean()
means
means.unstack()

states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])
df['data1'].groupby([states, years]).mean() #you can use any array with suitable length as group key

df.groupby(['key1', 'key2']).size() #use column name to group

# Iterating over groups-------------------------------
for name, group in df.groupby('key1'):
    print(name)
    print(group)

for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    print(group)

pieces = dict(list(df.groupby('key1'))) #get a dict of DataFrames
pieces['b']

# Grouping with dicts and Series--------
people = DataFrame(np.random.randn(5, 5),
                   columns=['a', 'b', 'c', 'd', 'e'],
                   index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.ix[2:3, ['b', 'c']] = np.nan # Add a few NA values
mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
           'd': 'blue', 'e': 'red', 'f' : 'orange'}

by_column = people.groupby(mapping, axis=1) #can choose group axis
by_column.sum()

map_series = Series(mapping)
people.groupby(map_series, axis=1).count()

# Grouping with functions------------------
people.groupby(len).sum()
key_list = ['one', 'one', 'one', 'two', 'two']
people.groupby([len, key_list]).min()

# Grouping by index levels--------------
columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],
                                    [1, 3, 5, 1, 3]], names=['cty', 'tenor'])
hier_df = DataFrame(np.random.randn(4, 5), columns=columns)
hier_df
hier_df.groupby(level='cty', axis=1).count()

# Data aggregation============================================
grouped = df.groupby('key1')
grouped['data1'].quantile(0.9)

def peak_to_peak(arr):
    return arr.max() - arr.min()

grouped.agg(peak_to_peak)
grouped.describe()

#---------------------------------------------------------
tips = pd.read_csv('tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']

grouped = tips.groupby(['sex', 'smoker'])
grouped_pct = grouped['tip_pct']

grouped_pct.agg('mean') #grouped_pct.mean()
grouped_pct.agg(['mean', 'std', peak_to_peak])  #diff funtions on same column
grouped_pct.agg([('foo', 'mean'), ('bar', np.std)]) #you can name the column to something other than the function name

#apply funtions to diff columns
functions = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(functions)
result
result['tip_pct']
#name the column
ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
grouped['tip_pct', 'total_bill'].agg(ftuples)

#apply diff funtions to diff columns
grouped.agg({'tip_pct' : ['min', 'max', 'mean', 'std'],
             'size' : ['sum', peak_to_peak]})

# Group-wise operations and transformations
people.groupby(key).transform(np.mean)  #mean return a scale value

key = ['one', 'two', 'one', 'two', 'one']
def demean(arr):    #demean return an array with the same length as input
    return arr - arr.mean()

people.groupby(key).transform(np.mean)  #mean return a scale value, sp boardcast it in the group
demeaned = people.groupby(key).transform(demean)    #apply funtion based on group
demeaned

#Apply: General split-apply-combine
def top(df, n=5, column='tip_pct'):
    return df.sort_index(by=column)[-n:]

top(tips, n=6)
tips.groupby('smoker').apply(top)
tips.groupby('smoker', group_keys=False).apply(top)

# Quantile and bucket analysis
frame = DataFrame({'data1': np.random.randn(1000), 'data2': np.random.randn(1000)})
factor = pd.cut(frame.data1, 4)
factor[:10]

def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}

grouped = frame['data2'].groupby(factor)
grouped.apply(get_stats).unstack()


# Pivot tables and Cross-tabulation===============================
tips.pivot_table(index=['sex', 'smoker'])   #default is mean()
tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'],
                 columns='smoker')
tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'],
                 columns='smoker')
tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'],
                 columns='smoker', margins=True)
tips.pivot_table('tip_pct', index=['sex', 'smoker'], columns='day',
                 aggfunc=len, margins=True)

# Cross-tabulations: crosstab
from StringIO import StringIO
data = """\
Sample    Gender    Handedness
1    Female    Right-handed
2    Male    Left-handed
3    Female    Right-handed
4    Male    Right-handed
5    Male    Left-handed
6    Male    Right-handed
7    Female    Right-handed
8    Female    Left-handed
9    Male    Right-handed
10    Female    Right-handed"""
data = pd.read_table(StringIO(data), sep='\s+')

pd.crosstab(data.Gender, data.Handedness, margins=True)

pd.crosstab([tips.time, tips.day], tips.smoker, margins=True)
