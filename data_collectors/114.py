#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[2]:


import sys
print(sys.executable)


# In[3]:


import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd # 0.23.0
import requests     # 2.18.4


# In[4]:


# 1.1.4 (A+B+C+D)/(E+F+G+H)

data = []

data.append(np.load('data/114_A.npy', allow_pickle=True))
data.append(np.load('data/114_B.npy', allow_pickle=True))
data.append(np.load('data/114_C.npy', allow_pickle=True))
data.append(np.load('data/114_D.npy', allow_pickle=True))
data.append(np.load('data/114_E.npy', allow_pickle=True))
data.append(np.load('data/114_F.npy', allow_pickle=True))
data.append(np.load('data/114_G.npy', allow_pickle=True))
data.append(np.load('data/114_H.npy', allow_pickle=True))

data = np.asarray(data)


# In[5]:


# data[series letter][country][time][column (date, country, value)]


# In[52]:


#
# Find common subset of countries
#

# Get a list o countries for each series
countries = []
for series in data:
    countries_in_series = []
    for country in series:
        countries_in_series.append(country[0,1])
    countries.append(countries_in_series)
    
# Get intersection of countries
countries_common = countries[0]

for i in range(1, len(countries)):
    countries_common = [e for e in countries_common if e in countries[i]]
    
print(countries_common)


# In[42]:


#
# Find common earliest time period
#

# Get latest common beginning period
minima = []
for series in data:
    print("Series ")
    minima_in_series = []
    minima_in_series_tag = []
    for country in series:
        num = int(country[0,0][0:4] + country[0,0][6:7])
        country_tag = country[0,0][0:4] + country[0,0][6:7] + " " + country[0,1]
        
        minima_in_series.append(num)
        minima_in_series_tag.append(country_tag)
        
    print(minima_in_series_tag)
        
    minima.append(max(minima_in_series))
    print(max(minima_in_series))
    
print("Common latest beginning period: " + str(max(minima)))


# In[51]:


#
# Find common latest time period
#

# Get latest common beginning period
maxima = []
for series in data:
    print("Series ")
    maxima_in_series = []
    maxima_in_series_tag = []
    for country in series:
        num = int(country[-1,0][0:4] + country[-1,0][6:7])
        country_tag = country[-1,0][0:4] + country[-1,0][6:7] + " " + country[-1,1]
        
        if(country[-1,1] != 'I7'):
            maxima_in_series.append(num)
            maxima_in_series_tag.append(country_tag)
        
    print(maxima_in_series_tag)
        
    maxima.append(min(maxima_in_series))
    print(min(maxima_in_series))
    
print("Common latest beginning period: " + str(min(maxima)))

## -> Exclude I7 (was ending in 2014)


# In[55]:


#
# Construct the derived indicator
#

# CONSTS

COUNTRIES = countries_common
START_TS = max(minima)
END_TS = min(maxima)

output = [] # [country][time][column (date, country, value)]

# data = [series][country][time][column (date, country, value)]
for country_tag in countries_common:
    for i in range()
            


# In[54]:


data[0]


# In[ ]:




