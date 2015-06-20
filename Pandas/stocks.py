# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:37:52 2015

@author: ZhuJiaqi
"""
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import pandas.io.data as web
import matplotlib.pyplot as plt
import pylab

all_data = {}   #all_data is a dict of DataFrame
for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']:
    all_data[ticker] = web.get_data_yahoo(ticker)

price = DataFrame({tic: data['Adj Close']
                   for tic, data in all_data.iteritems()})
volume = DataFrame({tic: data['Volume']
                    for tic, data in all_data.iteritems()})

plt.plot(price)

returns = price.pct_change()
returns.corr()
returns.cov()

returns.corrwith(returns.IBM)