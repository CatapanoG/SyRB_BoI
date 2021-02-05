#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[38]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sn


# In[ ]:


# Load input data
filename = '../data/output_data'
infile = open(filename,'rb')
output_data = pickle.load(infile)
infile.close()


# In[ ]:


# Dataset methods
def print_series_names(dataset):
    for key in dataset:
        print(key)
        
def print_series(dataset):
    for key in dataset:
        print(dataset[key])
        
def print_time_period_type(dataset):
    for key in dataset:
        time_str = str(dataset[key]['TIME_PERIOD'][0]) + " "
        freq = get_dataframe_time_freq(dataset[key])
        print(time_str + freq)
        

def describe_dataset(dataset):
    for key in dataset:
        print(key)
        print(dataset[key].describe(include='all'))
        print('\n')
        
# Dataframe methods
def get_dataframe_time_freq(dataframe):
    time_str = str(dataframe['TIME_PERIOD'][0])
    if len(time_str) == 4:
        return 'Y'
    elif time_str[5] == 'Q':
        return 'Q'
    else:
        return 'M'
        
#print_series_names(output_data)
#print_series(low_freq_data)
#print_time_period_type(low_freq_data)
describe_dataset(new_data_type)


# In[ ]:


# Reduce all series to their lowest frequency
low_freq_data = {}

# Filter for the last quarter (quarterly data) and last month (monthly data)
for series in output_data:
    series_time_freq = get_dataframe_time_freq(output_data[series])
    
    # Filter the dataframe according to its frequency
    if series_time_freq == 'Y':
        new_df = output_data[series]
    elif series_time_freq == 'Q':
        new_df = output_data[series][output_data[series]['TIME_PERIOD'].str.contains("Q4")]
    elif series_time_freq == 'M':
        new_df = output_data[series][output_data[series]['TIME_PERIOD'].str.contains("12")]
    
    # Append the filtered dataframe
    low_freq_data[series] = new_df
    


# In[22]:


# Join all indicators (Pandas dataframes)
joined_data = None

for series in output_data:
    # Filter out 'FREQ'
    filtered_df = output_data[series].filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)
    # First column
    if joined_data is None:
        joined_data = filtered_df.copy()
    # Other columns
    else:
        joined_data = pd.merge(joined_data, filtered_df,on=['TIME_PERIOD', 'REF_AREA'],how='inner')
    # Rename 'OBS_VALUE' for ease of computation
    joined_data = joined_data.rename(columns={'OBS_VALUE': series})


# In[23]:


joined_data.tail()


# In[36]:


corr = joined_data.corr()

corr


# In[39]:


sn.heatmap(corr, annot=True)


# In[ ]:




