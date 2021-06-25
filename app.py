import datetime
from pandas.core.indexes.datetimes import date_range
import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd 
import yfinance as yf
import sys
from dash.dependencies import Input, Output


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#14274E' ,
    'text': '#F1F6F9'
}

#################(VISUALS)

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2020, 1, 1)
dataset = yf.download('VOO',start=start,end=end, interval='1d')

yfDataframe = pd.DataFrame(dataset)

price_data = yfDataframe["Adj Close"]
price_data = price_data.iloc[1:]
daily_pricedelta = price_data.pct_change()*100 #daily % change *100= raw delta 
daily_pricedelta = daily_pricedelta.iloc[1:]
interpretation_data = pd.read_csv("training_data.csv") #read in the csv file of interp. data. 
interpretation_data.index = interpretation_data['date']
interpretation_data = interpretation_data.drop('date', axis=1)
interpretation_data = interpretation_data.iloc[2:]

def adding_pdelta():
  #Input: daily_pricedelta and training file w/epsilon greedy
  #Returns: training file w/ a column added for daily price delta
  #Hint: setting the Date to an index and converting it to DateTime dtype will make your life easier, also you'll need to drop the nan date
  global interpretation_data
  interpretation_data = interpretation_data.join(price_data, how='inner')
  interpretation_data['delta'] = 0
  interpretation_data['delta'] = daily_pricedelta
  return interpretation_data

adding_pdelta()


# graphData = pd.DataFrame(interpretation_data)
# btwn = graphData['delta'].between(0, .25, inclusive=True)

# df = graphData[btwn]
# fig = px.line(df, x=df.index, y=df["Adj Close"])


# def SetColor(x): 
#     if(x == 1):
#         return 'green'
#     elif(x == 0):
#         return 'yellow'
#     elif(x == 2):
#         return 'red'

# fig.update_traces(go.Scatter(
#                 marker = dict(color=list(map(SetColor, interpretation_data['choice']))),
#                 mode ='markers+lines'), )
# fig.update_layout(
#     title="Action for Specified Delta",
#     xaxis_title="Trading Days", 
#     yaxis_title="Price USD"
# )
# fig.update_layout(showlegend=True)


df = interpretation_data
fig = px.line(df, x=df.index, y='Adj Close', title='Price Over Time')



app.layout = dbc.Container (style={'backgroundColor': colors['background']}, children=    [

    html.H1(
        children='RL Trading Algorithm Dashboard',
        style={
            'textAlign': 'center', 
            'color': colors['text']
        }
    ),

    html.Hr(), 

    dcc.DatePickerRange(
        id='date-picker-range', 
        min_date_allowed = date_range(2000, 1, 1), 
        max_date_allowed = date_range(2021, 1, 1), 
    ),

    dcc.Tabs([
        dcc.Tab(label='Tab One', children = [
            dcc.Graph(
                figure = fig
            )

        ]), 
        
        dcc.Tab(label='Tab Two', children = [

        ]),

        dcc.Tab(label='Tab Three', children = [

        ])



    ])




    

])
 

if __name__ == '__main__': 
    app.run_server(port =4500)



