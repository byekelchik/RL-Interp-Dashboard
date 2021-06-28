"""This is the main frontend module"""
# TODO:
# 1. List the proper number or episodes on sidebar, ulan
# 2. Fix graph output so that choosing 1->3->2 outputs the correct graph, ulan
# 3. Fix visuals to allow for a dataset change
# 4. Set up visuals.py to call dataset only once rather than per function call
# 5. Whole numbers only, ulan

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# Creates sidebar strcuture
controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Dataset"),
                dcc.Dropdown(
                    id="dataset_name",
                    options=[
                        {"label": '2018', "value": '2018'},
                        {"label": 'COVID', "value": 'covid'}
                    ],
                    value='2018',
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Train or Test"),
                dcc.Dropdown(
                    id="train_test",
                    options=[
                        {"label": 'Train', "value": 'Train'},
                        {"label": 'Test', "value": 'Test'}
                    ],
                    value="Train",
                ),
            ]
        ),
        dbc.FormGroup(
            [
            dbc.Label("Episodes"),
            dcc.Checklist(id="episodes",
                    options=[
                        {"label": "1", "value": 1},
                        {"label": "2", "value": 2},
                        {"label": "3", "value": 3},
                        # {label:i, value:i } for i in data
                    ],
                    value=[1]
                    )
            ]
        ),
    ],
    body=True,
)

# Frontend layout for graphs
app.layout = dbc.Container(
    [
        html.Hr(),
        html.H1("Interpretability Dashboard", style={'text-align': 'center'}), # Header
        html.Hr(),
        # Columns for side panel and the outputted graphs and tables
        dbc.Row(
            [
                dbc.Col(html.Div(controls), width=2),
                dbc.Col(html.Div(id="delta-table"), width=4),
                dbc.Col(html.Div(id="delta-graph"), width=6),
            ],
            align="start",
        ),
    ],
    fluid=True,
)

#Callback for updating graph based on sidebar input
@app.callback(# TODO: output not correct for graphs, it needs to reset the graph then output a new one rather than appending to current graph
    Output(component_id="delta-graph", component_property="children"),
    [
        Input(component_id="episodes", component_property="value"),
        Input(component_id="dataset_name", component_property="value"),
    ],
)
def make_graphs(episodes, dataset_name):
    output=[]
    i = 0
    df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+dataset_name+"` order by episode, date")
    # Get a figure for each passed parameter
    for vis in vls.average_price_graph(episodes, str(dataset_name), df):
        output.append(dcc.Graph(id='avg_price_graph'+str(i), figure=vis))
        i += 1
    return output

#Callback for updating graph based on sidebar input
@app.callback(
    Output(component_id="delta-table", component_property="children"),
    [
        Input(component_id="episodes", component_property="value"),
        Input(component_id="dataset_name", component_property="value"),
    ],
)
def make_table(episodes, dataset_name):
    output=[]
    i = 0
    df = sd.get_data("select * from `irlts-317602.Training_Data_15eps.training_data_10eps_"+dataset_name+"` order by episode, date")
    # Get a figure for each passed parameter
    for vis in vls.average_state_table(episodes, str(dataset_name), df):
        output.append(dcc.Graph(id='avg_price_table'+str(i), figure=vis))
        i += 1
    return output
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)

