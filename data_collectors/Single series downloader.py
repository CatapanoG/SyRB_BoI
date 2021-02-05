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
import pickle
import requests     # 2.18.4


# In[4]:


# Series
# (.. = country)

all_queries = {

# 1.1.1 Size of banking sector
# (A) CBD2.Q.i.W0.67._Z._Z.A.A.A0000._X.ALL.CA._Z.LE._T.EUR # since 2014 Q4
# (B) MNA.Q.Y.i.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N # since 2014 Q4 (solo CY-ES-I6-I7-I8)

# 1.1.2 CR5
'1.1.2': 'SSI.A..122C.S10.X.U6.Z0Z.Z', 

# 1.1.3 HHI Herfindahl Index of banks’ assets
'1.1.3': 'SSI.A..122C.H10.X.U6.Z0Z.Z',
    
# 1.1.4 Share of lending to the domestic NFPS by resident MFIs
'1.1.4.A': 'QSA.Q.N..W2.S12K.S11.N.A.LE.F4.S._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.B': 'QSA.Q.N..W2.S12K.S1M.N.A.LE.F4.S._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.C': 'QSA.Q.N..W2.S12K.S11.N.A.LE.F4.L._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.D': 'QSA.Q.N..W2.S12K.S1M.N.A.LE.F4.L._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.E': 'QSA.Q.N..W0.S11.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.F': 'QSA.Q.N..W0.S1M.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.G': 'QSA.Q.N..W0.S11.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
'1.1.4.H': 'QSA.Q.N..W0.S1M.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T', # (preso da Q1 2000)
   
# 1.3.1 CET1 ratio
'1.3.1': 'CBD2.Q..W0.67._Z._Z.A.A.I4008._Z._Z._Z._Z._Z._Z.PC',
    
# 1.4.1 Credit to general governments, as share of total assets
'1.4.1.A': 'BSI.M..N.A.A30.A.1.U6.2100.Z01.E',
'1.4.1.B': 'BSI.M..N.A.A20.A.1.U6.2100.Z01.E',
'1.4.1.C': 'BSI.M..N.A.T00.A.1.Z5.0000.Z01.E',
    
# 1.4.3 Public sector indebtedness
'1.4.3': 'GFS.Q.N..W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ_CY._T.F.V.N._T',
    
# 3.2.2 Share of lending to NFPS by non-residents
'3.2.2.A': 'QSA.Q.N..W2.S1.S11.N.A.LE.F4.S._Z.XDC._T.S.V.N._T',
'3.2.2.B': 'QSA.Q.N..W2.S1.S1M.N.A.LE.F4.S._Z.XDC._T.S.V.N._T',
'3.2.2.C': 'QSA.Q.N..W2.S1.S11.N.A.LE.F4.L._Z.XDC._T.S.V.N._T',
'3.2.2.D': 'QSA.Q.N..W2.S1.S1M.N.A.LE.F4.L._Z.XDC._T.S.V.N._T',
'3.2.2.E': 'QSA.Q.N..W0.S11.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T',
'3.2.2.F': 'QSA.Q.N..W0.S1M.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T',
'3.2.2.G': 'QSA.Q.N..W0.S11.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T',
'3.2.2.H': 'QSA.Q.N..W0.S1M.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T'
    
}

dfs = {}


# In[10]:


# MAke the HTTP request 
def fetch_series(_key):
    # Building blocks for the URL
    entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' # Using protocol 'https'
    resource = 'data'           # The resource for data queries is always'data'
    
    flow_name, key_position = get_flow_name(_key) # Dataflow describing the data that needs to be returned, exchange rates in this case
    key = _key[key_position:]    # Defining the dimension values, explained below
    
    # Define the parameters
    parameters = {
        'startPeriod': '2000-01-01',  # Start date of the time series
        'endPeriod': '2100-10-01'     # End of the time series
    }
    
    # Construct the URL, eg: https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.CHF.EUR.SP00.A
    request_url = entrypoint + resource + '/'+ flow_name + '/' + key

    # Make the HTTP request
    response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})

    # Check if the response returns succesfully with response code 200
    print(response)
    
    # Print the full URL
    print(response.url)
    
    # Pandas df conversion
    return pd.read_csv(io.StringIO(response.text))

