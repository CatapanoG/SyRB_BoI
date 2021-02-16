#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[2]:


import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib
import numpy as np
import pandas as pd
import pickle
import seaborn as sn


# In[3]:


# Load input data
filename = '../data/renamed_output_data'
infile = open(filename,'rb')
output_data = pickle.load(infile)
infile.close()


# In[4]:


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
    return str(dataframe['FREQ'].iloc[0])
    
        
#print_series_names(output_data)
#print_series(low_freq_data)
#print_time_period_type(low_freq_data)
describe_dataset(output_data)


# In[127]:


'''# Reduce all series to their lowest frequency
low_freq_data = {}

# Filter for the last quarter (quarterly data) and last month (monthly data)
for series in output_data:
    series_time_freq = get_dataframe_time_freq(output_data[series])
    
    # Filter the dataframe according to its frequency
    if series_time_freq == 'Y':
        new_df = output_data[series]
    elif series_time_freq == 'Q':
        new_df = output_data[series][output_data[series]['TIME_PERIOD'] % 100 == 12]
    elif series_time_freq == 'M':
        new_df = output_data[series][output_data[series]['TIME_PERIOD'] % 100 == 12]
    
    # Append the filtered dataframe
    low_freq_data[series] = new_df
'''


# In[120]:


# Remove indicators with low number of obs
output_data.pop('1.1.1', None)
#output_data.pop('1.1.4', None)
#output_data.pop('1.3.7', None)
#output_data.pop('1.3.8', None)


# In[5]:


output_data.pop('Size banking sect', None)


# In[6]:


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


# In[7]:


joined_data.tail()


# In[8]:


corr = joined_data.corr().round(2)

corr


# In[39]:


sn.heatmap(corr, annot=True)


# In[36]:


# https://matplotlib.org/3.1.0/gallery/color/named_colors.html
low_info = 'slategray'
mid_info = 'slategray'
ful_info = 'paleturquoise'

# custom color map
cm = mc.LinearSegmentedColormap.from_list('mycmap', [(0, low_info),
                                                     (0.25, mid_info),
                                                    (0.5, ful_info),
                                                    (0.75, mid_info),
                                                    (1, low_info)]
                                        )

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12,12))         # Sample figsize in inches
#sns.heatmap(df1.iloc[:, 1:6:], annot=True, linewidths=.5, ax=ax)

sn.set(font_scale=1.4)
#sn.heatmap(corr, annot=True, cmap=cm , ax=ax, linewidths=.5, annot_kws={"size": 16})
sn.heatmap(corr, annot=True, cmap=cm, vmin=-1, vmax=1, ax=ax, linewidths=.5, annot_kws={"size": 16})


# In[ ]:




