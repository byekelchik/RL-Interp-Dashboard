from random import randint
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import structure_data as sd
import visuals as vls
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from Visualization import colors


# BEAR: define this
# BULL: define this
def heatmap(episode, dataset_name, train_test):
    graphs = []
    i, j = 0, 0
    x, y = [], []
    columns = []

    df = sd.get_data(dataset_name, train_test) # Never run with Testing
    df = df[(df['Episode'] == str(episode))]

    price_min, price_max = min(df['Price Delta']), max(df['Price Delta'])
    volume_min, volume_max = min(df['Volume Delta']), max(df['Volume Delta'])

    x = pd.cut(df['Price Delta'], retbins=True, bins=pd.interval_range(start=price_min-.1, end=price_max+.1, periods = 15))
    y = pd.cut(df['Volume Delta'], retbins=True, bins=pd.interval_range(start=volume_min-1, end=volume_max+1, periods = 15))
    x = x[1].to_tuples()
    y = y[1].to_tuples()

    new_df = pd.DataFrame(np.zeros(((len(y)-1, len(x)-1))))
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            values = df['Choice'][(df['Price Delta'].astype(float).between(x[i-1][0], x[i][0], inclusive = True)) & (df['Volume Delta'].astype(float).between(y[j-1][0], y[j][0], inclusive = True))]
            new_df[i-1][j-1] = values.median() if len(values) > 0 else -2

    fig = go.Figure(go.Heatmap(z=new_df, x=x[1], y=y[1], colorscale=colors.colorscale))
    fig.update_layout(
        title="Price v Volume Heatmap",
        xaxis_title="Price Delta",
        yaxis_title="Volume Delta"
    )
    
    return fig
heatmap(0, '2018', 'Training')

# A: for a bear market('covid'), x: price, y: volume. 