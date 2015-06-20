from pandas import Series, DataFrame
import pandas as pd
import numpy as np
#Series========================================================================
obj = Series([4, 7, -5, 3])
obj.values
obj.index

obj2 = Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
obj2

#index by index or loc
obj2[0:3] #3 excluded
obj2[[1,3]]
obj2['a']
obj2['d'] = 6
obj2[['c', 'a', 'd']]
obj2['d':'a']   #a included
#boolean index
obj2[obj2 > 0]
'b' in obj2
'e' in obj2
#operations
obj2 * 2
np.exp(obj2)

#use dict to create Series
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = Series(sdata)
obj3

states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = Series(sdata, index=states)
obj4

pd.isnull(obj4)
pd.notnull(obj4)

#auto align
obj3 + obj4
obj3.add(obj4, fill_value = 0)

#DataFrame=====================================================================
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data) #can set column and index
frame2 = DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                   index=['one', 'two', 'three', 'four', 'five'])

#selecting by columns, return a Series, so you can index the Series again
frame['state']
frame[['year','state']]
frame[[0]]
frame[[0,2,1]]
#selecting by rows or index
frame2[0:2] #there is no syntax like frame2[0] for DataFrame
frame2.ix[2]
frame2.ix[2:4]
frame2.ix['three']
frame2.ix['one':'three']
#ix
data = DataFrame(np.arange(16).reshape((4, 4)),
                 index=['Ohio', 'Colorado', 'Utah', 'New York'],
                 columns=['one', 'two', 'three', 'four'])
data.ix['Colorado', ['two', 'three']]
data.ix[['Colorado', 'Utah'], [3, 0, 1]]
data.ix[data.three > 5, :3]


#operation
frame2['debt'] = np.arange(5.)  #if assign an array or list to a column, need match the length
val = Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2['debt'] = val#if assign an Series, it will auto align by index
frame2['eastern'] = frame2.state == 'Ohio' #assign to create a new column
del frame2['eastern']   #delete a column

#index itself is an object
obj = Series(range(3), index=['a', 'b', 'c'])
index = obj.index
index = pd.Index(np.arange(3))
obj2 = Series([1.5, -2.5, 0], index=index)
obj2.index is index
#some methods and attributes of Index class
#append, diff, intersection, union, isin, delete, drop, insert, unique, is_unique, ismonotonic

#Essential Functionality=======================================================

#reindexing----------------------------------
obj = Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
obj
obj.reindex(['a', 'b', 'c', 'd', 'e'])  #reindex is not inplace
obj.reindex(['a', 'b', 'c', 'd', 'e'], fill_value=0)
obj3 = Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
obj3.reindex(range(6), method='ffill')

frame = DataFrame(np.arange(9).reshape((3, 3)), index=['a', 'c', 'd'],columns=['Ohio', 'Texas', 'California'])
frame
frame2 = frame.reindex(['a', 'b', 'c', 'd'])
frame2
states = ['Texas', 'Utah', 'California']
frame.reindex(columns=states)
frame.reindex(index=['a', 'b', 'c', 'd'], method='ffill', columns=states)

# Arithmetic and data alignment
df1 = DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
df2 = DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))

df1+df2
df1.add(df2, fill_value=0)

# Operations between DataFrame and Series
frame = DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'),
                  index=['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.ix[0]
frame - series #boardcast on each row
series2 = frame['d']
frame.sub(series2, axis=0)  #boardcast on each column

#Function application and mapping------------------------
# numpy的ufunc会被应用到元素级
frame = DataFrame(np.random.randn(4, 3), columns=list('bde'),index=['Utah', 'Ohio', 'Texas', 'Oregon'])
np.abs(frame)
frame.abs()
# DataFrame的apply默认将函数应用在各列
f = lambda x: x.max() - x.min() #x is an array?
frame.apply(f)
frame.apply(f,axis=1)   #应用于各行

def f(x):
    return Series([x.min(), x.max()], index = ['min', 'max'])
frame.apply(f)
#元素级的python函数应该用applymap，Series用map
format = lambda x: '%.2f' % x
frame.applymap(format)
frame['e'].map(format)

#Hierarchical indexing=====================================
data = Series(np.random.randn(10),index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],[1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
data.index
data['b']
data['b':'c']
data.ix[['b','d']]
data[:, 2]

data.unstack()  #unstack() 默认应用于内层

#for DataFrame
frame = DataFrame(np.arange(12).reshape((4, 3)),index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], columns=[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
frame

frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
frame
frame['Ohio']
frame.swaplevel(0, 1).sortlevel(0)

frame.sum(level='key2')
frame.sum(level='color', axis=1)
#use column to index!!!!!
frame = DataFrame({'a': range(7), 'b': range(7, 0, -1),'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'],'d': [0, 1, 2, 0, 1, 2, 3]})
frame
frame2 = frame.set_index(['c', 'd'])
frame2
frame2.reset_index() #inverse operation of set_index

#Sorting and ranking
#Axis indexes with duplicate values
#Unique values, value counts, and membership
#Handling missing data

#functions
#sort_index()
#order()
#rank()
#is_unique()
#sum()
#count()
#describe()
#min(), max()
#argmin(), argmax()
#idxmin(), idxmax()
#quantile()
#mean()
#median()
#mad()
#var()
#std()
#skew()
#kurt()
#cumsum(), cumprod()
#cummin(), cummax()
#diff()
#pct_change()










