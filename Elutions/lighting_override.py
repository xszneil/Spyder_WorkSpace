# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 09:51:33 2015

@author: jzhu0922
"""

import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
from pandas import Series
from datetime import datetime

data = pd.read_table('BradfordVictoria_May.csv', sep=',')
data.columns = ['time', 'power']

data['time'] = data['time'].map(lambda x : pd.to_datetime(x,dayfirst=True))
#data['date'] = data['time'].map(lambda x: x.date())

#Bradford Victoria, Weekday 7:00-23:00, Sunday 10:00-16:00, hard code now
def isopenat(x):
    if x.weekday() == 6:
        return 10 <= x.hour & x.hour < 16
    else:
        return 7 <= x.hour & x.hour < 23

def ecm(x):
    return (x.open==False) & (x.power > 50.0)

data['open'] = data['time'].map(isopenat)
data['ecm'] = data.apply(ecm,axis=1)
data = data.set_index('time')

ecms = {
    'start': [],
    'end':[],
    'saving':[]
}
# loop through 
i = 0
while i < len(data):
    if data.ecm[i]:
        j = i
        save = 0
        while data.ecm[i]:
            i = i+1
            save = save + (data.power[i] - 25.0) * 5 / 60
        ecms['start'].append(data.index[j])
        ecms['end'].append(data.index[i])
        ecms['saving'].append(save)
        #print ('start: ' + str(data.time[j]) + '; end: ' + str(data.time[i]) + '; saving: ' + str(save))
    else:
        i= i + 1
        
df_ecm = DataFrame(ecms, columns=['start','end','saving'])

#data.ix['20150430 8:00':'20150430 10:00','power']
#df_morning = data[data.index.hour == 8]

data.ix['20150503':'20150508','power'].plot()
for i in range(len(ecms['start'])):
    plt.axvspan(ecms['start'][i], ecms['end'][i], facecolor='r', alpha=0.4)

