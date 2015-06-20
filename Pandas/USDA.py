# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 16:20:08 2015

@author: jzhu0922
"""
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import json
db = json.load(open('foods-2011-10-03.json'))
len(db)

db[0].keys()
db[0]['nutrients'][0]   #for the first food in the db,  the first nutrients in that food

nutrients = DataFrame(db[0]['nutrients'])   #for the first food in the db, all nutrients in that food
nutrients[:7]

#from keys() of db[0], we know key nutritions, portions, tags are lists, but other keys are not, so we extract those info
info_keys = ['description', 'group', 'id', 'manufacturer']
info = DataFrame(db, columns=info_keys)
info[:5]
col_mapping = {'description':'food','group':'fgroup'}
info = info.rename(columns=col_mapping, copy=False)

pd.value_counts(info['group']) #number of food in each group

#get DataFrame for nutrients
nutrients = []
for rec in db:  #notice that db is list of dicts
    fnuts = DataFrame(rec['nutrients']) #say db[0]['nutrients'] is still a dict
    fnuts['id'] = rec['id'] #take a id to show where the nutrient comes from
    nutrients.append(fnuts) #nutrients is a list of DataFrame

nutrients = pd.concat(nutrients, ignore_index=True)
nutrients = nutrients.drop_duplicates()


#before join food and nutrients
col_mapping = {'description':'food','group':'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
col_mapping = {'description':'nutrient','group':'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)

ndata = pd.merge(nutrients, info, on='id',how='outer')

#we can get mean value for each nutrient in each food group
result = ndata.groupby(['nutrient', 'fgroup'])['value'].mean()
#say we want to know which kind of food contains 'Zinc, Zn' most
result['Zinc, Zn'].order().plot(kind='barh')


by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])

get_maximum = lambda x: x.xs(x.value.idxmax())
get_minimum = lambda x: x.xs(x.value.idxmin())

max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]

# make the food a little smaller
max_foods.food = max_foods.food.str[:50]
max_foods.ix['Amino Acids']['food']






