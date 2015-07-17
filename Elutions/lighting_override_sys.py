# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:59:56 2015

@author: jzhu0922
"""

import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
from pandas import Series
#from datetime import datetime

def is_open_at(x, op, ed, op_S, ed_S, delay=0):
    if x.weekday() == 6:
        return op_S-delay <= x.hour & x.hour < ed_S + delay
    else:
        return op-delay <= x.hour & x.hour < ed + delay

def is_lighting_ecm(x, name, thld, mult=1, bar=0):
    return (x.open == False) & (x[name] > mult * thld + bar)

def event_to_ecm(df, site, thld, limit = 0):
    ecms = {'start':[], 'end':[], 'saving':[]}
    i = 0
    while i < len(df):
        if df.ecm[i]:
            j = i
            save = 0
            while df.ecm[i]:
                i = i + 1
                save = save + (df[site][i] - thld) * 5 / 60
            if i-j >= limit:
                ecms['start'].append(df.index[j])
                ecms['end'].append(df.index[i])
                ecms['saving'].append(save)
        else:
            i = i + 1
    return ecms

def plot_ecm(data, start_str, end_str, site, result):
    ecms = result[site]
    p = data.ix[start_str:end_str, site].plot(title = site)
    p.set_ylabel('Lighting Demand Power 5 min (kw)')
    p.set_xlabel('Timestamp')
    for i in range(len(ecms['start'])):
        p.axvspan(ecms['start'][i], ecms['end'][i], facecolor='r', alpha=0.3)

def output_ecm(result):
    result_list = []
    for k,v in result.iteritems():
        df_ecm = DataFrame(v)
        df_ecm['site'] = k
        result_list.append(df_ecm)
    df= pd.concat(result_list)
    df = df[['site', 'start', 'end', 'saving']]
    df.set_index('site', inplace=True)
    return df

def simulation(data,df_info):  
    #initialize result data structure
    result = {}
    site_count = 0
    #loop through sites
    for site in data.columns:
        s = df_info.ix[site]    #get info, better if we can have siteID 
        df = DataFrame(data[site])
        # t is a series of time, check the open time and alert
        t = Series(df.index).apply(is_open_at, op=s.OpenWeekday, ed=s.CloseWeekday, op_S=s.OpenWeekend, ed_S=s.CloseWeekend, delay=1)
        t.index = df.index
        
        df['open'] = t
        df['ecm'] = df.apply(is_lighting_ecm, name=site, thld=s.Threshold, mult=1.3, bar = 3, axis=1)
        df.ix[-1,'ecm'] = False   #make sure the alarm will stop, i know i am lazy
           
        if df['ecm'].any():
            item = event_to_ecm(df,site,s.Threshold,limit=6)
            if len(item['start'])>0: result[site] = item
    
        site_count = site_count + 1
        print str(site_count) + ' of ' + str(len(data.columns)) + ' : ' + site
    
    return result

if __name__ == "__main__":
    #read the site info=================================================
    df_info = pd.read_csv('./file/site_info.csv',sep=',')
    #df_info['SiteID'] = df_info['SiteID'].apply(str)
    df_info.set_index('SiteName', inplace=True)    #maybe just use sitename as index, as long it is verified
    
    #read the demand power data=========================================
    data = pd.read_csv('./file/Jun BR.csv', sep=',')
    data['time'] = pd.to_datetime(data['time'], dayfirst=True)
    data.set_index('time', inplace=True)
    data.replace(to_replace=0, value=numpy.NaN, inplace=True) #some 0s seems like missing value
    data.fillna(method='ffill', inplace=True) 
    
    result = simulation(data, df_info)
    
    sites = data.columns.values
    
    r1 = output_ecm(result)   
    r2 = r1.merge(df_info,left_index=True,right_index=True)
    r2.to_csv('./Lighting ECM BR Jun.csv')    
    
    #r2[r2.SiteName == sites[9]]
    
    l = r2.SiteName.unique()
    for i in range(len(l)):
        plot_ecm(data,'20150601','20150630',l[i],result)
        plt.savefig("./fig/"+l[i]+".jpeg")
        plt.close()
    
