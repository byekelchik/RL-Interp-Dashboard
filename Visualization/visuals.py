#Import libraries and packages
# !pip install yfinance
# !pip install --upgrade google-cloud-bigquery
# !pip install pandas-gbq -U
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
import app

# import structure_data
# from structure_data import get_data, sys, os, pd

# Visualizations
  # Parameters:
  # 1.   Episodes
  # 2.   Dataset name(COVID, 2018)
  # 3.   Train or Test data

def price_v_volume(episodes, dataset_name, data): # compare two datasets at a time

  output = []
  df = data
  for episode in episodes:
    df = df[df['Episode'] == str(episode)]
    colorsIdx = {'0': 'Hold', '1': 'Buy',
                '2': 'Sell'}
    cols      = df['Choice'].map(colorsIdx)
    fig = px.scatter(df, x="Price Delta", y="Volume Delta", color=cols)

    
    fig.update_layout(
    title="Episode "+str(episode)+": B/S/H for Price/Volume Delta",
    xaxis_title="Price Delta",
    yaxis_title="Volume Delta",
    legend_title_text='Action'
    )

    output.append(fig)
    df = data
  return output
  
# INPUT: 2 episodes to compare
def two_way_table(episodes, df): # compare two datasets at a time
  df = df
  twt_dataframe = pd.DataFrame([[0, 0, 0], [0, 0, 0], [0, 0, 0]], columns=['Hold', 'Buy', 'Sell'], index=['Hold', 'Buy', 'Sell'])
  total = 0
  # split data into a df/episode
  ep_one = df[df['Episode'] == str(episodes[0])]
  ep_two = df[df['Episode'] == str(episodes[1])]
  
  # add overlapping values between two dfs to final table df
  for c_x, v_x in enumerate(['Hold', 'Buy', 'Sell']):
    for c_y, v_y in enumerate(['Hold', 'Buy', 'Sell']):
        temp = pd.merge(ep_one[['Date', 'Choice']][ep_one['Choice'] == str(c_x)], ep_two[['Date', 'Choice']][ep_two['Choice']== str(c_y)], on='Date', how='inner')
        twt_dataframe[v_x].iloc[c_y] = len(temp.index)
        total += len(temp.index)
  #Heatmap version        
  # fig = px.imshow(twt_dataframe, labels=dict(x="Episode "+str(episodes[0]), y="Episode "+str(episodes[1]), color="Overlap"), color_continuous_scale=px.colors.sequential.Viridis)
  # fig.update_xaxes(side="top")
  fig = go.Figure(data=[go.Table(header=dict(height = 38, values=['', 'Hold', 'Buy', 'Sell'], fill_color='paleturquoise'),
               cells=dict(height = 25, values=[twt_dataframe.index, twt_dataframe.Hold, twt_dataframe.Buy, twt_dataframe.Sell], fill_color='cornsilk'))
                   ])
  fig.update_layout(
  title="Two-way Table: Episode " + str(episodes[0]) + ' x ' + "Episode " + str(episodes[1])
  )
  return fig

# Average state(Price, Volume) table
# INPUT: specific episodes, name of dataset being used(COVID, 2018), train or test data
def average_state_table(episodes, dataset_name, data):

  df = data

  fig_output = []
  
  for episode in episodes:
    # restrcuture data by choice and episode
    buy = df[(df['Choice'] == '1') & (df['Episode'] == str(episode))]
    sell = df[(df['Choice'] == '2') & (df['Episode'] == str(episode))]
    hold = df[(df['Choice'] == '0') & (df['Episode'] == str(episode))]
    bsh = pd.concat([buy.median().round(2).astype(str) + '%', sell.median().round(2).astype(str) + '%', hold.median().round(2).astype(str) + '%'])

    # create plotly table
    fig = go.Figure(data=[go.Table(columnwidth = 1,
      header=dict(height = 38, values=['Action', 'Price Delta', 'Volume Delta'],
                  fill_color='paleturquoise',
                  align='left'),
      cells=dict(height = 25, values=[['Buy', 'Sell', 'Hold'], bsh['Price Delta'], bsh['Volume Delta']],
                fill_color='cornsilk',
                align='left'))
    ])

    fig.update_layout(
    title="Episode "+str(episode),
    height=300
    )

    # add to output list to send to dash
    fig_output.append(fig)
    
  return fig_output

