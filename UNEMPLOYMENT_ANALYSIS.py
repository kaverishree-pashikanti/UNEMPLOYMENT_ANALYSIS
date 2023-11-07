#!/usr/bin/env python
# coding: utf-8

# # Unemployment Analysis in India - covid 19 pandamic

# In[1]:


# importing important libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import calendar
import plotly.graph_objects as go
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df=pd.read_csv('Unemployment_Rate_upto_11_2020.csv')
df


# In[3]:


df.info()


# In[4]:


df.columns=['state','date','frequency','estimated unemployment rate','estimated employed','estimated labour participation rate','region','longitude','latitude']


# In[5]:


df.columns


# In[6]:


df.describe()


# In[7]:


df.isnull().sum()


# In[8]:


df.state.value_counts()


# In[9]:


# changing the datatype of 'data' from object to datetime
df['date']=pd.to_datetime(df['date'],dayfirst=True)
df.info()


# In[10]:


# Extracting month from date attribute
df['month_int']=df['date'].dt.month
df


# In[11]:


# The months are in integer datetype. We need to convert the months into words for better analysis
df['month']=df['month_int'].apply(lambda x: calendar.month_abbr[x])
df


# In[12]:


# Numeric data grouped by months
data=df.groupby(['month'])[['estimated unemployment rate','estimated employed','estimated labour participation rate']].mean()
data=pd.DataFrame(data).reset_index()


# In[13]:


# Bar plot of umemployment rate and labour participation rate
month=data.month
unemployment_rate=data['estimated unemployment rate']
labour_participation_rate=data['estimated labour participation rate']

fig=go.Figure()

fig.add_trace(go.Bar(x=month,y=unemployment_rate,name='Unemployment Rate'))
fig.add_trace(go.Bar(x=month,y=labour_participation_rate,name='Labour Participation Rate'))

fig.update_layout(title='Unemployment Rate and Labour Participation Rate',xaxis={'categoryorder':'array','categoryarray':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct']})
fig.show()


# In[14]:


import plotly.express as px


# In[15]:


fig=px.bar(data,x='month',y='estimated employed',color='month',category_orders={'month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct']},title='Estimated employed people from Jan 2020 to Oct 2020')
fig.show()


# In[16]:


# now comes state wise analysis
state=df.groupby(['state'])[['estimated unemployment rate','estimated employed','estimated labour participation rate']].mean()
state=pd.DataFrame(state).reset_index()


# In[17]:


# box plot
fig=px.box(data_frame=df,x='state',y='estimated unemployment rate',color='state',title='Unemployment rate')
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# In[18]:


# average unemployment rate bar plot
fig=px.bar(state,x='state',y='estimated unemployment rate',color='state',title='Average unemployment rate (statewise)')
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# The highest average amount of Unemployment rate is shown in Haryana and Jharkhand
# 
# Meghalaya was having the lowest average amount of Unemployment rate

# In[19]:


fig = px.bar(df,x='state',y='estimated unemployment rate',animation_frame='month',color='state',
            title='Unemployment rate from Jan 2020 to Oct 2020(StateWise)')

fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# from this graph we able to check the unemployment rate of every state by month 

# In[20]:


fig=px.scatter_geo(df,'longitude','latitude',color='state',
                  hover_name='state',size='estimated unemployment rate',
                  animation_frame='month',scope='asia',title='Impact of lockdown on employment in India')

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] =2000
fig.update_geos(lataxis_range=[5,40],lonaxis_range=[65,100],oceancolor='lightblue',
               showocean=True)

fig.show()


# In[21]:


df.region.unique()


# In[22]:


# numeric data grouped by region

region = df.groupby(['region'])[['estimated unemployment rate','estimated employed','estimated labour participation rate']].mean()
region = pd.DataFrame(region).reset_index()


# In[23]:


#Scatter plot

fig= px.scatter_matrix(df,dimensions=['estimated unemployment rate','estimated employed','estimated labour participation rate'],color='region')
fig.show()


# In[24]:


# Average Unemployment Rate

fig = px.bar(region,x='region',y='estimated unemployment rate',color='region',title='Average unemployment rate(regionwise)')
fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.show()


# In[25]:


fig = px.bar(df,x='region',y='estimated unemployment rate',animation_frame='month',color='state',
            title='Unemployment rate from Jan 2020 to Oct 2020')

fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] =2000

fig.show()


# In[26]:


unemployment =df.groupby(['region','state'])['estimated unemployment rate'].mean().reset_index()
unemployment.head()


# In[27]:


fig = px.sunburst(unemployment,path=['region','state'],values='estimated unemployment rate',
                 title ='Unemployment rate in state and region',height=600)
fig.show()


# In[28]:


# data representation before and after lockdown

before_lockdown = df[(df['month_int']>=1) &(df['month_int'] <4)]
after_lockdown = df[(df['month_int'] >=4) & (df['month_int'] <=6)]


# In[29]:


af_lockdown = after_lockdown.groupby('state')['estimated unemployment rate'].mean().reset_index()

lockdown = before_lockdown.groupby('state')['estimated unemployment rate'].mean().reset_index()
lockdown['unemployment rate before lockdown'] = af_lockdown['estimated unemployment rate']

lockdown.columns = ['state','unemployment rate before lockdown','unemployment rate after lockdown']
lockdown.head()


# In[30]:


# unenployment rate change after lockdown

lockdown['rate change in unemployment'] =round(lockdown['unemployment rate before lockdown']-lockdown['unemployment rate before lockdown']
                                              /lockdown['unemployment rate after lockdown'],2)
fig = px.bar(lockdown,x='state',y='rate change in unemployment',color='rate change in unemployment',
            title='Percentage change in Unemployment rate in each state after lockdown',template='ggplot2')
fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.show()


# In[ ]:




