'''Gets and structures data'''
import warnings
import datetime as dt
import yfinance as yf
import pandas as pd
import pandas_gbq

warnings.simplefilter(action='ignore', category=FutureWarning)

# For Google Colab:
# authorize google cloud connection
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/content/drive/MyDrive/Mountaintop2021/Google BQ Security/irlts-317602-7ed706ba79a2.json'


# INPUT: SQL query string
# OUTPUT: DataFrame holding returned query data
def get_data(dataset_name, train_test):
    """Queries BigQuery table and structures the data for the visuals"""

    if dataset_name == '2018':
        #GET THE DATA
        start = dt.datetime(2018, 1, 1)
        end = dt.datetime(2019, 1, 1)

    else:
        #GET THE DATA
        start = dt.datetime(2019, 1, 1)
        end = dt.datetime(2020, 1, 1)

    if train_test == 'Training':
        requested_query = "select * from `irlts-317602."+str(train_test)+".10eps_"+dataset_name+"` order by episode, date"
    else:
        requested_query = "select * from `irlts-317602."+str(train_test)+".10eps_"+dataset_name+"` order by date"

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
    if train_test == 'Training':
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta']
    else:
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Price Delta', 'Volume Delta']
    query_result = query_result.join(price_data, on='Date', how='inner')
    if train_test == 'Training':
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close']
    else:
        query_result.columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Price Delta', 'Volume Delta', 'Adj Close']


    return query_result
