"""For on-going work"""
import structure_data as sd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def testing_average_state_table(dataset_name):

  df = sd.get_data(dataset_name, 'Testing')
  
  # restrcuture data by choice and episode
  buy = df[df['Choice'] == '1']
  sell = df[df['Choice'] == '2']
  hold = df[df['Choice'] == '0']
  
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
  
  fig.show()
testing_average_state_table('2018')
