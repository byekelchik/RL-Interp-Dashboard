# Import libraries and packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
from Visualization import colors
import numpy as np


def median_state_table(data):

    df = data
    output = []
    # restrcuture data by choice and episode
    buy = df[df['Choice'] == '1']
    sell = df[df['Choice'] == '2']
    hold = df[df['Choice'] == '0']

    # check to confirm non-empty dfs
    if len(hold.index) == 0:
        hold = hold.append(pd.Series(0, index=df.columns), ignore_index=True)
    if len(sell.index) == 0:
        sell = sell.append(pd.Series(0, index=df.columns), ignore_index=True)
    if len(buy.index) == 0:
        buy = buy.append(pd.Series(0, index=df.columns), ignore_index=True)

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
    title="Average State",
    height=300,
    paper_bgcolor='#393E46',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#FFFFFF'
    )
    return fig


def price_v_volume(data):
    df = data
    colorsIdx = {'0': 'Hold', '1': 'Buy',
            '2': 'Sell'}
    cols = df['Choice'].map(colorsIdx)
    fig = px.scatter(df, x="Price Delta", y="Volume Delta", color=colors.get_labels(df), color_discrete_map=colors.get_colors(df))

    fig.update_layout(
    title="B/S/H for Price/Volume Delta",
    xaxis_title="Price Delta",
    yaxis_title="Volume Delta",
    legend_title_text="Action",
    paper_bgcolor='#393E46',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#FFFFFF'
    )

    return fig

def qvalues_plot(data):
    df = data[(data['Buy']!=-1) & (data['Sell']!=-1) & (data['Hold']!=-1)] # -1 is E-Greedy

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

def heatmap(data):
    i, j = 0, 0
    x, y, columns = [], [], []

    df = data # Never run with Testing

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

def buy_v_pricedelta(data): 

    df = data 
    buy = df[(df['Choice'] == '1')]     
    fig = px.histogram(buy, x="Price Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Price Delta v Buy Action Histogram",
        xaxis_title="Price Delta",
        yaxis_title="Buy",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )

    return fig

def sell_v_pricedelta(data): 

    df = data 
    sell = df[(df['Choice'] == '2')]    
    fig = px.histogram(sell, x="Price Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Price Delta v Sell Action Histogram",
        xaxis_title="Price Delta",
        yaxis_title="Sell",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    
    return fig

def hold_v_pricedelta(data): 

    df = data 
    hold = df[(df['Choice'] == '0')]     
    fig = px.histogram(hold, x="Price Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Price Delta v Hold Action Histogram",
        xaxis_title="Price Delta",
        yaxis_title="Hold",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    
    return fig

def buy_v_volumedelta(data): 

    df = data 
    buy = df[(df['Choice'] == '1')]     
    fig = px.histogram(buy, x="Volume Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Volume Delta v Buy Action Histogram",
        xaxis_title="Volume Delta",
        yaxis_title="Buy",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )

    return fig

def sell_v_volumedelta(data): 

    df = data 
    sell = df[(df['Choice'] == '2')]    
    fig = px.histogram(sell, x="Volume Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Volume Delta v Sell Action Histogram",
        xaxis_title="Volume Delta",
        yaxis_title="Sell",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    
    return fig

def hold_v_volumedelta(data): 

    df = data 
    hold = df[(df['Choice'] == '0')]     
    fig = px.histogram(hold, x="Volume Delta") 

    fig.update_layout(
        yaxis = dict(
                tickmode = 'linear',
                tick0 = 0,
                dtick = 1
            ),
        title="Volume Delta v Hold Action Histogram",
        xaxis_title="Volume Delta",
        yaxis_title="Hold",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )
    
    return fig
    





