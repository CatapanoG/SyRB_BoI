#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[3]:


import pandas as pd
import pickle


# In[45]:


# Load input data
filename = '../data/output_data'
infile = open(filename,'rb')
output_data = pickle.load(infile)
infile.close()


# In[46]:


output_data['1.1.2']['TIME_PERIOD'][0]


# In[48]:


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


# In[47]:


# Transform all series data into int64 of the type '201203'
new_data_type = {}

for series in output_data:
    series_time_freq = get_dataframe_time_freq(output_data[series])
    
    # Filter the dataframe according to its frequency
    if series_time_freq == 'Y':
        new_df = output_data[series].copy()
        new_df['TIME_PERIOD'] = new_df['TIME_PERIOD'] * 100 + 12
    elif series_time_freq == 'Q':
        #new_df = output_data[series][output_data[series]['TIME_PERIOD'].str.contains("Q4")]
        new_df = output_data[series].copy()
        new_df.loc[new_df["TIME_PERIOD"].str.contains("Q1") > 8, "B"] = "x"
        
    elif series_time_freq == 'M':
        #new_df = output_data[series][output_data[series]['TIME_PERIOD'].str.contains("12")]
        pass
    
    # Append the filtered dataframe
    new_data_type[series] = new_df


# In[31]:


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
    


# In[12]:


# Join all indicators (Pandas dataframes)
joined_data = None

for series in output_data:
    # First column
    if joined_data is None:
        joined_data = output_data[series].copy()
    # Other columns
    else:
        joined_data = pd.merge(joined_data, output_data[series],on=['TIME_PERIOD', 'REF_AREA'],how='inner')
    # Rename 'OBS_VALUE' for ease of computation
    #list_141 = list_141.rename(columns={'OBS_VALUE': series})


# In[ ]:




