"""For on-going work"""
import structure_data as sd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def two_way_table(episodes): # compare two datasets at a time
  df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_2018` order by episode, date limit 600")
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
  fig = go.Figure(data=[go.Table(header=dict(values=['', 'Hold', 'Buy', 'Sell'], fill_color='paleturquoise'),
               cells=dict(values=[twt_dataframe.index, twt_dataframe.Hold, twt_dataframe.Buy, twt_dataframe.Sell], fill_color='cornsilk'))
                   ])
  fig.update_layout(
  title="Two-way Table: Episode " + str(episodes[0]) + ' x ' + "Episode " + str(episodes[1])
  )
  return fig
