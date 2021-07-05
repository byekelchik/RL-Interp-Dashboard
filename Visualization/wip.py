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

# BEAR: 
# BULL: 
def heatmap(episode, dataset_name, train_test):
    graphs = []
    i, j = 0, 0
    x, y = [], []
    columns = []

    df = sd.get_data(dataset_name, train_test) # Never run with Testing
    df = df[(df['Buy']!=-1) & (df['Sell']!=-1) & (df['Hold']!=-1) & (df['Episode'] == str(episode))] # -1 is E-Greedy

    price_min, price_max = min(df['Price Delta']), max(df['Price Delta'])
    volume_min, volume_max = min(df['Volume Delta']), max(df['Volume Delta'])
    x = np.arange(price_min, price_max, .5).tolist()
    y = np.arange(volume_min, volume_max, 15).tolist()
    new_df = pd.DataFrame(np.zeros(((len(y), len(x)))))

    for i in range(1, len(x)):
        for j in range(1, len(y)):
            values = df['Choice'][(df['Price Delta'].astype(float).between(x[i-1], x[i], inclusive = True)) & (df['Volume Delta'].astype(float).between(y[j-1], y[j], inclusive = True))]
            new_df[i-1][j-1] = values.median() if len(values) > 0 else -1
    fig = go.Figure(go.Heatmap(z=new_df, x=x, y=y))
    fig.update_layout(
        title="Price v Volume Heatmap",
        xaxis_title="Price Delta",
        yaxis_title="Volume Delta"
    )
    
    fig.show()
heatmap(8, '2018', 'Training')

# A: for a bear market('covid'), x: price, y: volume. 