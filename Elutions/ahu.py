# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:53:12 2015

@author: jzhu0922
"""

import matplotlib.pyplot as plt
import pandas as pd 

#import scipy
import pylab 

base_url = 'file/ahu/historyExport'
dfs = []
for i in range(5):
    file_url = base_url + str(i) + '.txt'
    data = data = pd.read_table(file_url,sep=',')
    dfs.append(data)
data = pd.concat(dfs,ignore_index = True)

data['timestamp'] = data['date'] + data['time']
data['comment'] = data['comment1'].add(data['comment2'],fill_value='')

for i in ['date','time','comment1','comment2']:
    del data[i]


data = data[data['timestamp'].notnull()]
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['ahu'] = data['ahu'].str.strip()
data['value'] = data['value'].str.strip()
data['comment'] = data['comment'].str.strip()


s = data.ahu.drop_duplicates()
#s.index = range(s.count())
data['timestamp'] = pd.to_datetime(data['timestamp']) #slow
data.set_index('timestamp',inplace=True)
