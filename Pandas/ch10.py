# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:57:53 2015

@author: ZhuJiaqi
"""

#Time Series
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
import pandas as pd
pd.options.display.max_rows = 12
np.set_printoptions(precision=4, suppress=True)
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(12, 4))

# Date and Time Data Types and Tools
from datetime import datetime
now = datetime.now()
now.year, now.month, now.day

delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
delta.days
delta.seconds

from datetime import timedelta
start = datetime(2011, 1, 7)
start + timedelta(12)
start - 2 * timedelta(12)

#Converting between string and datetime
stamp = datetime(2011, 1, 3)
str(stamp)
stamp.strftime('%Y-%m-%d')

value = '2011-01-03'
datetime.strptime(value, '%Y-%m-%d')
datestrs = ['7/6/2011', '8/6/2011']
[datetime.strptime(x, '%m/%d/%Y') for x in datestrs]

from dateutil.parser import parse
parse('2011-01-03')
parse('Jan 31, 1997 10:45 PM')
parse('6/12/2011', dayfirst=True)

pd.to_datetime(datestrs)

#Time Series Basics
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
         datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12)]
ts = Series(np.random.randn(6), index=dates)

#Indexing, selection, subsetting
ts['1/10/2011']
ts['20110110']

longer_ts = Series(np.random.randn(1000),
                   index=pd.date_range('1/1/2000', periods=1000))
longer_ts
longer_ts['2001']
longer_ts['2001-05']

ts[datetime(2011, 1, 7):]
ts['1/6/2011':'1/11/2011']
ts.truncate(after='1/9/2011')

dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')
long_df = DataFrame(np.random.randn(100, 4),
                    index=dates,
                    columns=['Colorado', 'Texas', 'New York', 'Ohio'])
long_df.ix['5-2001']

# Date ranges, Frequencies, and Shifting
ts
ts.resample('D')

pd.date_range('4/1/2012', '6/1/2012')   #Generating date ranges
pd.date_range(start='4/1/2012', periods=20)
pd.date_range(end='6/1/2012', periods=20)
pd.date_range('1/1/2000', '12/1/2000', freq='BM')
pd.date_range('5/2/2012 12:56:31', periods=5)
pd.date_range('5/2/2012 12:56:31', periods=5, normalize=True)

pd.date_range('1/1/2000', periods=10, freq='1h30min')   #Frequencies and Date Offsets

# Shifting (leading and lagging) data
ts = Series(np.random.randn(4),
            index=pd.date_range('1/1/2000', periods=4, freq='M'))
ts
ts.shift(2) #this kind of shift will cause drop some data
ts.shift(-2)
ts.shift(2,freq='M')    #this kind of shift just change the time

#Time Zone Handling=============================================

#Period==========================================================

#resample========================================================

#Time series plotting============================================
close_px_all = pd.read_csv('stock_px.csv', parse_dates=True, index_col=0)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
close_px = close_px.resample('B', fill_method='ffill')
close_px.info()

close_px['AAPL'].plot()
close_px.ix['2009'].plot()
close_px['AAPL'].ix['01-2011':'03-2011'].plot()

appl_q = close_px['AAPL'].resample('Q-DEC', fill_method='ffill')
appl_q.ix['2009':].plot()

#Moving window functions
close_px.AAPL.plot()
pd.rolling_mean(close_px.AAPL, 250).plot()

appl_std250 = pd.rolling_std(close_px.AAPL, 250, min_periods=10)
appl_std250[5:12]













