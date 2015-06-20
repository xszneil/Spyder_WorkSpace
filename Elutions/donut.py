# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:09:35 2015

@author: jzhu0922
"""

import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
from pandas import Series
from datetime import datetime

data = pd.read_table('donut.csv', sep=';')
data[data.isnull().any(axis=1)]

data = data.fillna(method='ffill')
data['Date'] = data['Date'].map(lambda x : pd.to_datetime(x,dayfirst=True))
data = data.set_index('Date')
data.index.name = 'timestamp'

b1 = 4 <= data.index.hour
b2 = data.index.hour < 7
b3 = data.index.weekday != 6
b4 = b1 & b2 & b3

data_morning = data[b4]
data_morning_ave = data_morning.resample('D',how='mean')

data_morning_ave[:'20150511'].mean() - data_morning_ave['20150512':].mean()
data_morning_ave.std()

#for plot
ndays = (data.index[-1].date() - data.index[0].date()).days + 1
four = pd.date_range('4/1/2015 04:00:00', periods=ndays)
seven = pd.date_range('4/1/2015 07:00:00', periods=ndays)

data['20150401':'20150403'].plot()
for i in range(ndays):
    plt.axvspan(four[i], seven[i], facecolor='y', alpha=0.3)
