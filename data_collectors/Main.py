#!/usr/bin/env python
# coding: utf-8

# In[25]:


# 'Helps' with the autocompletion of Java variables within Jupyter
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[1]:


import sys
print(sys.executable)


# In[2]:


import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd # 0.23.0
import requests     # 2.18.4


# In[3]:


# Series
# (i = country)

# 1.1.1 Size of banking sector
# (A) CBD2.Q.i.W0.67._Z._Z.A.A.A0000._X.ALL.CA._Z.LE._T.EUR # since 2014 Q4
# (B) MNA.Q.Y.i.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N # since 2014 Q4 (solo CY-ES-I6-I7-I8)

# 1.1.2 CR5
# SSI.A.i.122C.S10.X.U6.Z0Z.Z 

# 1.1.3 HHI Herfindahl Index of banks’ assets
# SSI.A.i.122C.H10.X.U6.Z0Z.Z

# 1.1.4 Share of lending to the domestic NFPS by resident MFIs
# (A) QSA.Q.N.i.W2.S12K.S11.N.A.LE.F4.S._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (B) QSA.Q.N.i.W2.S12K.S1M.N.A.LE.F4.S._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (C) QSA.Q.N.i.W2.S12K.S11.N.A.LE.F4.L._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (D) QSA.Q.N.i.W2.S12K.S1M.N.A.LE.F4.L._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (E) QSA.Q.N.i.W0.S11.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (F) QSA.Q.N.i.W0.S1M.S1.N.L.LE.F4.S._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (G) QSA.Q.N.i.W0.S11.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T (preso da Q1 2000)
# (H) QSA.Q.N.i.W0.S1M.S1.N.L.LE.F4.L._Z.XDC._T.S.V.N._T (preso da Q1 2000)


# In[201]:


# Building blocks for the URL
entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' # Using protocol 'https'
resource = 'data'           # The resource for data queries is always'data'
flowRef ='SSI'              # Dataflow describing the data that needs to be returned, exchange rates in this case
key = 'A..122C.H10.X.U6.Z0Z.Z'    # Defining the dimension values, explained below

# Define the parameters
parameters = {
    'startPeriod': '2000-01-01',  # Start date of the time series
    'endPeriod': '2100-10-01'     # End of the time series
}


# In[202]:


# Construct the URL: https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.CHF.EUR.SP00.A
request_url = entrypoint + resource + '/'+ flowRef + '/' + key

# Make the HTTP request
response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})

# Check if the response returns succesfully with response code 200
print(response)

# Print the full URL
print(response.url)


# In[203]:


#my_data = np.genfromtxt(io.StringIO(response.text), delimiter=',')

df = pd.read_csv(io.StringIO(response.text))


# In[204]:


df.info()


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




