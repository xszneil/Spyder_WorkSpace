# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:59:56 2015

@author: jzhu0922
"""

#import numpy 
import matplotlib.pyplot as plt
import pandas as pd 
from pandas import DataFrame 
from pandas import Series
#from datetime import datetime

def isopenat(x,op,ed,op_S,ed_S):
    if x.weekday() == 6:
        return op_S <= x.hour & x.hour < ed_S
    else:
        return op <= x.hour & x.hour < ed

def isecm(x,name,thld,mul=1):
    return (x.open==False) & (x[name] > mul*thld)

def get_ecm(df,site,thld):
    ecms = {'start': [],'end':[],'saving':[]}
    i = 0
    while i < len(df):
        if df.ecm[i]:
            j = i
            save = 0
            while df.ecm[i]:
                i = i+1
                save = save + (df[site][i] - thld) * 5 / 60
            if i-j >= 6:
                ecms['start'].append(df.index[j])
                ecms['end'].append(df.index[i])
                ecms['saving'].append(save)
        else:
            i= i + 1
    return ecms

def plot_ecm(data,start_str,end_str,site,result):
    ecms = result[site]
    p = data.ix[start_str:end_str,site].plot(title = site)
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
    df = df[['site','start','end','saving']]
    df.set_index('site',inplace=True)
    df.to_csv('lighting ecms.csv')
    return df



#read the site info=================================================
df_info = pd.read_csv('./file/site_info.csv',sep=',')
df_info['SiteID'] = df_info['SiteID'].apply(str)
df_info.set_index('SiteID',inplace=True)    #maybe just use sitename as index, as long it is verified

#read the demand power data=========================================
data = pd.read_csv('./file/site_lighting2.csv', sep=',')
data['time'] = pd.to_datetime(data['time'],dayfirst=True)
data.set_index('time',inplace=True)

#initialize result data structure
result = {}
site_count = 0
#loop through sites
for site in data.columns:
    s = df_info[df_info['SiteName'] == site].ix[0]    #get info, better if we can have siteID 
    df = DataFrame(data[site])
    # t is a series of time, check the open time and alert
    t = Series(df.index).apply(isopenat, op=s.OpenWeekday, ed=s.CloseWeekday, op_S=s.OpenWeekend, ed_S=s.CloseWeekend)
    t.index = df.index
    
    df['open'] = t
    df['ecm'] = df.apply(isecm, name=site, thld=s.Threshold, mul=1.2, axis=1)
    df.ix[-1,'ecm'] = False   #make sure the alarm will stop, lazy way
       
    if df['ecm'].any():
        result[site] = get_ecm(df,site,s.Threshold)

    site_count = site_count + 1
    print str(site_count) + ' of ' + str(len(data.columns)) + ' : ' + site

plot_ecm(data,'20150502','20150507','Bradford Victoria',result)
#plot_ecm(data,'20150501','20150507','London Chingford',result)
r = output_ecm(result)   