def testing_average_state_table(dataset_name, data):

  df = data
  
  # restrcuture data by choice and episode
  buy = df[df['Choice'] == '1']
  sell = df[df['Choice'] == '2']
  hold = df[df['Choice'] == '0']
  hold = hold.append(pd.Series(0, index=df.columns), ignore_index=True) # REMOVE
  bsh = pd.concat([buy.median().round(2).astype(str) + '%', sell.median().round(2).astype(str) + '%', hold.median().round(2).astype(str) + '%'])

  # create plotly table
  fig = go.Figure(data=[go.Table(columnwidth = 1,
    header=dict(height = 38, values=['Action', 'Price Delta', 'Volume Delta'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(height = 25, values=[['Buy', 'Sell', 'Hold'], bsh['Price Delta'], bsh['Volume Delta']],
              fill_color='cornsilk',
              align='left'))
  ])

  fig.update_layout(
  title="Average State",
  height=300
  )
  
  return fig

# Average state(Price, Volume) graph
# INPUT: specific episodes, name of dataset being used(COVID, 2018)
def average_price_graph(episodes, dataset_name, data):

  fig_output = []
  df = data

  buy = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  sell = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  hold = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  
  
  for episode in episodes:
    buy = buy.append(df[(df['Choice'] == '1') & (df['Episode'] == str(episode))].median(), ignore_index=True)
    sell = sell.append(df[(df['Choice'] == '2') & (df['Episode'] == str(episode))].median(), ignore_index=True)
    hold = hold.append(df[(df['Choice'] == '0') & (df['Episode'] == str(episode))].median(), ignore_index=True)

  # plot a line for the specified number of episodes
  for state in ['Price', 'Volume']:
    fig = go.Figure(layout=go.Layout(
          title=go.layout.Title(text="Average Price State by Episode")
      ))
    fig.add_trace(go.Scatter(x=episodes, y=buy[state+' Delta'],
                      mode='lines+markers',
                      name='Buy'))
    fig.add_trace(go.Scatter(x=episodes, y=sell[state+' Delta'],
                    mode='lines+markers',
                    name='Sell'))
    fig.add_trace(go.Scatter(x=episodes, y=hold[state+' Delta'],
                    mode='lines+markers',
                    name='Hold'))
    fig.update_layout(
    title="Average "+state+" Delta by Episode",
    xaxis_title="Episode",
    yaxis_title="% Change"
    )
    fig_output.append(fig)
    
  return fig_output

# Helper function for heatmap visual
def SetColor(x):
    if(x == 1):
        return "green"
    elif(x == 0):
        return "yellow"
    elif(x == 2):
        return "red"

# INPUT: lower and upper delta values, name of dataset, train or test dataset
def heatmap_visual(lower, upper, episode):

  graphData = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by episode, date")
  btwn = graphData['Price Delta'].between(lower, upper, inclusive = True)
  df = graphData[btwn]

  fig = go.Figure()

  # graph data for days with delta between inputted values

  fig.add_trace(go.Scatter(x=df["Date"], y=df["Adj Close"],
                    mode='lines+markers'))

  # overlay markers for B/S/H
  fig.update_traces(go.Scatter( 
                    marker = dict(color=list(map(SetColor, graphData['Choice'].astype(int)))),
                    mode='markers+lines'))
  

  fig.update_layout(
    title="Action for Specified Delta",
    xaxis_title="Trading Days",
    yaxis_title="Price USD"
  )
  

  fig.show()

# def bar_chart():
  #input: same as Heatmap_visual, interval user wants to understand
  #output: bar chart of action on a given internval if interval given, else bar chart of action for entire trading window

def price(episode):
  #price_data
  #output: show the user the price overtime
  df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")
  fig = px.line(df, x=df.index, y="Adj Close", title='Price Over Time')
  fig.show()

def randon_action_plot(episode):
  queryResult = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")

  #output: visual of the amount of random actions in a certain episode compared to real values
  ep_greedy = queryResult[queryResult['Hold']==str(-1)] #get the days when we dont go greedy
  ep_greedy_days = ep_greedy.shape[0] #get the shape of df and take the first value of list
  non_greedy_days = queryResult.shape[0] - ep_greedy_days #subtract greedy days from total trading horizon
  pct_greedy = (ep_greedy_days)/queryResult.shape[0]
  pct_non_greedy = 1-pct_greedy

  ###now plot pct_greedy and pct_non_greedy
  labels = ['Greedy', 'Non-Greedy']
  values = [ep_greedy_days, non_greedy_days]

  fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

  # enhance visual
  colors = ['lightcyan', 'royalblue']
  fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
  fig.update_layout(
    title="Greedy vs. Non-greedy"
  )
  fig.show()

def qvalues_plot(episode):

  queryResult = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")

  buy = queryResult[queryResult['Buy']!=-1]
  sell = queryResult[queryResult['Sell']!=-1]
  hold = queryResult[queryResult['Hold']!=-1]
  df = pd.concat([buy, sell, hold]).drop_duplicates()

  fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="B/S/H Q-Values over time")
    ))
  fig.add_trace(go.Scatter(x=df.index, y=df['Buy'],
                    mode='markers',
                    name='Buy'))
  fig.add_trace(go.Scatter(x=df.index, y=df['Hold'],
                  mode='markers',
                  name='Hold'))
  fig.add_trace(go.Scatter(x=df.index, y=df['Sell'],
                  mode='markers',
                  name='Sell'))

  fig.update_layout(
    title="B/S/H Q-Values Over Time",
    xaxis_title="Trading Days",
    yaxis_title="Q-Values"
  )
  fig.show()

