#Import libraries and packages
# !pip install yfinance
# !pip install --upgrade google-cloud-bigquery
# !pip install pandas-gbq -U
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
import structure_data
from structure_data import get_data, sys, os, pd

# Visualizations
  # Parameters:
  # 1.   Episodes
  # 2.   Dataset name(COVID, 2018)
  # 3.   Train or Test data


# def confusion_matrix(): # compare two datasets at a time
#   df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '1' order by date")
#   # generate random values for truth
#   truth = pd.DataFrame(np.random.randint(0,3,size=(len(df)+4)), columns=['Truth'])
#   df['Truth'] = truth
#   buyVal = []
#   buy = df[['Choice', 'Truth']][df['Choice'] == '1']
#   sell = df[['Choice', 'Truth']][df['Choice'] == '2']
#   hold = df[['Choice', 'Truth']][df['Choice'] == '0']
#   # buy = buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count()
#   # sell = sell['Choice'][sell['Choice'].astype(int) == sell['Truth'].astype(int)].count()
#   # hold = hold['Choice'][hold['Choice'].astype(int) == hold['Truth'].astype(int)].count()

#   # fig = go.Figure(data=go.Heatmap(labels=dict(x="What Should have Happened", y="What Algo DId", color="Viridis"),
#   #                  z=[[int(buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count()), int(buy['Choice'][buy['Choice'].astype(int) == buy[buy['Truth'] == '2'].astype(int)].count()), int(buy['Choice'][buy['Choice'].astype(int) == buy[buy['Truth'] == '0'].astype(int)].count())],
#   #                     [sell['Choice'][sell['Choice'].astype(int) == sell[sell['Truth']=='1'].astype(int)].count(), sell['Choice'][sell['Choice'].astype(int) == sell['Truth'].astype(int)].count(), sell['Choice'][sell['Choice'].astype(int) == sell[sell['Truth']=='0'].astype(int)].count()],
#   #                     [hold['Choice'][hold['Choice'].astype(int) == hold[hold['Truth']=='1'].astype(int)].count(), hold['Choice'][hold['Choice'].astype(int) == hold[hold['Truth']=='2'].astype(int)].count(), hold['Choice'][hold['Choice'].astype(int) == hold['Truth'].astype(int)].count()]],
#   #                  x=['Buy', 'Sell', 'Hold'],
#   #                  y=['Buy', 'Sell', 'Hold'],
#   #                  hoverongaps = False))
#   # fig.show()
#   print(buy['Choice'][buy['Choice'].astype(int) == buy['Truth'].astype(int)].count().iloc[0])

###USE PLOTLY###

# Average state(Price, Volume) table
# INPUT: specific episodes, name of dataset being used(COVID, 2018), train or test data
def average_state_table(episodes, dataset_name, train_test):

  df = structure_data.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+dataset_name+"` order by date")

  for episode in episodes:
    buy = df[(df['Choice'] == '1') & (df['Episode'] == str(episode))]
    sell = df[(df['Choice'] == '2') & (df['Episode'] == str(episode))]
    hold = df[(df['Choice'] == '0') & (df['Episode'] == str(episode))]
    bsh = pd.concat([buy.median().round(2).astype(str) + '%', sell.median().round(2).astype(str) + '%', hold.median().round(2).astype(str) + '%'])

    fig = go.Figure(data=[go.Table(columnwidth = 1,
      header=dict(height = 38, values=['Action', 'Price Delta', 'Volume Delta'],
                  fill_color='paleturquoise',
                  align='left'),
      cells=dict(height = 25, values=[['Buy', 'Sell', 'Hold'], bsh['Price Delta'], bsh['Volume Delta']],
                fill_color='cornsilk',
                align='left'))
    ])

    fig.update_layout(
    title="Episode "+str(episode)
    )

    fig.show()
average_state_table([1, 2], '2018', 'Train')
# Average state(Price, Volume) graph
# INPUT: specific episodes, name of dataset being used(COVID, 2018)
def average_state_graph(episodes, dataset_name):

  df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+dataset_name+"` order by episode, date")
  buy = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  sell = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  hold = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
  # plot a line for the specified number of episodes
  for episode in episodes:
    buy = buy.append(df[(df['Choice'] == '1') & (df['Episode'] == str(episode))].median(), ignore_index=True)
    sell = sell.append(df[(df['Choice'] == '2') & (df['Episode'] == str(episode))].median(), ignore_index=True)
    hold = hold.append(df[(df['Choice'] == '0') & (df['Episode'] == str(episode))].median(), ignore_index=True)
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
    fig.show()

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

  graphData = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by episode, date")
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
  df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")
  fig = px.line(df, x=df.index, y="Adj Close", title='Price Over Time')
  fig.show()

def randon_action_plot(episode):
  queryResult = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")

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

  queryResult = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '"+str(episode)+"' order by date")

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
def qq_plot():
  df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '6' order by date")
  buy = df[df['Choice'] == '1']
  sell = df[df['Choice'] == '2']
  hold = df[df['Choice'] == '0']
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

  fig.show()

# Shapiro-Wilk Test
def shapiro_wilk():
  df = get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` where episode = '10' order by date")
  buy = df[df['Choice'] == '1']
  sell = df[df['Choice'] == '2']
  hold = df[df['Choice'] == '0']

  stat, p = shapiro(sell['Price Delta'])

  print('Statistics=%.3f, p=%.3f' % (stat, p))
  # interpret
  alpha = 0.05
  if p > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
  else:
    print('Sample does not look Gaussian (reject H0)')