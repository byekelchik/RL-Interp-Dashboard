#import all libraries and packages
# !pip install yfinance
# !pip install --upgrade google-cloud-bigquery
# !pip install pandas-gbq -U
from google.cloud import bigquery
import pandas_gbq
import yfinance as yf
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import sys
import datetime as dt
import os
import numpy as np

#GET THE DATA
start = dt.datetime(2018, 1, 1)
end = dt.datetime(2019, 1, 1)
dataset = yf.download('VOO',start=start,end=end,
                      interval='1d')

# authorize google cloud connection
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/content/drive/MyDrive/Mountaintop2021/Google BQ Security/irlts-317602-7ed706ba79a2.json'
# INPUT: SQL query string
# OUTPUT: DataFrame holding returned query data

queryResult = pd.DataFrame() 

def get_data(requested_query):

  global queryResult
  # resize data to match size from trading algorithm
  yfDataframe = pd.DataFrame(dataset)
  validation_size = 0.2
  train_size = int(len(yfDataframe) * (1-validation_size))
  yfDataframe = yfDataframe[0:train_size]
  yfDataframe = yfDataframe.iloc[1:]

  # ADJ CLOSE DATA
  price_data = yfDataframe["Adj Close"]
  
  # PRICE DELTA DATA
  daily_pricedelta = price_data.pct_change() * 100 # daily % change * 100 = raw delta 
  daily_pricedelta = daily_pricedelta.iloc[1:]
  price_data = price_data.iloc[1:]

  # VOLUME DELTA DATA
  volume_data = yfDataframe["Volume"]
  daily_volumedelta = volume_data.pct_change()*100 # daily % change * 100 = raw delta 
  daily_volumedelta = daily_volumedelta.iloc[1:]

  # connect to BigQuery table and execute query
  project_id = 'irlts-317602'
  queryResult = pandas_gbq.read_gbq(requested_query, project_id=project_id, progress_bar_type=None) # do not filter query by choice

  # reformat 'Date' to datetime
  queryResult = queryResult.iloc[4:] 
  queryResult['Date'] = pd.to_datetime(queryResult['Date'], errors='coerce')
  

  # join all data
  queryResult = queryResult.join(daily_pricedelta, on='Date', how='inner')
  queryResult = queryResult.join(daily_volumedelta, on='Date', how='inner')
  queryResult.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta']
  queryResult = queryResult.join(price_data, on='Date', how='inner')
  queryResult.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close']

  return queryResult
# print(get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '1' order by date limit 10"))
