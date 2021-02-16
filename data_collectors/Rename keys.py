#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[3]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sn


# In[4]:


# Load input data
filename = '../data/output_data'
infile = open(filename,'rb')
output_data = pickle.load(infile)
infile.close()


# In[9]:


def print_series_names(dataset):
    for key in dataset:
        print(key)
        
print_series_names(output_data)


# In[6]:


output_data['Size banking sect'] = output_data.pop('1.1.1')
output_data['CR5'] = output_data.pop('1.1.2')
output_data['HI bank\'s assets'] = output_data.pop('1.1.3')
output_data['% lending NFPS by res MFIs'] = output_data.pop('1.1.4')

output_data['CET1 ratio'] = output_data.pop('1.3.1')
output_data['RoE'] = output_data.pop('1.3.7')
output_data['Cost income ratio'] = output_data.pop('1.3.8')

output_data['Cred to gov / tot assets'] = output_data.pop('1.4.1')
output_data['Pub sec indebtness'] = output_data.pop('1.4.3')

output_data['% lending NFPS by non-res'] = output_data.pop('3.2.2')


# In[7]:


# Save the data on the disk
def save_all_input_data():
    filename = '../data/renamed_output_data'
    outfile = open(filename,'wb')
    pickle.dump(output_data,outfile)
    outfile.close()


# In[8]:


save_all_input_data()


# In[ ]:




