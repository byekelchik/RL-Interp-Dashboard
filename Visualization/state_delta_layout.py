'''Creates visual under respective tab'''

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls

def make_layout():
    """Creates layout for visualization"""
    return dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Dataset"),
                            dcc.Dropdown(
                                id="t2_dataset_name",
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
                                id="t2_train_test",
                                options=[
                                    {"label": 'Train', "value": 'Training'},
                                    {"label": 'Test', "value": 'Testing'}
                                ],
                                value="Training",
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
                                value=[1, 2],
                            )
                        ]
                    )
                ],
            body=True,
            )
        ),
            dbc.Col(id="delta-table", width=4),
            dbc.Col(id="delta-graph", width=6),
        ]
    )

def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback([
        Output(component_id="delta-graph", component_property="children"),
        Output(component_id="delta-table", component_property="children")],
        [
            Input(component_id="episodes", component_property="value"),
            Input(component_id="t2_dataset_name", component_property="value"),
            Input(component_id="t2_train_test", component_property="value"),
        ],
    )
    def make_graphs(episodes, dataset_name, train_test):
        graphs, tables = [], []
        i = 0
        df = sd.get_data(dataset_name, train_test)
        # Get a figure for each passed parameter
        for vis in vls.average_state_table(episodes, df):
            tables.append(dcc.Graph(id='average_state_table'+str(i), figure=vis))
            i += 1
        i = 0
        for vis in vls.average_price_graph(episodes, df):
            graphs.append(dcc.Graph(id='avg_price_graph'+str(i), figure=vis))
            i += 1
        return graphs, tables
