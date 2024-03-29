# Import libraries and packages
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
from Visualization import colors

# not operational right now, focusing on testing
def heatmap(episode, data):
    graphs = []
    i, j = 0, 0
    x, y = [], []
    columns = []

    df = data # Never run with Testing
    df = df[(df['Episode'] == str(episode))] # choose the episode wanted for analysis

    # get max and min values
    price_min, price_max = min(df['Price Delta']), max(df['Price Delta'])
    volume_min, volume_max = min(df['Volume Delta']), max(df['Volume Delta'])

    # create bins with distribution as close to normal as possible
    x = pd.cut(df['Price Delta'], retbins=True, bins=pd.interval_range(start=price_min-.1, end=price_max+.1, periods = 15))
    y = pd.cut(df['Volume Delta'], retbins=True, bins=pd.interval_range(start=volume_min-1, end=volume_max+1, periods = 15))

    # convert intervalindex to tuple for looping
    x = x[1].to_tuples()
    y = y[1].to_tuples()

    # fill df with zeros to initialize 
    new_df = pd.DataFrame(np.zeros(((len(y)-1, len(x)-1))))

    # iterate through entire df and replace with action for the given price/volume delta
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            values = df['Choice'][(df['Price Delta'].astype(float).between(x[i-1][0], x[i][0], inclusive = True)) & (df['Volume Delta'].astype(float).between(y[j-1][0], y[j][0], inclusive = True))]
            new_df[i-1][j-1] = values.median() if len(values) > 0 else -2

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
    return fig

def price_v_volume(episodes, data):  # compare two datasets at a time

    output = []
    df = data
    for episode in episodes:
        df = df[df['Episode'] == str(episode)]

        fig = px.scatter(df, x="Price Delta", y="Volume Delta",color=colors.get_labels(df), color_discrete_map=colors.get_colors(df))

        fig.update_layout(
        title="Episode "+str(episode)+": B/S/H for Price/Volume Delta",
        xaxis_title="Price Delta",
        yaxis_title="Volume Delta",
        legend_title_text='Action',
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
        )

        output.append(fig)
        df = data
    return output

# INPUT: 2 episodes to compare
def two_way_table(episodes, data): # compare two datasets at a time
    df = data
    twt_dataframe = pd.DataFrame([[0, 0, 0], [0, 0, 0], [0, 0, 0]], columns=['Hold', 'Buy', 'Sell'], index=['Hold', 'Buy', 'Sell'])
    total = 0
    # split data into a df/episode
    ep_one = df[df['Episode'] == str(episodes[0])]
    ep_two = df[df['Episode'] == str(episodes[1])]

    # add overlapping values between two dfs to final table df
    for c_x, v_x in enumerate(['Hold', 'Buy', 'Sell']):
        for c_y in range(0, 3):
            temp = pd.merge(ep_one[['Date', 'Choice']][ep_one['Choice'] == str(c_x)], ep_two[['Date', 'Choice']][ep_two['Choice']== str(c_y)], on='Date', how='inner')
            twt_dataframe[v_x].iloc[c_y] = len(temp.index)
            total += len(temp.index)

    # create figure and return
    fig = go.Figure(data=[go.Table(header=dict(height = 38, values=['', 'Hold', 'Buy', 'Sell'], fill_color='#99A8B2', align='left'),
                cells=dict(height = 25, values=[twt_dataframe.index, twt_dataframe.Hold, twt_dataframe.Buy, twt_dataframe.Sell], fill_color='#393E46', align='left'))
                    ])
    fig.update_layout(
    title="Two-way Table: Episode " + str(episodes[0]) + ' x ' + "Episode " + str(episodes[1]),
    height=300,
    paper_bgcolor='#393E46',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#FFFFFF'
    )
    return fig

# Average state(Price, Volume) table
# INPUT: specific episodes, name of dataset being used(COVID, 2018), train or test data
def average_state_table(episodes, data):

    df = data

    fig_output = []

    for episode in episodes:
        # restrcuture data by choice and episode
        buy = df[(df['Choice'] == '1') & (df['Episode'] == str(episode))]
        sell = df[(df['Choice'] == '2') & (df['Episode'] == str(episode))]
        hold = df[(df['Choice'] == '0') & (df['Episode'] == str(episode))]
        # check to confirm non-empty dfs
        if len(hold.index) == 0:
            hold = hold.append(pd.Series(0, index=df.columns), ignore_index=True)
        if len(sell.index) == 0:
            sell = sell.append(pd.Series(0, index=df.columns), ignore_index=True)
        if len(hold.index) == 0:
            hold = hold.append(pd.Series(0, index=df.columns), ignore_index=True)
        bsh = pd.concat([buy.median().round(2).astype(str) + '%', sell.median().round(2).astype(str) + '%', hold.median().round(2).astype(str) + '%'])

        # create plotly table
        fig = go.Figure(data=[go.Table(columnwidth = 1,
        header=dict(height = 38, values=['Action', 'Price Delta', 'Volume Delta'],
                    fill_color='#99A8B2',
                    align='left'),
        cells=dict(height = 25, values=[['Buy', 'Sell', 'Hold'], bsh['Price Delta'], bsh['Volume Delta']],
                    fill_color='#393E46',
                    align='left'))
        ])

        fig.update_layout(
        title="Episode "+str(episode),
        height=300,
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
        )

        # add to output list to send to dash
        fig_output.append(fig)

    return fig_output

# Average state(Price, Volume) graph
# INPUT: specific episodes, name of dataset being used(COVID, 2018)
def inter_state_delta_graph(episodes, data):

    fig_output = []
    df = data

    buy = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
    sell = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
    hold = pd.DataFrame(columns = ['Date', 'Hold', 'Buy', 'Sell', 'Choice', 'Episode','Price Delta', 'Volume Delta', 'Adj Close'])
    
    
    for episode in episodes:
        buy = buy.append(df[(df['Choice'] == '1') & (df['Episode'] == str(episode))].median(), ignore_index=True)
        sell = sell.append(df[(df['Choice'] == '2') & (df['Episode'] == str(episode))].median(), ignore_index=True)
        hold = hold.append(df[(df['Choice'] == '0') & (df['Episode'] == str(episode))].median(), ignore_index=True)
    
    # check to confirm non-empty dfs
    if len(hold.index) == 0:
        hold = hold.append(pd.Series(0, index=df.columns), ignore_index=True)
    if len(sell.index) == 0:
        sell = sell.append(pd.Series(0, index=df.columns), ignore_index=True)
    if len(buy.index) == 0:
        buy = buy.append(pd.Series(0, index=df.columns), ignore_index=True)

    # plot a line for the specified number of episodes
    for state in ['Price', 'Volume']:
        fig = go.Figure(layout=go.Layout(
            title=go.layout.Title(text="Average Price State by Episode")
        ))
        # add line and markers for buy values by episode
        fig.add_trace(go.Scatter(x=episodes, y=buy[state+' Delta'],
                        mode='lines+markers',
                        name='Buy',
                        line = dict(color='#01A6A4')))
        # add line and markers for sell values by episode
        fig.add_trace(go.Scatter(x=episodes, y=sell[state+' Delta'],
                        mode='lines+markers',
                        name='Sell',
                        line = dict(color='#EC6355')))
        # add line and markers for hold values by episode
        fig.add_trace(go.Scatter(x=episodes, y=hold[state+' Delta'],
                        mode='lines+markers',
                        name='Hold',
                        line = dict(color='#F2BE4A')))
        # update axes and format interval
        fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
            title=state+" Delta by Episode",
            xaxis_title="Episode",
            yaxis_title="% Change",
            paper_bgcolor='#393E46',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF'
        )
        fig_output.append(fig)

    return fig_output


# Average state(Price, Volume) graph
# INPUT: specific episodes, name of dataset being used(COVID, 2018)
def intra_state_delta_graph(episode, data):

    fig_output = []
    df = data[data['Episode'] == str(episode)]

    # plot a line for the specified number of episodes
    for state in ['Price', 'Volume']:
        
        # plot markers for state delta value by date
        fig= px.scatter(x=df['Date'], y=df[state+' Delta'], color=colors.get_labels(df), color_discrete_map=colors.get_colors(df))

        fig.update_layout(
            title="Episode " + str(episode) + ": Average "+state+" Delta",
            xaxis_title="Date",
            yaxis_title="% Change",
            legend_title_text='Action',
            paper_bgcolor='#393E46',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF'
        )
        fig_output.append(fig)

    return fig_output
# Helper function for heatmap visual
def SetColor(x):
    if x == 1:
        return "green"
    elif x == 0:
        return "yellow"
    elif x == 2:
        return "red"

# INPUT: lower and upper delta values, name of dataset, train or test dataset
def heatmap_visual(lower, upper, episode, data):

    graphData = data
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

def random_action_plot(episode, data):
    queryResult = data[data['Episode'] == str(episode)]

    #output: visual of the amount of random actions in a certain episode compared to real values
    ep_greedy = queryResult[queryResult['Hold']==str(-1)] #get the days when we dont go greedy
    ep_greedy_days = ep_greedy.shape[0] #get the shape of df and take the first value of list
    non_greedy_days = queryResult.shape[0] - ep_greedy_days #subtract greedy days from total trading horizon
    pct_greedy = (ep_greedy_days)/queryResult.shape[0]

    # display count of greedy vs non-greedy days
    labels = ['Greedy', 'Non-Greedy']
    values = [ep_greedy_days, non_greedy_days]

    # create pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # enhance visual
    colors = ['lightcyan', 'royalblue']
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(
        title="Greedy vs. Non-greedy",
        height=300,
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    return fig

def qvalues_plot(episode, data):

    # get data only for given episode
    data = data[data['Episode'] == str(episode)]

    df = data[(data['Buy']!=str(-1)) & (data['Sell']!=str(-1)) & (data['Hold']!=str(-1))] # -1 is E-Greedy (remove them)
    
    fig = go.Figure(layout=go.Layout(
            title=go.layout.Title(text="B/S/H Q-Values over time")
        ))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Buy'].astype(float),
                        mode='markers',
                        name='Buy',
                        line = dict(color='#01A6A4')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Hold'].astype(float),
                        mode='markers',
                        name='Hold',
                        line = dict(color='#F2BE4A')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Sell'].astype(float),
                        mode='markers',
                        name='Sell',
                        line = dict(color='#EC6355')))

    fig.update_layout(
        title="B/S/H Q-Values Over Time",
        xaxis_title="Trading Days",
        yaxis_title="Q-Values",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    return fig

"""# Normality Tests for Visualization Data"""

# Quantile-Quantile Plot
def qq_plot(episodes, dataset_name, train_test, data):
    df = data
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
def shapiro_wilk(episodes, dataset_name, train_test, data):
    df = data
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
  