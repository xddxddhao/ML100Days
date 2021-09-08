#!/usr/bin/env python
# coding: utf-8

# In[40]:


import pandas as pd
import numpy as np
import talib
import datetime

import math
import statistics
import matplotlib.pyplot as plt
import zipfile
from datetime import datetime
from scipy import stats
import seaborn as sns

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


plt.style.use('ggplot')


# In[41]:


data1 = pd.read_csv("TXF 2010-2020 1min.txt")


# In[42]:


data1["Datetime"] = pd.to_datetime(data1["Datetime"])
data1.sort_values(by = "Datetime", inplace = True, ascending = True)
data1


# In[43]:


data1 = data1.set_index(data1.Datetime).drop(columns = {"Datetime"})
data1


# In[44]:


data1 = data1.resample("60T", label = "right", closed = "right", offset = "9h45min").agg(dict(zip(data1.columns,["first", "max", "min", "last", "sum"])))

data1= data1[data1["Close"].isna()==False].copy()
data1

data1['Hour'] = data1.index.map(lambda x: x.hour)


# In[45]:


Morning = data1[(data1.Hour >= 8) & (data1.Hour <= 13)]
data1["MA20"] = data1["Close"].rolling(20).mean()


# In[46]:


fast = data1['Close'].ewm(span=12, adjust=False, min_periods=12).mean()

slow = data1['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
MACD = fast-slow
data1['macd']=data1.index.map(MACD)
data1.head(50)


# In[47]:



data1["shift"] = data1["macd"].shift(1)
data1.head(50)


# In[48]:


buy_signal = (data1["macd"] > 0) &(data1["macd"].shift() <0 )
sellshort_signal = (data1["macd"] < 0) &(data1["macd"].shift() >0)
buy_filter1 = data1["macd"] >data1["shift"]
buy_filter2 = data1['High'] > data1["MA20"]
sell_filter1 = data1["macd"] <data1["shift"]
sell_filter2  = data1['High'] < data1["MA20"]
condition = [buy_signal & buy_filter1 & buy_filter2, sellshort_signal &sell_filter1 & sell_filter2 ]
choice = [1, -1]
data1["Signal_"] = np.select(condition, choice, default = 0)
data1.head(50)


# In[49]:


fig, (ax1, ax2) = plt.subplots(2, figsize = (15,5))
ax1.plot(data1.Close.dropna(), color = '#01889f', alpha = 0.5, label = 'TFX close price')
ax2.plot(data1.Signal_, alpha = 0.5, label = 'macd signal')
fig.legend()


# In[ ]:





# In[ ]:




