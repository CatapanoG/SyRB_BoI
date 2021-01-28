#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[2]:


from functools import reduce
import pandas as pd
import pickle


# In[3]:


# Load input data
filename = '../data/input_data'
infile = open(filename,'rb')
input_data = pickle.load(infile)
infile.close()


# In[12]:


def print_series_names(dataset):
    for key in dataset:
        print(key)
        
print_series_names(input_data)


# In[11]:


# 1.1.4

# Get list of component dataftames
list_114 = None
for series in input_data:
    if '1.1.4' in series:
        # First column
        if list_114 is None:
            list_114 = input_data[series].copy()
        # Other columns
        else:
            list_114 = pd.merge(list_114,input_data[series],on=['TIME_PERIOD', 'REF_AREA'],how='inner')
        # Rename 'OBS_VALUE' for ease of computation
        list_114 = list_114.rename(columns={'OBS_VALUE': series})

# Compute the indicator
list_114['OBS_VALUE'] = (list_114['1.1.4.A'] + list_114['1.1.4.B'] + list_114['1.1.4.C'] + list_114['1.1.4.D']) / (list_114['1.1.4.E'] + list_114['1.1.4.F'] + list_114['1.1.4.G'] + list_114['1.1.4.H'])

# Filter out component data
list_114 = list_114.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)

# Remove components from input data
for series in list(input_data.keys()):
    if '1.1.4' in series:
        del input_data[series]
        
# Append the composite indicator to input_data
input_data['1.1.4'] = list_114


# In[6]:


# 1.4.1

# Get list of component dataftames
list_141 = None
for series in input_data:
    if '1.4.1' in series:
        # First column
        if list_141 is None:
            list_141 = input_data[series].copy()
        # Other columns
        else:
            list_141 = pd.merge(list_141,input_data[series],on=['TIME_PERIOD', 'REF_AREA'],how='inner')
        # Rename 'OBS_VALUE' for ease of computation
        list_141 = list_141.rename(columns={'OBS_VALUE': series})

# Compute the indicator
list_141['OBS_VALUE'] = (list_141['1.4.1.A'] + list_141['1.4.1.B']) / list_141['1.4.1.C']

# Filter out component data
list_141 = list_141.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)

# Remove components from input data
for series in list(input_data.keys()):
    if '1.4.1' in series:
        del input_data[series]
        
# Append the composite indicator to input_data
input_data['1.4.1'] = list_141


# In[9]:


# 3.2.2

# Get list of component dataftames
list_322 = None
for series in input_data:
    if '3.2.2' in series:
        # First column
        if list_322 is None:
            list_322 = input_data[series].copy()
        # Other columns
        else:
            list_322 = pd.merge(list_322,input_data[series],on=['TIME_PERIOD', 'REF_AREA'],how='inner')
        # Rename 'OBS_VALUE' for ease of computation
        list_322 = list_322.rename(columns={'OBS_VALUE': series})

# Compute the indicator
list_322['OBS_VALUE'] = (list_322['3.2.2.A'] + list_322['3.2.2.B'] + list_322['3.2.2.C'] + list_322['3.2.2.D']) / (list_322['3.2.2.E'] + list_322['3.2.2.F'] + list_322['3.2.2.G'] + list_322['3.2.2.H'])

# Filter out component data
list_322 = list_322.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)

# Remove components from input data
for series in list(input_data.keys()):
    if '3.2.2' in series:
        del input_data[series]
        
# Append the composite indicator to input_data
input_data['3.2.2'] = list_322


# In[16]:


input_data['1.4.1'].tail()


# In[13]:


# Save the data on the disk ('../data/input_data')
def save_all_input_data():
    filename = '../data/output_data'
    outfile = open(filename,'wb')
    pickle.dump(input_data,outfile)
    outfile.close()


# In[14]:


save_all_input_data()


# In[ ]:




