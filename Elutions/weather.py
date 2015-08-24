# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:15:16 2015

@author: jzhu0922
"""

import urllib2
import json
import datetime
from datetime import timedelta
import re
import time
import pandas as pd

base_url1 = 'http://api.wunderground.com/api/165967bed6d1af1b/history_'
base_url2 = 'http://api.wunderground.com/api/fdd96b9124a76f1e/history_'
base_url3 = 'http://api.wunderground.com/api/ae63a141e2e05630/history_'
start_date = datetime.date(2013,8,10);
locations = ['Bristol','Northolt','Birmingham','Exeter','Brize Norton','Biggin Hill','Cranfield','Glasgow','Leeds And Bradford','Farnborough','Manchester','Heathrow','Edinburgh Airport']
#locations = ['Bristol','Northolt']
bases = [base_url1, base_url2, base_url3]

request_count = 0
result = {}
dates = []

def get_mean_temp(url):
    try:
        f = urllib2.urlopen(url)
        parsed_json = json.loads(f.read())
        temp_str = parsed_json['history']['dailysummary'][0]['meantempm']
        temp = float(temp_str)
        f.close()
        return temp
    except Exception, e:
        print e.reason

for loc in locations:
    loc_str = re.sub('\s+', '%20', loc)
    result[loc] = {}
    print loc
    for day in range(7):
        for year in range(3):
            date = start_date + timedelta(day + 365 * year)
            date_str = str(date).replace('-','')
            url = bases[year] + date_str + '/q/GB/' + loc_str + '.json'
            temp = get_mean_temp(url)
            result[loc][date_str] = temp
            
            if date_str not in dates:
                dates.append(date_str)
            
        request_count = request_count + 1
        if request_count % 10 == 0:
            time.sleep(60)            
    
    print result[loc]

df = pd.DataFrame(result).T[dates]
df.to_csv('13 site Aug 10-16.csv')
