# Import libraries and packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
from Visualization import colors

# Helper function for heatmap visual
def SetColor(x):
    if x == 1:
        return "green"
    elif x == 0:
        return "yellow"
    elif x == 2:
        return "red"

def get(data):

    '''Median state table'''
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
    fig1 = go.Figure(data=[go.Table(columnwidth = 1,
    header=dict(height = 38, values=['Action', 'Price Delta', 'Volume Delta'],
            fill_color='paleturquoise',
            align='left'),
    cells=dict(height = 25, values=[['Buy', 'Sell', 'Hold'], bsh['Price Delta'], bsh['Volume Delta']],
        fill_color='cornsilk',
        align='left'))
    ])

    fig1.update_layout(
    title="Average State",
    height=300
    )
    output.append(fig1)


    '''Price v Volume Graph'''
    colorsIdx = {'0': 'Hold', '1': 'Buy',
            '2': 'Sell'}
    cols = df['Choice'].map(colorsIdx)
    fig2 = px.scatter(df, x="Price Delta", y="Volume Delta", color=colors.get_labels(df), color_discrete_map=colors.get_colors(df))

    fig2.update_layout(
    title="B/S/H for Price/Volume Delta",
    xaxis_title="Price Delta",
    yaxis_title="Volume Delta",
    legend_title_text="Action"
    )

    output.append(fig2)

    '''Q-Values Plot'''
    df = data[(data['Buy']!=-1) & (data['Sell']!=-1) & (data['Hold']!=-1)] # -1 is E-Greedy

    fig3 = go.Figure(layout=go.Layout(
            title=go.layout.Title(text="B/S/H Q-Values over time")
        ))
    fig3.add_trace(go.Scatter(x=df['Date'], y=df['Buy'].astype(float),
                        mode='markers',
                        name='Buy',
                        line = dict(color='#01A6A4')))
    fig3.add_trace(go.Scatter(x=df['Date'], y=df['Hold'].astype(float),
                        mode='markers',
                        name='Hold',
                        line = dict(color='#F2BE4A')))
    fig3.add_trace(go.Scatter(x=df['Date'], y=df['Sell'].astype(float),
                        mode='markers',
                        name='Sell',
                        line = dict(color='#EC6355')))

    fig3.update_layout(
        title="B/S/H Q-Values Over Time",
        xaxis_title="Trading Days",
        yaxis_title="Q-Values"
    )
    output.append(fig3)
    return output
