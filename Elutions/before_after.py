import matplotlib.pyplot as plt
import pandas as pd 

#import scipy
import pylab 
pylab.rcParams['figure.figsize'] = (14.0, 8.0)

# import before data into a dataframe
data = pd.read_table('076-0087.csv', sep=';')
data.columns = ['time', 'power']
data['time'] = data['time'].map(lambda x : pd.to_datetime(x,dayfirst=True))
data['date'] = data['time'].map(lambda x: x.date())
data = data.set_index('time')
data['power'].plot()

daily_ave = data['power'].groupby(data['date']).mean()
daily_ave.drop(daily_ave.index[-1],inplace=True)
daily_ave.plot()

realize_date = pd.to_datetime('11/25/2014').date()  #realization date provided by morrisons team
realize_idx = daily_ave.index.get_loc(realize_date)

daily_ave_before = daily_ave[:realize_idx].mean()
daily_ave_after = daily_ave[realize_idx:].mean()

annual_saving = (daily_ave_before - daily_ave_after) * 24 * 365
print 'estimated annual saving from this ECM is: '+ str(annual_saving)
#to change this as a function, need file path, realize date as input
# or can we find the realization date 
#def f(url_str,date_str)
