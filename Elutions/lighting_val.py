import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
from pandas import Series
#import scipy
import pylab 
pylab.rcParams['figure.figsize'] = (14.0, 8.0)

from datetime import datetime 
from dateutil.parser import parse 

# dateutil parse('12/01/2014 00:35:00', dayfirst=True)

# import before ECM data into a dataframe
xitbl_b = pd.read_table('csvConvert.csv', sep=';')
data_b = pd.DataFrame(tbl_b)
data_b.columns = ['date' , 'power']
date_b = data_b.date
power_b = data_b.power

# use pandas to convert strings to date - x = pd.to_datetime('12/01/2014 00:35:00', dayfirst=True)

#covert to date objects
dates_b = []
for x in date:
    dates_b.append( pd.to_datetime(x, dayfirst=True) )

ts_b = Series((power_b.tolist()), index=dates_b)

thresh = 0

#plot data
plt.plot(ts_b, zorder = 1)
plt.title('Lighting Before ECM')
plt.ylabel('Power  kW')
plt.xlabel('time index (every 5 mins)') 

# setup energy bucket
Eb = 0

# loop through timeSeries
for id in numpy.arange(0,len(ts_b)):
    pw = ts_b[id]
    stmp = ts_b.index[id]
    hr = stmp.hour
    # print hr
    
    if (hr < 8) or (hr > 21):  #and (pw > thresh):
        #print hr
        E_id = (pw - thresh)*(5/float(60)) 
        #print E_id
        Eb = Eb + E_id
        

print Eb

count = 2555
avg = 46.6
E_av = (avg - thresh)*(5/float(60))*2555*0.4