from __future__ import division
from numpy.random import randn
import numpy as np
np.set_printoptions(precision=4, suppress=True)

#Creating ndarrays
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)

data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
arr2.ndim
arr2.shape

#some other functions for creating
np.zeros(10)
np.zeros((3,6))	#a tuple not two parameter

a = np.arange(15)	#arange is the Numpy version of range() in python
a.reshape(3,5)

# some usefull functions
# array
# asarray
# arange
# ones, ones_like
# zeros, zeros_like
# empty, empty_like
# eye, identity
# reshape

#数组和标量之间的运算
#大小相等的数组之间的算术运算会应用的元素
#数组和标量间的算术运算会broadcast到各个元素（bool运算也会）
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
arr
arr * arr
arr - arr
1 / arr
arr ** 0.5

#Basic indexing and slicing
arr = np.arange(10)
arr
arr[5]
arr[5:8]	#5包含，8不包含
arr[5:8] = 12
arr
#slice是直接获取原对象的window而不是复制了原对象，修改会应用到原对象
#copy（）用于复制
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr2d[2]
arr2d[0][2]
arr2d[0, 2]
arr2d[:2,1:]

#boolean index
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
names == 'Bob'
names[names != 'Bob']	#可以用mask技术，可用于index维度合适的其他ndarray，不必非要是自己本身

#Fancy indexing...

# Transpose
# T
# transpose()
# swapaxes()

#Universal Functions: Fast element-wise array functions
#对ndarray中的元素执行元素级运算的函数
arr = np.arange(10)
np.sqrt(arr)
np.exp(arr)

x = randn(8)
y = randn(8)
np.maximum(x, y)

#unary ufunc
# abs, fabs
# sqrt
# square
# exp
# log, log10, log2, log1p
# sign
# ceil
# floor
# rint
# modf
# isnan
# isfinite, isinf
# cos, cosh, sin, sinh, tan, tanh
# arccos, acrcosh, arcsin, arcsinh, arctan, arctanh
# logical_not

#binary ufunc
# add
# subtract
# multiply
# divide, floor_divide
# power
# maximum, fmax
# minimum, fmin
# mod
# copysign
# greater, greater_equal, less, less_equal, equal, not_equal	>, >=, <, <=, ==, !=
# logical_and, logical_or, logical_xor	&, |, ^

#an example
points = np.arange(-5, 5, 0.01) # 1000 equally spaced points
xs, ys = np.meshgrid(points, points)
from matplotlib.pyplot import imshow, title
import matplotlib.pyplot as plt
z = np.sqrt(xs ** 2 + ys ** 2)
z
plt.imshow(z, cmap=plt.cm.gray); plt.colorbar()
plt.title("Image plot of $\sqrt{x^2 + y^2}$ for a grid of values")

#Expressing conditional logic as array operations
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

arr = randn(4, 4)
arr
np.where(arr > 0, 2, -2)
np.where(arr > 0, 2, arr) # set only positive values to 2

#Mathematical and statistical methods
arr = np.random.randn(5, 4) # normally-distributed data
arr.mean()
np.mean(arr)	#these two are the same
arr.mean(axis = 0)
arr.mean(axis = 1)
#aggregation or reduction functions
# sum
# mean
# std, var
# min, max
# argmin, argmax

#not aggregate
# cumsum
# cumprod

#bool
# any
# all

#sort
arr = randn(5,3)
arr.sort(axis = 1)	#will change arr


#Unique and other set logic
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
np.unique(names)
ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
np.unique(ints)
# unique(x)
# intersect1d(x,y)
# union1d(x,y)
# in1d(x,y)
# setdiffid(x,y)
# setxor(x,y)

# Linear algebra...
