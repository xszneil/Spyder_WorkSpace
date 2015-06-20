# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 10:10:35 2014

@author: mikiyas
"""
def env_setup():
    import numpy 
    import matplotlib.pyplot as plt
    import pandas as pd 
    from pandas import Series, DataFrame 
    import pylab 
    pylab.rcParams['figure.figsize'] = (13.0, 8.0)
    print "environment has been configured."
    print "data analysis and inline plotting enabled."




import numpy 
import matplotlib.pyplot as plt

# reject outliers (m = number of stds from main that will be preserved)
def reject_outliers(data_in, m):
    mu = numpy.nanmean(data_in)
    std = numpy.std(data_in)
    data_out = [pt for pt in data_in if mu-m*std < pt < mu+m*std] 
    plt.plot(data_out, zorder = 1)
    plt.title('trimmed data')
    plt.ylabel('')
    plt.xlabel('time  (5 mins)') 
    plt.axhline(y=mu,xmin=0,xmax=len(data_out),c="red", linewidth=2,zorder=2)
    print "\n Plot of data with points outside {0} std deviations of the mean rejected.".format(m)
    print "\n NOTE: reject_outliers also returns data_out as an array."    
    return data_out  
    

# extract slices of data from load sources  
def zoom_demand(load_data_in, x_knot , mins):
    slice_data = load_data_in[x_knot : numpy.round(x_knot+mins/5)]
    # check for data-loss
    if numpy.isnan(slice_data).any() :
        print "\n data loss detected. "
    # plot slice with stats
    plt.plot(slice_data, zorder=1)
    ave = numpy.nanmean(slice_data)
    print "\n The average of this slice is {0:.2f}".format(ave)
    stdd = numpy.nanstd(slice_data)
    varr = numpy.nanvar(slice_data)
    print "\n The standard deviation of this slice is {0:.2f} , and the variance is {1:.2f}".format(stdd, varr)
    plt.axhline(y=ave,xmin=0,xmax=len(slice_data),c="red", linewidth=2,zorder=2)
    plt.title('Load')
    plt.ylabel('kW')
    plt.xlabel('time  {0} mins to {1} mins'.format(x_knot/5 , x_knot+mins/5))
    return slice_data
    
    
# extract slices of data from temperature sources  
def zoom_temp(temp_data_in, x_knot , mins):
    slice_data = temp_data_in[x_knot : numpy.round(x_knot+mins/5)]
    # check for data-loss
    if numpy.isnan(slice_data).any() :
        print "\n data loss detected."
    # plot slice with stats
    plt.plot(slice_data,--, zorder=1)
    ave = numpy.nanmean(slice_data)
    print "\n The average of this slice is {0:.2f}".format(ave)
    stdd = numpy.nanstd(slice_data)
    varr = numpy.nanvar(slice_data)
    print "\n The standard deviation of this slice is {0:.2f} , and the variance is {1:.2f}".format(stdd, varr)
    plt.axhline(y=ave,xmin=0,xmax=len(slice_data),c="red", linewidth=2,zorder=2)
    plt.title('Temperature')
    plt.ylabel('C')
    plt.xlabel('time  {0} mins to {1} mins'.format(x_knot*5 , x_knot+mins*5))
    print "\n NOTE: reject_outliers also returns data_out as an array."    
    return slice_data
    
    
# determine if temperature data is within ECM defined parameters    
def setpoint_ECM(power_in, temp_in, set_point, plus_or_minus, units):   
    
    ppkwh = 0.09
    # list to store indices of our-of-range (OOR) values
    OOR_index_list = []
    # list to store indices that are ub a tight deadband
    deadband = [] 
    std = plus_or_minus
    
    for index, temp in enumerate(temp_in):
        if (~numpy.isnan(temp)) and (not (set_point - std < temp < set_point + std)):
            OOR_index_list.append(index)
    
    temp_ave = numpy.nanmean(temp_in) 
    
    
    plt.plot(temp_in, zorder = 1)
    plt.title('temperature')
    plt.ylabel('{0}'.format(units))
    plt.xlabel('time index (every 5 mins)') 
    plt.axhline(y=set_point,xmin=0,xmax=len(temp_in),c="blue", linewidth=3,zorder=2)
    plt.axhline(y=set_point+std,xmin=0,xmax=len(temp_in),c="red", linewidth=1,zorder=2)
    plt.axhline(y=set_point-std, xmin=0,xmax=len(temp_in),c="red", linewidth=1,zorder=2)
    plt.axhline(y=temp_ave, xmin=0,xmax=len(temp_in),c="green", linewidth=1,zorder=2)
    
    
    num_total = float(numpy.count_nonzero(~numpy.isnan(temp_in)))
    num_nan = len(temp_in) - num_total    
    num_OOR = len(OOR_index_list)
    PCT_OOR = (num_OOR/num_total)*100
    PCT_nan = (num_nan/num_total)*100
    
    ave_diff = numpy.abs(temp_ave - set_point) 
    
    print "\n {0:.2f}% of the observed temperature values were outside of desired range.".format(PCT_OOR)
    print "\n {0:.2f}% of timestamps don't contain values (data-loss).".format(PCT_nan)
    if (temp_ave < set_point and PCT_OOR > 50): 
        print "\n Overcooling detected:"
        print "\n Average temperature for this period was {0:.02f}{1} below set-point.".format(ave_diff, units)
        print "-----------------------------------------------------------------------------"        
        print " RECOMMEND - increase setpoint to {0}{1}. ".format(set_point, units)
        print "-----------------------------------------------------------------------------"        
    elif (temp_ave > set_point and PCT_OOR > 50):
        print "\n Overheating detected:"
        print "\n Average temperature for this period was {0:.02f}{1} above set-point.".format(ave_diff, units)
        print "-----------------------------------------------------------------------------"        
        print " RECOMMEND - cooling equipment may be turned on."
        print "-----------------------------------------------------------------------------"        

    # We would also like to know if the temperature is too "tight"
    for index, temp in enumerate(temp_in):
        if (~numpy.isnan(temp)) and (temp_ave - 1 < temp < temp_ave + 1):
            deadband.append(index)
    
    num_deadband = len(deadband)
    PCT_deadband = (num_deadband/num_total)*100
    if (PCT_deadband > 60):
        print "\n More than 60% of values are within +/- 1{0} of the average temperature.".format(units)
        print "-----------------------------------------------------------------------------"        
        print " RECOMMEND - Expand deadband to prevent short-cycling."
        print "-----------------------------------------------------------------------------"        

    # we can include power and cost analysis
    # calculate the current consumption
    energy_total = (5/float(60))*(numpy.sum(power_in))
    #power_ave = numpy.nanmean(power_in)
    baseline_cost = energy_total * ppkwh
    cost_savings = ave_diff*(5/float(100))*baseline_cost
    new_cost = baseline_cost - cost_savings
    print "\n Baseline cost for period is €{0:,.2f}.".format(baseline_cost)
    print "\n This ECM, on average, would have saved €{0:,.2f}, reducing billings to €{1:,.2f}.".format(cost_savings,new_cost )

    
# calcuate total power from a load source
def total_consumption(data_in, ppkWh):
    energy_total = (5/float(60))*(numpy.sum(data_in))
    ave = numpy.nanmean(data_in)
    money = energy_total * ppkWh    
    
    print "\n Client: Vodafone | Site: Bedford "
    print "-------------------------------------"
    print "\n Total energy consumption for this period by this load was {0:,.2f} kWh.".format(energy_total)
    print "\n Average power consumption was {0:.2f} kW.".format(ave)
    print "\n Billings for this period are estimated to be €{0:,.2f} at €{1:.2f} per kWh.".format(money, ppkWh)
    return energy_total    
    
    



    


if __name__ == "__env_setup__":
    env_setup()

if __name__ == "__reject_outliers__":
    reject_outliers()
    
if __name__ == "__zoom_demand__":
    zoom_demand()
    
if __name__ == "__zoom_temp__":
    zoom_temp()

if __name__ == "__setpoint_ECM__":
    setpoint_ECM()
    
if __name__ == "__total_consumption__":
    total_consumption()
    
    
    
    
#def new_table(table_name, n_rows, n_columns) :
#    # check if the table already exists
#    file_path = "/Users/mikiyas/Documents/WORKSTUFF/Maestro exports/" + str(table_name)
#    is_it_there = os.path.exists(file_path)
#    if is_it_there:
#        print "That file already exists. Please pick a new name."
#    elif ~is_it_there:
#        # create a new pandas dataframe to hold table 
#        file_name = table_name # hold info here for writing to disk later 
#    
#
#new_table("consolidated_AC_load.csv")
#    