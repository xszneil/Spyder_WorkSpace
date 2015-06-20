# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 11:03:33 2014

@author: mikiyas
"""
# cd/ 
# cd Users/mikiyas/Documents/work stuff/Maestro exports/

# set up the appropriate environment 

import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
#import scipy
import pylab 
pylab.rcParams['figure.figsize'] = (13.0, 5.0)
from matplotlib.ticker import FuncFormatter

# elutions specific analysis functions live in funcs.py file 
import funcs

# setup environment 
#funcs.env_setup() ------- need to figure out why this doesn't work!!!

# import sensor datainto a Pandas dataframe
tbl = pd.read_table('vodafone-bedford-mech-temps', sep=';')
data = pd.DataFrame(tbl)
data.columns = ['date' , 'mech' , 'sensorTemp' , 'OAT']
date = data.date
mech = data.mech
sensorTemp = data.sensorTemp
OAT = data.OAT

# import another table 
tbl2 = pd.read_table('vodafone_OAT_mech.csv', sep=';')
data2 = pd.DataFrame (tbl2)
data2.columns = ['date' , 'AirTemp' , 'mech2']
date2 = data2.date
mech2 = data2.mech2

# yet another - these are time indices and OAT that correspond to the power data in table 2
tbl3 = pd.read_table('vodafone_OAT.csv', sep=';')
data3 = pd.DataFrame (tbl3)
data3.columns = ['date' , 'OAT']
date3 = data3.date
OAT = data3.OAT

# ------ generate fake data points ------- 
number_of_points = 1000
rand_array = numpy.random.random( (number_of_points) )
plt.plot(rand_array)

"""
# interpolate temp data 
plt.plot(OAT)
len(OAT)
old_grid = numpy.linspace(0,len(OAT), len(OAT) )
new_grid = numpy.linspace(0,len(OAT), 1000)
new_OAT = numpy.interp(new_grid, old_grid, OAT )
plt.plot(new_OAT)
"""

# plot some of the data 
plt.plot(mech2)
  
# look at data without outlier values 
mech_trm = funcs.reject_outliers(mech2, 3.5)


# extract slice of data from mechanical load sources     
x_knot = 0; dur_mins = len(mech)*5; power = funcs.zoom_demand(mech,x_knot,dur_mins);

# We could also slice up and analyze temperature data
x_knot = 0; dur_mins = len(mech)*5 - 60000; temps = funcs.zoom_temp(sensorTemp, x_knot, dur_mins);

# we could import temperature data and analyze ECM-specific trends   
#x = numpy.arange(1000)
#y = 23 + numpy.sin(x)
#plt.plot(x,y)
 
 
funcs.setpoint_ECM(power, temps, 23, 2, "C")

# We can calculate total power ocnsumption for loads        
mech_consumption = funcs.total_consumption(power, 0.09)

# Track billings month-by-month (fake data)
indd = numpy.arange(1,13,1)
Ave_power_2014 = [56.34, 58.23, 57.56, 59.43, 60.43, 54.43, 53.22, 53.21, 54.43, 51.12, 50.45, 50.00]
#plt.plot(Ave_power_2014)
wid = 0.35
rects = plt.bar(indd-wid/2, Ave_power_2014, width=wid, bottom=0, color='y')
plt.axis([0, 13, 0.9*numpy.min(Ave_power_2014), 1.08*numpy.max(Ave_power_2014) ])
plt.title('average monthly power')
plt.ylabel('ave. power   kW')
plt.xlabel('month')

# monthly billing tracking (fake data)
bill_2014 = [(0.09)*float(720)*x for x in Ave_power_2014]

rects = plt.bar(indd-wid/2, bill_2014, width=wid, bottom=0, color='g')
plt.axis([0, 13, 0.9*numpy.min(bill_2014), 1.08*numpy.max(bill_2014) ])
plt.title('Monthly Billings')
plt.ylabel('Cost of electricity    euros')
plt.xlabel('month')

# include plotting the deltas from month to month 
def series_delta(data_in):
    delta = []
    for x in range(2,len(data_in)):
        delta.append( ((data_in[x] - data_in[x - 1])/data_in[x-1])*100 ) 
    return delta 
    
power_2014_delta = series_delta(bill_2014)

indd = numpy.arange(1,11,1)
rects = plt.bar(indd-wid/2, power_2014_delta, width=wid, bottom=0, color='g')
plt.axis([0, 13, 0.9*numpy.min(power_2014_delta), 1.08*numpy.max(power_2014_delta) ])
plt.title('Monthly Changes')
plt.ylabel('percentage change in billings    %')
plt.xlabel('month')

# Free-cooling analysis 
def free_cooling (power_data, outside_temp, threshold):
    n_fans = 120 # numer of fans attached to chiller 
    kwPF = 2.5 # kilowatts per fan 
    duration = 12*30 # hours - should be calculated automatically from time-stamps     
    ppkw = 0.09  # price per kilowatt    
    
    fan_energy = n_fans*kwPF*duration  # kWhr
    fan_opex = fan_energy*ppkw
    
    # --- make sure data series match size ---
    if (len(outside_temp) != len(power_data)):
        old_grid = numpy.linspace(0,len(outside_temp), len(outside_temp) )
        new_grid = numpy.linspace(0,len(outside_temp), len(power_data))
        new_OAT = numpy.interp( new_grid, old_grid, outside_temp )
    
    # logic to calculate percentage of values under the threshold 
    UT_list = []
    for index, temp in enumerate(outside_temp):
        if (temp < threshold):
            UT_list.append(index)
    
    num_total = float(numpy.count_nonzero(~numpy.isnan(outside_temp)))
    num_UT = len(UT_list)
    PCT_UT = (num_UT/num_total)*100
    
    print "\n Free-cooling opportunity detected for {0:.2f}% of the time in this period.".format(PCT_UT)
    energy_opex = (5/float(60))*(numpy.sum(power_data))
    free_cooling_savings = energy_opex - fan_opex 
    
    print "\n-----------------------------------------------------------------------------------"        
    print " RECOMMEND - Enable Free-Cooling Operation when outside temperature falls below {0}C.".format(threshold)
    print "-----------------------------------------------------------------------------------"        
    
    print "\n Baseline cost for this period is €{0:,.02f}.".format(energy_opex)
    print "\n This ECM, on average, would have saved €{0:,.02f}, reducing billings to €{1:,.02f}.".format(free_cooling_savings, fan_opex)
    
    # show the plot of power and OTA         
    fig, ax1 = plt.subplots()    
    ax1.plot(power_data, 'b', zorder = 1)
    ax1.set_xlabel('time (5 mins)')

    plt.title('power & temperature')
    plt.xlabel('time index (every 5 mins)') 
    ax1.set_ylabel('AHU Power Demand    kW', color='b')
    
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(new_OAT, 'r', linewidth = 3 , zorder = 2)
    ax2.set_ylabel('Outside Air Temperature   C', color='r')
    ax2.axhline(y=threshold,xmin=0,xmax=len(power_data),c="green", linewidth=3,zorder=2)

    for tl in ax2.get_yticklabels():
        tl.set_color('r')
        
        
    #ax3 = ax1.twinx()
    #ax3.axhline(y=threshold,xmin=0,xmax=len(power_data),c="green", linewidth=3,zorder=2)

    
    plt.show()
    
    
    
    
    

free_cooling(mech2, OAT, 10)

# import time-stamp reader from Pandas 

form 

# write a function totimezone()

# write function hour()

# 

# detect all values of Load above threshold

# calculate cost (L - Th)*
