"""# Normality Tests for Visualization Data"""

# Quantile-Quantile Plot
def qq_plot(episodes, dataset_name, train_test):
  df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+dataset_name+"` order by episode, date")
  output = []
  for episode in episodes:
    buy = df[(df['Choice'] == '1') & (df['Episode'] == str(episode))]
    sell = df[(df['Choice'] == '2') & (df['Episode'] == str(episode))]
    hold = df[(df['Choice'] == '0') & (df['Episode'] == str(episode))]
    qqplot_data = qqplot(sell['Price Delta'], line='s').gca().lines
    fig = go.Figure()

    fig.add_trace({
        'type': 'scatter',
        'x': qqplot_data[0].get_xdata(),
        'y': qqplot_data[0].get_ydata(),
        'mode': 'markers',
        'marker': {
            'color': '#19d3f3'
        }
    })

    fig.add_trace({
        'type': 'scatter',
        'x': qqplot_data[1].get_xdata(),
        'y': qqplot_data[1].get_ydata(),
        'mode': 'lines',
        'line': {
            'color': '#636efa'
        }

    })


    fig['layout'].update({
        'title': 'Quantile-Quantile Plot',
        'xaxis': {
            'title': 'Theoretical Quantities',
            'zeroline': False
        },
        'yaxis': {
            'title': 'Sample Quantities'
        },
        'showlegend': False,
        'width': 800,
        'height': 700,
    })

    output.append(fig)
  return output
# Shapiro-Wilk Test
def shapiro_wilk(episdoes, dataset_name, train_test):
  df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+str(dataset_name)+"` order by episode, date")
  output = []
  for episode in episodes:
    buy = df[(df['Choice'] == '1') & (df['Episode'] == str(episode))]
    sell = df[(df['Choice'] == '2') & (df['Episode'] == str(episode))]
    hold = df[(df['Choice'] == '0') & (df['Episode'] == str(episode))]

    stat, p = shapiro(sell['Price Delta'])

    output.append('Statistics=%.3f, p=%.3f' % (stat, p))
  return output
    # interpret
    # alpha = 0.05
    # if p > alpha:
    #   print('Sample looks Gaussian (fail to reject H0)')
    # else:
    #   print('Sample does not look Gaussian (reject H0)')
  