# Filter for the useful data
def filter_series(_df):
    
    # Filter relevant columns
    return _df.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE', 'FREQ'], axis=1)

# Convert data types to int (of the type: 20201130)
def convert_data_types(_df):
    # Helper used to adjust quarterly data
    def quarters(x):
        new_date = int(x[0:4]) * 100
        if 'Q1' in x:
            new_date += 3
        elif 'Q2' in x:
            new_date += 6
        elif 'Q3' in x:
            new_date += 9
        elif 'Q4' in x:
            new_date += 12
        return new_date
    # Helper used to adjust monthly data
    def months(x):
        new_date = int(x[0:4]) * 100 + int(x[5:7])
        return new_date

    time_freq = _df['FREQ'][0]
    if time_freq == 'A':
        _df['TIME_PERIOD'] = _df['TIME_PERIOD'] * 100 + 12
    elif time_freq == 'Q':
        _df['TIME_PERIOD'] = _df['TIME_PERIOD'].map(quarters)
    elif time_freq == 'M':
        _df['TIME_PERIOD'] = _df['TIME_PERIOD'].map(months)

# Get the data flow name from the query string
def get_flow_name(query_string):
    flow_name = ""
    end_position = 0
    
    for char in query_string:
        end_position += 1
        if char != '.':
            flow_name += char
        else:
            break
            
    return flow_name, end_position

# Execute all queries and store the results in 'dfs'
def get_all_input_data():
    for entry in all_queries:
        print('Indicator: ' + entry)
        print('Series: ' + all_queries[entry])

        # Fetch series from ECB
        dfs[entry] = fetch_series(all_queries[entry])

        # Filter columns
        dfs[entry] = filter_series(dfs[entry])
        
        # Convert data types
        convert_data_types(dfs[entry])

        print('\n')

# Save the data on the disk ('../data/input_data')
def save_all_input_data():
    filename = '../data/input_data'
    outfile = open(filename,'wb')
    pickle.dump(dfs,outfile)
    outfile.close()


# In[11]:


get_all_input_data()
save_all_input_data()


# In[31]:





# In[ ]:


# OLD STUFF FOLLOWS


# In[12]:


dfs


# In[205]:


df.tail()


# In[206]:


# change
df_filtered = df.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)

countries = df.REF_AREA.unique()
print(countries)

# change
data = []

for country in countries:
    # change, change
    ts = df_filtered.loc[(df_filtered['REF_AREA'] == country)].to_numpy()
    # change
    data.append(ts)
    
# change, change
data = np.asarray(data)
    
# change
for ts in data:
    if(ts[0,1] == 'IT' or ts[0,1] == 'DE' or ts[0,1] == 'FR'):
        plt.plot(ts[:,0],ts[:,2],label=ts[0,1])

plt.legend()


# In[166]:


#data


# In[207]:


# file name
name = '113'

# save csv
df_filtered.to_csv('data/' + name + '.csv',index=False)

# save numpy
np.save('data/' + name + '.npy', data, allow_pickle=True)


# In[208]:


test = np.load('data/' + name + '.npy', allow_pickle=True)

test


# In[43]:


# Create a new DataFrame called 'ts'
ts = df.filter(['TIME_PERIOD', 'REF_AREA', 'OBS_VALUE'], axis=1)
# 'TIME_PERIOD' was of type 'object' (as seen in df.info). Convert it to datetime first
#ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])
# Set 'TIME_PERIOD' to be the index
#ts = ts.set_index('TIME_PERIOD')
# Print the last 5 rows to screen
ts.tail()


# In[20]:


# Convert to numpy
np_ts = ts.to_numpy()


# In[21]:


np_ts


# In[76]:





# In[78]:




plt.plot(np_ts_ITA[:,0], np_ts_ITA[:,1], label='CR5 ITA')
plt.plot(np_ts_DE[:,0], np_ts_DE[:,1], label='CR5 DEU')
plt.legend()


# In[ ]:




