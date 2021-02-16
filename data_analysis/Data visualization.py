#!/usr/bin/env python
# coding: utf-8

# In[55]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')

# Jupyter 100% screen width
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


# In[28]:


import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sn
from typing import List


# In[29]:


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
    time_str = str(dataframe['TIME_PERIOD'][0])
    if len(time_str) == 4:
        return 'Y'
    elif time_str[5] == 'Q':
        return 'Q'
    else:
        return 'M'
        
describe_dataset(output_data)


# In[62]:


NUM_COLS = 5
PLOT_WIDTH = 20
SUBPLOT_SIZE = 5
OVERALL_TITLE_FONT_SIZE = 20
SUBPLOT_TITLE_FONT_SIZE = 14

PLOT_TITLE = 'SyRB Core indicators'

INTERESTING_COUNTRIES = ['IT', 'DE', 'FR', 'ES']


# In[58]:


def get_subplots(num_subplots: int, overall_title: str) -> (plt.Figure, List[plt.Axes]):
    num_rows = get_num_rows(num_subplots)

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(num_rows, NUM_COLS,
                           figsize=(PLOT_WIDTH, SUBPLOT_SIZE * num_rows))

    fig.suptitle(overall_title, fontsize=OVERALL_TITLE_FONT_SIZE)

    axs: List[plt.Axes] = ax.flatten().tolist()

    return fig, axs


def get_num_rows(tot_num_subplots: int) -> int:
    num_rows: int = int(tot_num_subplots / NUM_COLS)

    if tot_num_subplots % NUM_COLS > 0:
        num_rows += 1

    return num_rows

def format_date_for_matplotlib(raw_date):
    # date_fmt is a string giving the correct format for your data. In this case
    # we are using 'YYYYMMDD.0' as your dates are actually floats.
    date_fmt = '%Y%m'

    # Use a list comprehension to convert your dates into datetime objects.
    # In the list comp. strptime is used to convert from a string to a datetime
    # object.
    dt_date = [dt.datetime.strptime(str(i), date_fmt) for i in raw_date]

    # Finally we convert the datetime objects into the format used by matplotlib
    # in plotting using matplotlib.dates.date2num
    return [mdates.date2num(i) for i in dt_date]

# Matplotlib colormaps: https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
# Usage: change: pl.cm.<NAME_OF_THE_COLORMAP>(np.linspace(0,1,num_series))
def get_colors(num_series: int):
    return pl.cm.Accent(np.linspace(0,1,num_series))


# In[63]:


colors = get_colors(len(INTERESTING_COUNTRIES))



fig, axs = get_subplots(num_subplots=len(output_data), overall_title=PLOT_TITLE)
fig.patch.set_facecolor('xkcd:white')

for i, series in zip(range(len(output_data)), output_data):
    #countries =  output_data[series]['REF_AREA'].unique()
    for j, country in zip(range(len(INTERESTING_COUNTRIES)),INTERESTING_COUNTRIES):
        data = output_data[series][output_data[series]['REF_AREA'] == country]

        x = format_date_for_matplotlib(data['TIME_PERIOD'])
        y = data['OBS_VALUE']

        axs[i].set_title(series, fontsize=SUBPLOT_TITLE_FONT_SIZE)
        axs[i].plot(x, y, color=colors[j], label=country)

        # Create a DateFormatter object which will format your tick labels properly.
        # As given in your question I have chosen "YYMMDD"
        date_formatter = mdates.DateFormatter('%Y %m')

        # Set the major tick formatter to use your date formatter.
        axs[i].xaxis.set_major_formatter(date_formatter)
        
        axs[i].tick_params(axis='x', labelrotation=25)

# This simply rotates the x-axis tick labels slightly so they fit nicely.
#fig.autofmt_xdate()

plt.tight_layout()
plt.legend()


# In[ ]:




