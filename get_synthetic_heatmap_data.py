# Import libraries and packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
from Visualization import colors
from Visualization import structure_data as sd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
# import numpy as np


def heatmap(data):
    i, j = 0, 0
    x, y, columns = [], [], []
    output = []
    df = data

    # get max and min values
    price_min, price_max = min(df['Price Delta']), max(df['Price Delta'])
    volume_min, volume_max = min(df['Volume Delta']), max(df['Volume Delta'])

    # create bins with distribution as close to normal as possible
    x = pd.cut(df['Price Delta'], retbins=True, bins=pd.interval_range(start=price_min, end=price_max, periods = 20))
    y = pd.cut(df['Volume Delta'], retbins=True, bins=pd.interval_range(start=volume_min, end=volume_max, periods = 20))

    # convert intervalindex to tuple for looping
    x = x[1].to_tuples()
    y = y[1].to_tuples()

    # fill df with zeros to initialize 
    new_df = pd.DataFrame(np.zeros(((len(y)-1, len(x)-1))))
    empty_df = pd.DataFrame()
    # iterate through entire df and replace with action for the given price/volume delta
    k=0
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            values = df['Choice'][(df['Price Delta'].astype(float).between(x[i-1][0], x[i][0], inclusive = True)) & (df['Volume Delta'].astype(float).between(y[j-1][0], y[j][0], inclusive = True))]
            new_df[i-1][j-1] = values.median() if len(values) > 0 else -2
            if len(values) <= 0:
                empty_df.loc[k, 'Price Delta'] = x[i-1][0]
                empty_df.loc[k, 'Volume Delta'] = y[j-1][0]
                empty_df.loc[k, 'adj close'] = 100*(1+(float(x[i-1][0])/100))
                k+=1
    std_scaler = StandardScaler()
    empty_df[['empty_price_scaled','empty_volume_scaled']] = std_scaler.fit_transform(empty_df[['Price Delta', 'Volume Delta']])
    print(empty_df)
    empty_df.to_csv(path_or_buf="jupyter/2017/saved_models/99gamma_default/empty_df_99gamma_default.csv", index=False)
    # create heatmap and return it
    fig = go.Figure(go.Heatmap(z=new_df, x=x[1], y=y[1], colorscale=colors.get_colorscale()))
    
    fig.update_layout(
        title="Price v Volume Heatmap",
        xaxis_title="Price Delta",
        yaxis_title="Volume Delta",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )

    return output

import warnings
import datetime as dt
import yfinance as yf
import pandas_gbq

warnings.simplefilter(action='ignore', category=FutureWarning)
# INPUT: SQL query string
# OUTPUT: DataFrame holding returned query data
def get_data(dataset_name, table_name):
    """Queries BigQuery table and structures the data for the visuals"""

    # adjust data based on passed parameters
    if dataset_name == '2018':
        #GET THE DATA
        start = dt.datetime(2018, 1, 1)
        end = dt.datetime(2019, 1, 1)
    elif dataset_name == '2017': # '2017'
        #GET THE DATA
        start = dt.datetime(2017, 10, 18)
        end = dt.datetime(2018, 1, 1)
    else: # 'covid'
        #GET THE DATA
        start = dt.datetime(2019, 1, 1)
        end = dt.datetime(2020, 1, 1)

    if table_name == 'Training':
        requested_query = "select * from `irlts-317602."+str(dataset_name)+"."+str(table_name)+"` order by episode, date"
    else: # 'Testing'
        requested_query = "select * from `irlts-317602."+str(dataset_name)+"."+str(table_name)+"` order by date"

    # resize data to match size from trading algorithm
    dataset = yf.download('VOO',start=start,end=end, interval='1d')
    yf_dataframe = pd.DataFrame(dataset)
    validation_size = 0.2
    train_size = int(len(yf_dataframe) * (1-validation_size))
    yf_dataframe = yf_dataframe[0:train_size]
    yf_dataframe = yf_dataframe.iloc[1:]

    # ADJ CLOSE DATA
    price_data = yf_dataframe["Adj Close"]

    # PRICE DELTA DATA
    daily_pricedelta = price_data.pct_change() * 100 # daily % change * 100 = raw delta
    daily_pricedelta = daily_pricedelta.iloc[1:]
    price_data = price_data.iloc[1:]

    # VOLUME DELTA DATA
    volume_data = yf_dataframe["Volume"]
    daily_volumedelta = volume_data.pct_change()*100 # daily % change * 100 = raw delta
    daily_volumedelta = daily_volumedelta.iloc[1:]

    # connect to BigQuery table and execute query
    project_id = 'irlts-317602'
    query_result = pandas_gbq.read_gbq(requested_query, project_id=project_id, progress_bar_type=None) # do not filter query by choice

    # reformat 'Date' to datetime
    query_result = query_result.iloc[4:]
    query_result['Date'] = pd.to_datetime(query_result['Date'], errors='coerce')

    
    # join all data
    
    query_result = query_result.join(daily_pricedelta, on='Date', how='inner')
    query_result = query_result.join(daily_volumedelta, on='Date', how='inner')
    
    if table_name == 'Training':
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta']
    else:
        
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Price Delta', 'Volume Delta']
        
    query_result = query_result.join(price_data, on='Date', how='inner')
    if table_name == 'Training':
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close']
    else:
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Price Delta', 'Volume Delta', 'Adj Close']

    return query_result

heatmap(get_data('2017', '99gamma_default'))



